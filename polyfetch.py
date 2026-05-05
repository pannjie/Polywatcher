import os
import datetime
import pandas as pd
import statistics
import uvicorn
import asyncio
import httpx
import numpy as np
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from db.db import insert_wallet, update_wallet_analysis, get_wallets, metadata, engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager


load_dotenv()

from fastapi import FastAPI, HTTPException, status

GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API = "https://data-api.polymarket.com"
GOLDSKY_URL = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn"
POLYGONSCAN_API = "https://api.etherscan.io/v2/api"

# 25 March 2026
# Use Leaderboard API to loop through the top accounts, and verify them against the current params
# Modify the output data for USDC.e and timestamps, to create a more readable format for the end user # update: let's just keep the raw data as is, no point making half of it readable and half of it technical.
# Integrate more blockchain data for analysis, including their wallet age and interactions with DeFi tools known for money laundering, such as Tornado Cash.
# Graph Analysis for using wallets as nodes, to see if all wallets within a market are connected. #update: not possible, not meaningful

#kickstart the scheduler to run the leaderboard function every 24 hours, to keep the database updated with the daily top trades.
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(leaderboard, "cron", hour=3, minute=0)
    scheduler.add_job(analyse_leaderboard, "cron", hour=3, minute=15)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def health():
    return {"status": "ok"}

def get_start_date(chain_data, address):
    for tx in chain_data.get("result", []):
        if tx.get("to", "").lower() == address.lower():
            return int(tx.get("timeStamp", 0))
    return None

def find_closed_positions(closed_positions_data):
    df_1 = pd.json_normalize(closed_positions_data)
    if df_1.empty or 'realizedPnl' not in df_1.columns:
        return []
    df_1 = df_1.sort_values('realizedPnl', ascending=False)
    return df_1.head(3)['timestamp'].astype(int).tolist()

def find_event_slug(closed_positions_data):
    df_1 = pd.json_normalize(closed_positions_data)
    if df_1.empty or 'realizedPnl' not in df_1.columns:
        return []
    df_1 = df_1.sort_values('realizedPnl', ascending=False)
    return df_1.head(3)['eventSlug'].tolist()

def find_event_slug_all(closed_positions_data):
    df_1 = pd.json_normalize(closed_positions_data)
    if df_1.empty or 'realizedPnl' not in df_1.columns:
        return []
    df_1 = df_1.sort_values('realizedPnl', ascending=False)
    df_1 = df_1[df_1['realizedPnl'] > 0]
    return df_1['eventSlug'].tolist()

 

