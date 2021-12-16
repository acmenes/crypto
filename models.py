# File for all classes that are used in the crypto app

from os import curdir
import sqlalchemy as db
from sqlalchemy import Integer, Column, create_engine, ForeignKey
from sqlalchemy.sql.expression import table
from sqlalchemy.dialects import postgresql
from sqlalchemy.util.langhelpers import symbol

engine = db.create_engine(
    'postgresql://postgres:H%40L!M@localhost:3360/crypto')
connection = engine.connect()
metadata = db.MetaData()
purchases = db.Table('purchases', metadata)
portfolios = db.Table('portfolios', metadata)
top_cryptos = db.Table('top_cryptos', metadata)


class Purchases(db.Model):
    '''One entry in a portfolio'''

    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coin_id = db.Column(db.String(30), db.ForeignKey(
        top_cryptos.name), nullable=False)
    symbol = db.Column(db.String)
    qty = db.Column(db.Float, default=1)
    price_at_purchase = db.Column(db.Float)
    current_price = db.Column(db.Float)
    # gain_loss is the price difference between price_at_purchase and current_price
    gain_loss = db.Column(db.Float, default=0)

    portfolio_id = db.Relationship('Portfolio')

    @classmethod
    def create_line(cls, coin_id, qty, price_at_purchase, gain_loss):
        line = Purchases(coin_id=coin_id, qty=qty,
                         price_at_purchase=price_at_purchase, gain_loss=0.0)

        db.session.add(line)
        return line


class Portfolios(db.Model):
    '''Portfolio of many cryptos'''

    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def create_portfolio(cls):
        portfolio = Portfolios()

        db.session.add(portfolio)
        return portfolio


class Top_Cryptos(db.Model):
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


def connect_db(app):
    '''Connect to the app'''

    db.app = app
    db.init_app(app)
