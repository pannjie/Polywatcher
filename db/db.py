import os
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

engine = sa.create_engine(os.getenv("DATABASE_URL"), echo=True)
connection = engine.connect()
metadata = sa.MetaData()

wallets_table = sa.Table(
    'wallets',
    metadata,
    sa.Column('rank', sa.String, primary_key=True),
    sa.Column('username', sa.String, unique=True, nullable=True),
    sa.Column('proxywallet', sa.String, unique=True, nullable=True),
    sa.Column('pnl', sa.Float, nullable=True),
    sa.Column('vol', sa.Float, nullable=True),
    sa.Column('Market Spread', sa.Float, nullable=True),
    sa.Column('Wallet Age', sa.Float, nullable=True),
    sa.Column('Creation/Cashout Gap', sa.Float, nullable=True),
    sa.Column('Creation/Volume', sa.Float, nullable=True),
    sa.Column('Success Rate', sa.Float, nullable=True),
    sa.Column('Position Size', sa.Float, nullable=True),
    sa.Column('24h Deposits', sa.Float, nullable=True),
    sa.Column('AI Similarity Score', sa.Float, nullable=True) 
)

def insert_wallet(rank, username, proxywallet, pnl, vol,
                  market_spread=None, wallet_age=None, cashout_gap=None,
                  creation_volume=None, success_rate=None, position_size=None,
                  deposits_24h=None, ai_similarity=None) -> None:
    values = {
        "rank": rank, "username": username, "proxywallet": proxywallet,
        "pnl": pnl, "vol": vol,
        "Market Spread": market_spread, "Wallet Age": wallet_age,
        "Creation/Cashout Gap": cashout_gap, "Creation/Volume": creation_volume,
        "Success Rate": success_rate, "Position Size": position_size,
        "24h Deposits": deposits_24h, "AI Similarity Score": ai_similarity,
    }
    query = sa.dialects.postgresql.insert(wallets_table).values(**values)
    query = query.on_conflict_do_update(index_elements=['rank'], set_=values)
    connection.execute(query)
    connection.commit()

    

def get_wallets():
    result = connection.execute(wallets_table.select())
    return [{"rank": row.rank, "proxywallet": row.proxywallet} for row in result]

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Tables created.")
