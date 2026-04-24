---
name: Polywatcher project state
description: Architecture, DB setup, Railway deployment, and next steps for Polywatcher
type: project
---

Polywatcher is a FastAPI app (polyfetch.py) that analyses Polymarket wallet addresses for suspicious trading behaviour. Deployed on Railway.

**Why:** Detect potential insider trading / money laundering on Polymarket.

## Stack
- FastAPI + uvicorn on Railway (port 8080)
- PostgreSQL on Railway (internal: postgres.railway.internal:5432, external: shortline.proxy.rlwy.net:31123)
- SQLAlchemy + psycopg2-binary for DB
- HuggingFace InferenceClient for slug similarity embeddings

## DB (db/db.py)
- `wallets` table: rank (String PK), username, proxywallet, vol, pnl (Float)
- Upsert on conflict by rank
- DATABASE_URL loaded from .env locally, from Railway env var in prod

## Venv issue
- Polywatcher/env is misconfigured (pyvenv.cfg points to Polyinsider)
- Fixed with pip.conf in env/ setting target to correct site-packages
- Must use --target or rely on pip.conf for new installs

## Key endpoints
- GET /api/user/{address} — full wallet analysis
- GET /api/leaderboard — fetches Polymarket leaderboard, stores wallets in DB
- GET /api/analyse-leaderboard — PLANNED: batch analysis of all wallets in DB

## Next steps (incomplete)
1. Refactor user_raw() → extract run_analysis(address) as standalone async function
2. Add get_wallets() to db/db.py to query proxywallet addresses
3. Implement /api/analyse-leaderboard endpoint with 2s stagger between calls
4. Fix start_date=None crash in get_activity_2() (no None guard before + 172800)
5. Fix volume_gap() crash on empty dataframe (missing column check)
6. Fix analyse_top_activity() IndexError for wallets with <3 closed positions
7. Consider APScheduler lifespan for daily leaderboard refresh

**How to apply:** When resuming work, start with the run_analysis refactor (step 1) as it unblocks steps 2-3.