async def run_analysis(address: str):
    chain, raw_closed = await asyncio.gather(
        get_chain(address),
        get_closed_positions(address),
    )
    start_date = get_start_date(chain, address)
    top_3_timestamps = find_closed_positions(raw_closed)
    top_3_event_slug = find_event_slug(raw_closed)
    all_event_slug = find_event_slug_all(raw_closed)

    creator, activity, positions, redemptions, activity_timed, *top_activity = await asyncio.gather(
        get_creator(address),
        get_activity(address),
        get_positions(address),
        get_redemptions(address),
        get_activity_2(address, start_date),
        *[get_activity_3(address, ts) for ts in top_3_timestamps]
    )
    closed_positions = raw_closed
    pnl = closed_positions

    spread_analysis = analyse_spread(positions, closed_positions)
    spread_risk = analyse_spread_risk(spread_analysis)

    volume_48hr = volume_gap(activity_timed)
    volume_48hr_risk = volume_gap_risk(volume_48hr)

    time_gap = get_timegap(redemptions, creator)
    time_gap_risk = get_timegap_risk(time_gap)

    value_redemptions, num_positions = analyse_volume(positions, closed_positions, redemptions)
    volume_risk = analyse_volume_risk(value_redemptions, closed_positions, positions)

    top_activity_1, top_activity_2, top_activity_3 = analyse_top_activity(top_activity, top_3_event_slug)
    activity_risk = analyse_top_activity_risk(top_activity_1, top_activity_2, top_activity_3)

    slug_similarity = await analyse_slug_similarity(all_event_slug)
    slug_similarity_risk = analyse_slug_similarity_risk(slug_similarity)

    total_profit = analyse_profits(pnl)
    profit_risk = analyse_profit_risk(total_profit)

    success_rate, success_count, failure_count = analyse_success(pnl)
    success_risk = analyse_success_risk(success_rate)

    high_frequency = high_frequency_check(activity)

    size_deviation, average_size = analyse_relative_size(positions, closed_positions)
    size_deviation_risk = analyse_relative_size_risk(size_deviation)

    sum_input = analyse_chain(chain, address)
    sum_input_risk = analyse_chain_risk(sum_input)

    sum_input_48hr = analyse_chain_48hr(chain, address)
    sum_input_48hr_risk = analyse_chain_48hr_risk(sum_input_48hr)

    sum_input_24hr = analyse_chain_24hr(chain, address)
    sum_input_24hr_risk = analyse_chain_24hr_risk(sum_input_24hr)

    withdrawal_48hr = chain_gap(chain, address)
    chain_gap_result = chain_gap_risk(withdrawal_48hr, sum_input_48hr)

    return {
        #raw
        "creator": creator,
        "activity": activity,
        "positions": positions,
        "closed_positions": closed_positions,
        "redemptions": redemptions,
        "pnl": pnl,
        #1 SPREAD ANALYSIS
        "spread_analysis": round(spread_analysis, 2),
        "spread_risk": spread_risk,
        #2 VOLUME GAP ANALYSIS
        "activity_timed": activity_timed,
        "volume_48hr": round(volume_48hr, 2),
        "volume_48hr_risk": volume_48hr_risk,
        #3 TIME GAP ANALYSIS
        "time_gap": time_gap,
        "time_gap_risk": time_gap_risk,
        #3 VOLUME ANALYSIS
        "volume_risk": volume_risk,
        "value_redemptions": round(value_redemptions, 2),
        "num_positions": num_positions,
        #PROXIMITY ANALYSIS
        "top_3_timestamps": top_3_timestamps,
        "top_3_event_slug": top_3_event_slug,
        "top_activity": top_activity,
        "top_activity_1": round(top_activity_1, 2),
        "top_activity_2": round(top_activity_2, 2),
        "top_activity_3": round(top_activity_3, 2),
        "activity_risk": activity_risk,
        #AI SIMILIARITY ANALYSIS
        "all_event_slug": all_event_slug,
        "slug_similarity": slug_similarity,
        "slug_similarity_risk": slug_similarity_risk,
        #4 PROFIT ANALYSIS
        "total_profit": round(total_profit, 2),
        "profit_risk": profit_risk,
        #5 SUCCESS RATE ANALYSIS
        "success_rate": round(success_rate, 2),
        "success_count": success_count,
        "failure_count": failure_count,
        "success_risk": success_risk,
        #6 HIGH FREQUENCY ANALYSIS
        "high_frequency": high_frequency,
        #SIZE DEVIATION ANALYSIS
        "size_deviation": size_deviation,
        "size_deviation_risk": size_deviation_risk,
        "average_size": average_size,
        # BLOCKCHAIN FIRST 20 TX ANALYSIS
        "sum_input": round(sum_input, 2),
        "sum_input_risk": sum_input_risk,
        # BLOCKCHAIN FIRST 48HR ANALYSIS
        "sum_input_48hr": round(sum_input_48hr, 2),
        "sum_input_48hr_risk": sum_input_48hr_risk,
        # BLOCKCHAIN FIRST 24HR ANALYSIS
        "sum_input_24hr": round(sum_input_24hr, 2),
        "sum_input_24hr_risk": sum_input_24hr_risk,
        # BLOCKCHAIN GAP ANALYSIS
        "chain_gap": chain_gap_result,
        "chain_output": round(withdrawal_48hr, 2),
        "chain_raw": chain.get("result", [])
    }

