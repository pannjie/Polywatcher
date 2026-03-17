import os
import datetime
import statistics
import uvicorn
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, status

app = FastAPI()

GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API = "https://data-api.polymarket.com"
GOLDSKY_URL = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn"
POLYGONSCAN_API = "https://api.etherscan.io/v2/api"
# Most likely it's the Goldsky subgraph cold start. The first query to the subgraph takes longer as it warms up. If it exceeds your 30-second timeout, it throws a ReadTimeout, which gets caught by your except Exception and returns an error page. Subsequent queries are faster because the subgraph is already warm.

# You could either increase the timeout or add a simple retry:



@app.get("/")
async def health():
    return {"status": "ok"}

@app.get("/api/user/{address}")
async def user_raw(address: str):
    try:
        creator, activity, positions, closed_positions, redemptions, pnl, chain = await asyncio.gather(
            get_creator(address),
            get_activity(address),
            get_positions(address),
            get_closed_positions(address),
            get_redemptions(address),
            get_pnl(address),
            get_chain(address)
        )

        spread_analysis = analyse_spread(positions, closed_positions)
        spread_risk = analyse_spread_risk(spread_analysis)

        time_gap = get_timegap(redemptions, creator)
        time_gap_risk = get_timegap_risk(time_gap)

        value_redemptions, num_positions = analyse_volume(positions, closed_positions, redemptions)
        volume_risk = analyse_volume_risk(value_redemptions, closed_positions, positions)

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
            "spread_analysis": spread_analysis,
            "spread_risk": spread_risk,
            #2 TIME GAP ANALYSIS
            "time_gap": time_gap,
            "time_gap_risk": time_gap_risk,
            #3 VOLUME ANALYSIS
            "volume_risk": volume_risk,
            "value_redemptions": value_redemptions,
            "num_positions": num_positions,
            #4 PROFIT ANALYSIS
            "total_profit": total_profit,
            "profit_risk": profit_risk,
            #5 SUCCESS RATE ANALYSIS
            "success_rate": success_rate,
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
            "sum_input": sum_input,
            "sum_input_risk": sum_input_risk,

            # BLOCKCHAIN FIRST 48HR ANALYSIS
            "sum_input_48hr": sum_input_48hr,
            "sum_input_48hr_risk": sum_input_48hr_risk,

            # BLOCKCHAIN FIRST 24HR ANALYSIS
            "sum_input_24hr": sum_input_24hr,
            "sum_input_24hr_risk": sum_input_24hr_risk,

            # BLOCKCHAIN GAP ANALYSIS
            "chain_gap": chain_gap_result,
            "chain_output": withdrawal_48hr,

            "chain_raw": chain.get("result", [])
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not fetch data for address {address}. Error: {e}")
    
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


async def get_positions(user, limit=1000):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/positions", params={"user": user, "limit": limit})
        res.raise_for_status()
        return res.json()
    
async def get_closed_positions(user, limit=1000):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_API}/closed-positions", params={"user": user, "limit": limit})
        res.raise_for_status()
        return res.json()


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


#amended to check for all positions, both open and closed.
#amended to avoid over-flagging of normal users.`
##todo: Amend Javascript for better understanding. + %`
def analyse_spread(positions_data, closed_positions):
    event_ids_1 = [position.get('eventId') for position in positions_data]
    event_ids_2 = [position.get('eventId') for position in closed_positions]
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
        total_profit += int(pnl.get("realizedPnl") or 0) / 1e6
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
        if int(pnl.get("realizedPnl") or 0) > 0:
            success += 1
        elif int(pnl.get("realizedPnl") or 0) < 0:
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
            activity.get("timestamp")
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
