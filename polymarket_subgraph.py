import requests
import math

GOLDSKY_URL = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn"

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

wallet = "0x9d84ce0306f8551e02efef1680475fc0f1dc1344"

query = """
{
  userPositions(
    where: { user: "%s" }
    first: 500
  ) {
    id
    tokenId
    amount
    avgPrice
    realizedPnl
    totalBought
  }
}
""" % wallet

response = requests.post(
    GOLDSKY_URL,
    json={"query": query},
    timeout=10,
)

positions = response.json()["data"]["userPositions"]

for p in positions:
    print({
        "tokenId": p["tokenId"],
        "amount": int(p["amount"]) / 1e6,
        "avgPrice": int(p["avgPrice"]) / 1e6,
        "realizedPnl": int(p["realizedPnl"]) / 1e6,
        "totalBought": int(p["totalBought"]) / 1e6,
    })