@app.get("/api/user/{address}")
async def user_raw(address: str):
    try:
        return await run_analysis(address)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not fetch data for address {address}. Error: {e}")
    
@app.get("/api/leaderboard-results")
async def leaderboard_results():
    return get_wallets()

@app.get("/api/leaderboard")
async def leaderboard():
    data = await get_leaderboard()
    metadata.create_all(engine)
    for entry in data:
        insert_wallet(
            rank=entry.get("rank"),
            username=entry.get("userName"),
            proxywallet=entry.get("proxyWallet"),
            pnl=entry.get("pnl", 0),
            vol=entry.get("vol", 0)
        )
    return data

@app.get("/api/analyse-leaderboard")
async def analyse_leaderboard():
    wallets = get_wallets()
    for wallet in wallets:
        await asyncio.sleep(20)
        try:
            result = await run_analysis(wallet["proxywallet"])
            update_wallet_analysis(
                proxywallet=wallet["proxywallet"],
                market_spread=result.get("spread_analysis"),
                cashout_gap=result.get("time_gap"),
                creation_volume=result.get("volume_48hr"),
                success_rate=result.get("success_rate"),
                position_size=result.get("size_deviation"),
                deposits_24h=result.get("sum_input_24hr"),
                ai_similarity=result.get("slug_similarity"),
            )
        except Exception as e:
            print(f"Failed analysis for {wallet['proxywallet']}: {e}")
            continue
    return {"status": "done", "processed": len(wallets)}

async def get_leaderboard():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/v1/leaderboard", params={"category": "OVERALL", "timePeriod": "DAY", "orderBy": "PNL", "limit": 25})
        res.raise_for_status()
        leaderboard = res.json()
        return leaderboard
    
async def get_chain(address):
    async with httpx.AsyncClient() as client:
        res = await client.get(f'{POLYGONSCAN_API}', params={"module": "account", "action": "tokentx", "address": address, "startblock": 0, "endblock": 99999999, "chainid": 137, "sort": "asc", "apikey": os.getenv("POLYGONSCAN_API_KEY"), "offset": 500, "page": 1})
        res.raise_for_status()
        data = res.json()
        return data


async def get_creator(address):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{GAMMA_API}/public-profile", params={"address": address})
        res.raise_for_status()
        data = res.json()

        return data
       
async def get_redemptions(user):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/activity", params={"user": user, "type": "REDEEM", "limit": 1000})
        res.raise_for_status()
        return res.json()


async def get_activity(user, limit=1000):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/activity", params={"user": user, "limit": limit})
        res.raise_for_status()
        data = res.json()

    return data

async def get_activity_2(user, start_date, limit=1000):
    if start_date is None:
        return []
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/activity", params={"user": user, "side": "BUY", "start": start_date, "end": start_date + 172800, "limit": limit})
        res.raise_for_status()
        return res.json()
    
async def get_activity_3(user, ts, limit=1000):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/activity", params={"user": user, "side": "BUY", "start": ts - 172800 , "end": ts, "limit": limit})
        res.raise_for_status()
        return res.json()


async def get_positions(user, limit=1000):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/positions", params={"user": user, "limit": limit})
        res.raise_for_status()
        data = res.json()

    return data    
    
async def get_closed_positions(user, limit=1000):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/closed-positions", params={"user": user, "limit": limit})
        res.raise_for_status()
        data = res.json()
    return data    



async def get_pnl(address):
    all_positions = []
    skip = 0
    batch_size = 100

    async with httpx.AsyncClient() as client:
        while True:
            query = """
            {
              userPositions(
                where: { user: "%s" }
                first: %d
                skip: %d
              ) {
                tokenId
                amount
                avgPrice
                realizedPnl
                totalBought
              }
            }
            """ % (address.lower(), batch_size, skip)

            res = await client.post(GOLDSKY_URL, json={"query": query}, timeout=30)
            res.raise_for_status()
            result = res.json()
            if "data" not in result or result["data"] is None:
                print(f"GOLDSKY ERROR: {result}")
                break

            positions = result["data"]["userPositions"]
            all_positions.extend(positions)

            if len(positions) < batch_size:
                break
            skip += batch_size

    return all_positions


HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
hf_client = InferenceClient(api_key=HF_API_KEY)

async def get_embeddings(texts: list[str]):
    loop = asyncio.get_running_loop()
    try:
        embeddings = await loop.run_in_executor(
            None,
            lambda: hf_client.feature_extraction(text=texts, model=HF_MODEL)
        )
        return embeddings
    except Exception as e:
        print(f"HF embedding error: {e}")
        return None

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

async def analyse_slug_similarity(slugs: list[str]):
    if len(slugs) < 2:
        return 0

    embeddings = await get_embeddings(slugs)
    if embeddings is None:
        return 0

    scores = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            scores.append(cosine_similarity(embeddings[i], embeddings[j]))

    return round(sum(scores) / len(scores), 3)

def analyse_slug_similarity_risk(slug_similarity):
    avg = slug_similarity
    if avg > 0.8:
        return "extreme risk"
    elif avg > 0.7:
        return "very high risk"
    elif avg > 0.6:
        return "high risk"
    elif avg > 0.5:
        return "medium risk"
    elif avg > 0.4:
        return "low risk"
    else:
        return "minimal risk"



#amended to check for all positions, both open and closed.
#amended to avoid over-flagging of normal users.`
##todo: Amend Javascript for better understanding. + %`
def analyse_spread(positions_data, closed_positions):
    event_ids_1 = [position.get('eventId') for position in positions_data if position.get('eventId')]
    event_ids_2 = [position.get('eventId') for position in closed_positions if position.get('eventId')]
    final_ids = event_ids_1 + event_ids_2
    if final_ids == []:
        return 0
    else:
        total = len(final_ids)
        unique = len(set(final_ids))
        similiarity_report = ((total - unique)/total) * 100
        return similiarity_report
    
def analyse_spread_risk(spread_analysis):
    if spread_analysis < 50:
        return "minimal risk"
    elif spread_analysis < 60:
        return "low risk"
    elif spread_analysis < 70:
        return "medium risk"
    elif spread_analysis < 80:
        return "high risk"
    elif spread_analysis < 90:
        return "very high risk"
    else:
        return "extreme risk"

#Compares account creation date, to the date of its first REDEEM. If less than one month has elapsed between account creation, and a redemption of more than 10,000 USD, the account will be flagged.
def get_timegap(redemptions_data, creator_data):
    if not redemptions_data:
        return None
    creator_time = creator_data.get('createdAt')
    if not creator_time:
        return None
    creator_time = datetime.datetime.fromisoformat(creator_time).timestamp()

    sorted_redemptions = sorted(redemptions_data, key=lambda x: x.get("timestamp", 0))
    first_redemption = next((redemption for redemption in sorted_redemptions if redemption.get("usdcSize", 0) > 10000), None)

    if first_redemption is None:
        return None

    #might require adjusting, too tight a margin
    gap = first_redemption.get("timestamp", 0) - creator_time
    time_gap = gap / (60 * 60 * 24) 
    time_gap = round(time_gap, 2)

    return time_gap

def get_timegap_risk(time_gap):
    if time_gap is None:
        return "unknown"
    if time_gap <= 5:
        return "extreme risk"
    elif time_gap <= 10:
        return "very high risk"
    elif time_gap <= 15:
        return "high risk"
    elif time_gap <= 25:
        return "medium risk"
    elif time_gap <= 30:
        return "low risk"
    else:
        return "minimal risk"



def analyse_volume(positions_data, closed_positions, redemptions_data):
    all_positions = positions_data + closed_positions
    num_positions = len(all_positions)
    value_redemptions = sum(redemption.get("usdcSize", 0) for redemption in redemptions_data)
    return value_redemptions, num_positions

