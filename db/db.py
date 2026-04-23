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
    sa.Column('username', sa.String, unique=True, nullable=False),
    sa.Column('proxywallet', sa.String, unique=True, nullable=False),
    sa.Column('pnl', sa.Float, nullable=False),
    sa.Column('vol', sa.Float, nullable=False)
)

def insert_wallet(rank, username, proxywallet, pnl, vol) -> None:
    query = sa.dialects.postgresql.insert(wallets_table).values(rank=rank, username=username, proxywallet=proxywallet, pnl=pnl, vol=vol)
    query = query.on_conflict_do_update(index_elements=['rank'], set_={"username": username, "proxywallet": proxywallet, "pnl": pnl, "vol": vol})
    connection.execute(query)
    connection.commit()

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Tables created.")
