# File for all classes that are used in the crypto app

import sqlalchemy as db
from sqlalchemy import Integer, Column, create_engine, ForeignKey
from sqlalchemy.sql.expression import table
from sqlalchemy.dialects import postgresql
from sqlalchemy.util.langhelpers import symbol
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship, Query
import os

from dotenv import find_dotenv, load_dotenv, dotenv_values

config = dotenv_values(".env")

os.getenv("DB_HOST")

load_dotenv(find_dotenv(raise_error_if_not_found=True))

db_user = config.get('DB_USERNAME')
db_password = config.get('DB_PASSWORD')
db_host = config.get('DB_HOST')
db_port = config.get('DB_PORT')
db_name = config.get('DB_DATABASE')

connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

Base = declarative_base()
engine = db.create_engine(connection_string)

# After creating the engine, you have to run this code to connect it.
# However, this code is causing an unpacking error "error: unpack requires a buffer of 4 bytes"
# I am leaving it commented out while I debug, as well as any session.commit() instances.
# connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

metadata = db.MetaData(bind=engine)
purchases = db.Table('purchases', metadata)
portfolios = db.Table('portfolios', metadata)
top_cryptos = db.Table('top_cryptos', metadata)


class Purchases(Base):
    '''One entry in a portfolio'''

    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coin_id = db.Column(db.String(30), db.ForeignKey(
        'top_cryptos.name'), nullable=False)
    symbol = db.Column(db.String)
    qty = db.Column(db.Float, default=1)
    price_at_purchase = db.Column(db.Float)
    current_price = db.Column(db.Float)
    # gain_loss is the price difference between price_at_purchase and current_price
    gain_loss = db.Column(db.Float, default=0)

    portfolio_id = db.Column(db.Integer, db.ForeignKey('porfolios.id'))

    @classmethod
    def create_line(cls, coin_id, qty, price_at_purchase, current_price, gain_loss):
        line = Purchases(coin_id=coin_id, qty=qty,
                         price_at_purchase=price_at_purchase, gain_loss=0.0)

        # db.session.add(line)
        return line


class Portfolios(Base):
    '''Portfolio of many cryptos'''

    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def create_portfolio(cls):
        portfolio = Portfolios()

        # db.session.add(portfolio)
        return portfolio


class Top_Cryptos(Base):
    '''Log of the top cryptos each hour'''

    __tablename__ = "top_cryptos"

    symbol = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    current_price = db.Column(db.Float)
    date = db.Column(db.String)
    time = db.Column(db.String)

    @classmethod
    def create_entry(cls, symbol, name, current_price, date, time):
        entry = Top_Cryptos(symbol=symbol, name=name,
                            current_price=current_price, date=date, time=time)
        return entry