def analyse_volume_risk(value_redemptions, closed_positions, positions_data):
    all_positions = positions_data + closed_positions
    num_positions = len(all_positions)
    risk = " "
    if (num_positions < 5 and value_redemptions > 250000) or (num_positions < 10 and value_redemptions > 500000):
        risk = f"extreme risk"
    elif (num_positions < 5 and value_redemptions > 200000) or (num_positions < 10 and value_redemptions > 400000):
        risk = f"very high risk"
    elif (num_positions < 5 and value_redemptions > 150000) or (num_positions < 10 and value_redemptions > 300000):
        risk = f"high risk"
    elif (num_positions < 5 and value_redemptions > 100000) or (num_positions < 10 and value_redemptions > 200000):
        risk = f"medium risk"
    elif (num_positions < 5 and value_redemptions > 50000) or  (num_positions < 10 and value_redemptions > 100000):
        risk = f"low risk"
    else:
        risk = f"minimal risk"
    return risk



def analyse_profits(pnl_data):
    total_profit = 0
    for pnl in pnl_data:
        total_profit += float(pnl.get("realizedPnl") or 0)
    return total_profit
  
    
def analyse_profit_risk(total_profit):
    profit_risk = " "
    if total_profit > 500000:
        profit_risk = "extreme risk"
    elif total_profit > 250000:
        profit_risk = "very high risk"
    elif total_profit > 100000:
        profit_risk = "high risk"
    elif total_profit > 50000:
        profit_risk = "medium risk"
    elif total_profit > 10000:
        profit_risk = "low risk"
    else:
        profit_risk = "minimal risk"
    return profit_risk

    
#analyses the success rate of the trader. Current studies by MIT show only 10-16% make money. If activity is both high volume and high profit, the user will be flagged for further investigation
## Should I check only the success rate of big trades? -hmmmm
def analyse_success(pnl_data):
    success = 0
    failure = 0
    for pnl in pnl_data:
        if float(pnl.get("realizedPnl") or 0) > 0:
            success += 1
        elif float(pnl.get("realizedPnl") or 0) < 0:
            failure += 1
    if success + failure == 0:
        return 0, 0, 0
    success_rate = success / (success + failure)* 100
    return success_rate, success, failure


def analyse_success_risk(success_rate):
    if success_rate > 60:
        return "extreme risk"
    elif success_rate > 50:
        return "very high risk"
    elif success_rate > 40:
        return "high risk"
    elif success_rate > 30:
        return "medium risk"
    elif success_rate > 20:
        return "low risk"
    else:
        return "minimal risk"
    

#check if the trader is using a bot or a high frequency trading strategy. If there are more than 10 trades with less than 1s apart, the user will be flagged for further investigation.  
def high_frequency_check(activity_data):
    timestamps = []
    fails = 0
    verdict = " "
    for activity in activity_data:
        if activity.get('type') == "TRADE":
            timestamps.append(activity.get("timestamp"))
    #loop through the timestamps and see if there are more than 10 trades with less than 1s apart.
    timestamps.sort()
    for i in range(len(timestamps) - 1):
        if timestamps[i + 1] - timestamps[i] < 1:
            fails += 1
    if fails > 10:
        verdict = 'Yes'
    else:
        verdict = 'No'

    return verdict

#checks if the positions is unusually large compared to other positions made by the user. If X bets 500,000 on a market when he usually bets less than 50,000, flag it as potential insider trade.

def analyse_relative_size(positions_data, closed_positions):
    all_positions = positions_data + closed_positions
    if not all_positions:
        return 0, 0

    sizes = [p.get("size", 0) for p in all_positions]
    values = [p.get("currentValue", 0) for p in all_positions]

    median_size = statistics.median(sizes)
    median_value = statistics.median(values)
    mad_size = statistics.median([abs(s - median_size) for s in sizes])
    mad_value = statistics.median([abs(v - median_value) for v in values])

    average_size = statistics.mean(sizes)

    max_deviation = 0
    for position in all_positions:
        size = position.get("size", 0)
        value = position.get("currentValue", 0)
        if mad_size > 0 and mad_value > 0:
            deviation = ((size - median_size) / mad_size + (value - median_value) / mad_value) / 2
            max_deviation = max(max_deviation, deviation)

    return round(max_deviation, 2), round(average_size, 2)

