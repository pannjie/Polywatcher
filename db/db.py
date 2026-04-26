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
    sa.Column('username', sa.String, nullable=True),
    sa.Column('proxywallet', sa.String, nullable=True),
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
    try:
        query = sa.dialects.postgresql.insert(wallets_table).values(**values)
        query = query.on_conflict_do_update(index_elements=['rank'], set_=values)
        connection.execute(query)
        connection.commit()
    except Exception:
        connection.rollback()
        raise

    

def update_wallet_analysis(proxywallet, market_spread=None, cashout_gap=None,
                           creation_volume=None, success_rate=None, position_size=None,
                           deposits_24h=None, ai_similarity=None) -> None:
    try:
        query = wallets_table.update().where(
            wallets_table.c.proxywallet == proxywallet
        ).values(**{
            "Market Spread": float(market_spread) if market_spread is not None else None,
            "Creation/Cashout Gap": float(cashout_gap) if cashout_gap is not None else None,
            "Creation/Volume": float(creation_volume) if creation_volume is not None else None,
            "Success Rate": float(success_rate) if success_rate is not None else None,
            "Position Size": float(position_size) if position_size is not None else None,
            "24h Deposits": float(deposits_24h) if deposits_24h is not None else None,
            "AI Similarity Score": float(ai_similarity) if ai_similarity is not None else None,
        })
        connection.execute(query)
        connection.commit()
    except Exception:
        connection.rollback()
        raise

def get_wallets():
    try:
        connection.rollback()
    except Exception:
        pass
    result = connection.execute(wallets_table.select().order_by(sa.cast(wallets_table.c.rank, sa.Integer)))
    return [
        {
            "rank": row.rank,
            "username": row.username,
            "proxywallet": row.proxywallet,
            "pnl": row.pnl,
            "vol": row.vol,
            "market_spread": row._mapping["Market Spread"],
            "wallet_age": row._mapping["Wallet Age"],
            "cashout_gap": row._mapping["Creation/Cashout Gap"],
            "creation_volume": row._mapping["Creation/Volume"],
            "success_rate": row._mapping["Success Rate"],
            "position_size": row._mapping["Position Size"],
            "deposits_24h": row._mapping["24h Deposits"],
            "ai_similarity": row._mapping["AI Similarity Score"],
        }
        for row in result
    ]

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Tables created.")