def analyse_relative_size_risk(size_deviation):
    if size_deviation > 3:
        return "extreme risk"
    elif size_deviation > 2.5:
        return "very high risk"
    elif size_deviation > 2:
        return "high risk"
    elif size_deviation > 1.5:
        return "medium risk"
    elif size_deviation > 1:
        return "low risk"
    else:
        return "minimal risk"

#checks the first trades into the proxy wallet. if the cumulative value of the first 20 trades is above X USD, flag the account for suspicious activity.
def analyse_chain(chain_data, address):
    input_data = []
    for tx in chain_data.get("result",[])[:20]:
        if tx.get("to", "").lower() == address.lower():
            input_data.append(int(tx.get("value", 0)) / 1e6)
    sum_input = sum(input_data)
    return sum_input

def analyse_chain_risk(sum_input):
    if sum_input > 100000:
        return "extreme risk"
    elif sum_input > 75000:
        return "very high risk"
    elif sum_input > 50000:
        return "high risk"
    elif sum_input > 25000:
        return "medium risk"
    elif sum_input > 10000:
        return "low risk"
    else:        
        return "minimal risk"

#analyse the amount uploaded to the proxy wallet in its first 24/48 hours. if the amount is above X USD, flag the account for suspicious activity.
def analyse_chain_48hr(chain_data, address):
    input_data_48 = []
    first_timestamp = None
    for tx in chain_data.get("result",[]):
        if tx.get("to", "").lower() == address.lower():
            timestamp = int(tx.get("timeStamp", 0))
            if first_timestamp is None:
                first_timestamp = timestamp
            if timestamp - first_timestamp < 172800:  
                input_data_48.append(int(tx.get("value", 0)) / 1e6)
    sum_input_48 = sum(input_data_48)
    return sum_input_48

def analyse_chain_48hr_risk(input_data_48):
    if input_data_48 > 100000:
        return "extreme risk" 
    elif input_data_48 > 75000:
        return "very high risk" 
    elif input_data_48 > 50000:
        return "high risk" 
    elif input_data_48 > 25000:
        return "medium risk" 
    elif input_data_48 > 10000:
        return "low risk" 
    else:        
        return "minimal risk"

    
def analyse_chain_24hr(chain_data, address):
    input_data_24 = []
    first_timestamp = None
    for tx in chain_data.get("result",[]):
        if tx.get("to", "").lower() == address.lower():
            timestamp = int(tx.get("timeStamp", 0))
            if first_timestamp is None:
                first_timestamp = timestamp
            if timestamp - first_timestamp < 86400:
                input_data_24.append(int(tx.get("value", 0)) / 1e6)
    return sum(input_data_24)

def analyse_chain_24hr_risk(sum_input_24):
    if sum_input_24 > 50000:
        return "extreme risk"
    elif sum_input_24 > 25000:
        return "very high risk"
    elif sum_input_24 > 12500:
        return "high risk"
    elif sum_input_24 > 6250:
        return "medium risk"
    elif sum_input_24 > 3125:
        return "low risk"
    else:
        return "minimal risk"

def chain_gap(chain_data, address):
    # Anchor the 48hr window to the first deposit (input), not first withdrawal
    first_input_timestamp = None
    for tx in chain_data.get("result", []):
        if tx.get("to", "").lower() == address.lower():
            first_input_timestamp = int(tx.get("timeStamp", 0))
            break

    output_48hr = []
    if first_input_timestamp:
        for tx in chain_data.get("result", []):
            if tx.get("from", "").lower() == address.lower():
                timestamp = int(tx.get("timeStamp", 0))
                value = int(tx.get("value", 0)) / 1e6
                if timestamp - first_input_timestamp < 172800 and value > 2000:
                    output_48hr.append(value)

    withdrawal_48hr = sum(output_48hr)
    return withdrawal_48hr 

def volume_gap(activity_data):
    if not activity_data:
        return 0
    df_1 = pd.json_normalize(activity_data)
    if 'side' not in df_1.columns:
        return 0
    total_trades = float(df_1[df_1['side'] == 'BUY']['usdcSize'].sum())
    return total_trades

def volume_gap_risk(total_trades):
    if total_trades > 100000:
        return "extreme risk"
    elif total_trades > 75000:
        return "very high risk"
    elif total_trades > 50000:
        return "high risk"
    elif total_trades > 25000:
        return "medium risk"
    elif total_trades > 10000:
        return "low risk"
    else:
        return "minimal risk"

def chain_gap_risk(withdrawal_48hr, sum_input_48hr):
    result = ''
    if sum_input_48hr > 100000 and withdrawal_48hr > 100000:
        result = "extreme risk"
    elif sum_input_48hr > 75000 and withdrawal_48hr > 75000:
        result = "very high risk"
    elif sum_input_48hr > 50000 and withdrawal_48hr > 50000:
        result = "high risk"
    elif sum_input_48hr > 25000 and withdrawal_48hr > 25000:
        result = "medium risk"
    elif sum_input_48hr > 10000 and withdrawal_48hr > 10000:
        result = "low risk"
    else:        
        result = "minimal risk"
    return result
    
def analyse_top_activity(top_activity_data, top_3_event_slug):
    df_1 = pd.json_normalize(top_activity_data[0]) if len(top_activity_data) > 0 and top_activity_data[0] else pd.DataFrame()
    df_2 = pd.json_normalize(top_activity_data[1]) if len(top_activity_data) > 1 and top_activity_data[1] else pd.DataFrame()
    df_3 = pd.json_normalize(top_activity_data[2]) if len(top_activity_data) > 2 and top_activity_data[2] else pd.DataFrame()

    event_1 = top_3_event_slug[0] if len(top_3_event_slug) > 0 else None
    event_2 = top_3_event_slug[1] if len(top_3_event_slug) > 1 else None
    event_3 = top_3_event_slug[2] if len(top_3_event_slug) > 2 else None

    total_1 = float(df_1[df_1['eventSlug'] == event_1]['usdcSize'].sum()) if 'eventSlug' in df_1.columns else 0
    total_2 = float(df_2[df_2['eventSlug'] == event_2]['usdcSize'].sum()) if 'eventSlug' in df_2.columns else 0
    total_3 = float(df_3[df_3['eventSlug'] == event_3]['usdcSize'].sum()) if 'eventSlug' in df_3.columns else 0

    return total_1, total_2, total_3

def analyse_top_activity_risk(total_1, total_2, total_3):
    sum_total = total_1 + total_2 + total_3
    active = 0
    if total_1 > 5000:
        active = active + 1
    if total_2 > 5000:
        active = active + 1
    if total_3 > 5000:
        active = active + 1

    if sum_total > 100000 and active == 3:
        return "extreme risk"
    elif sum_total > 75000 and active >= 2:   
        return "very high risk"
    elif sum_total > 50000 and active >= 1:
        return "high risk"
    elif sum_total > 25000 and active >= 1:
        return "medium risk"
    elif sum_total > 10000 and active >= 1:
        return "low risk"          
    else:
        return "minimal risk"



        
    





   #value > 5000 indicates that it is a withdrawal to a hot wallet or a GSN, rather than a new txn or trade. This is to avoid flagging users who make a large deposit, but then make a few small trades, which is not necessarily suspicious.
    # results = ""
    # if sum(input_data_48) > 50000  and (sum(output_48hr) > 50000 or len(output_48hr) > 10):
    #     results = "high risk"
    # elif sum(input_data_48) > 25000 and (sum(output_48hr) > 25000 or len(output_48hr) > 5):
    #     results = 'medium risk'
    # elif sum(input_data_48) > 10000 and (sum(output_48hr) > 10000 or len(output_48hr) > 2):
    #     results = 'low risk'
    # else:        
    #     results = 'minimal risk'

    # return results, sum(output_48hr)
            

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("polyfetch:app", host="0.0.0.0", port=port)
