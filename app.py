"""Crypto Interview Assessment Module."""

# from models import db, Purchases, Portfolios, Top_Cryptos
from datetime import datetime
import crypto_api as ca
import time
import sched
import os
import logging
import psycopg2

from dotenv import find_dotenv, load_dotenv, dotenv_values

GLOBAL_CHECK_TIME = datetime.time(datetime.now())

# connect_db(app)

# This will allow us to log the results of trades.
logging.basicConfig(filename='storage/logs/app.log',
                    encoding='utf-8', level=logging.DEBUG)

config = dotenv_values(".env")

os.getenv("DB_HOST")

load_dotenv(find_dotenv(raise_error_if_not_found=True))

# this will allow you to call a scheduler in any function you want to schedule
# as this app runs automatically, it requires functions to be scheduled
s = sched.scheduler(time.time, time.sleep)

# You can access the environment variables as such,
# and any variables from the .env file will be loaded in for you to use.
# os.getenv("DB_HOST")


def initialize_portfolio():
    '''Starts the app with a new portfolio'''

    # new_portfolio = Portfolios.create_portfolio()
    # db.session.add(new_portfolio)
    # db.session.commit()
    print("New portfolio created")


def hour_check(sc):
    '''Automated function that checks the prices and returns data for the top 3 coins'''

    try:
        check = ca.get_coins()
        top3 = [check[0], check[1], check[2]]

        x = 0
        top3_names = []

        current_date = datetime.date(datetime.now())
        current_time = datetime.time(datetime.now())

        print(
            f"Here are the top 3 cryptos on {current_date} at {current_time}.")

        while x < len(top3):
            top3_names.append(top3[x].get("id"))
            print("Currency: %s" % top3[x].get("id"))
            print("Current Price: %s" % top3[x].get("current_price"))
            print("Average Price: %s" % average_price(f"{top3_names[x]}"))
            # check = Top_Cryptos.create_entry(symbol=top3[x].get("id"), name=top3[x].get(
            #     "id"), current_price=top3[x].get("current_price"), date=current_date, time=current_time)
            # db.session.add(check)
            # db.session.commit()
            if float(average_price(f"{top3_names[x]}")) > float(top3[x].get("current_price")):
                # ca.submit_order(top3_names[x], 1, top3[x].get("current_price"))
                submit_order({top3_names[x]}, 1, top3[x].get("current_price"))
            x += 1

        s.enter(3600, 100, hour_check, (sc,))

    except:
        print(
            f"An error occurred in the hour check function at {GLOBAL_CHECK_TIME}.")


def average_price(coin_id: str):
    '''Automated function that gets the average from the get price history function
    add all the values from a check to a list and average them

    This function takes a string (coin_id) and looks up the price history (past ten prices.

    Then it averages those prices.

    This function should also check against what is already in the portfolio
    and show the gain/losses on the coin'''

    try:

        x = 0
        price_list = []
        coin_history = ca.get_coin_price_history(coin_id)

        while x < len(coin_history):
            price_list.append(coin_history[x][1])
            x += 1

        total = 0

        for n in range(0, len(price_list)):
            total = total + price_list[n]

        average_price = total / len(price_list)

        return average_price

    except:
        print(
            f"An error occured in the average function at {GLOBAL_CHECK_TIME}.")


def submit_order(coin_id: str, qty: int, bid: float):
    '''Submits an order of one unit of a coin and logs it to the log file'''

    try:

        ca.submit_order(coin_id, qty, bid)

        current_date = datetime.date(datetime.now())
        current_time = datetime.time(datetime.now())

        # While submitting an order, check if we already have one of those coins in our portfolio
        # coin_by_id = Purchases.query.get(coin_id)
        # if(coin_by_id):
        #     average_price(coin_id)
        # replace the current_price field with the result of the average price function
        # calculate the difference between current price and average price and replace the gain_loss field with the result

        print(
            f"Submitting order of {coin_id} for {qty} coin at a price of {bid}.")

        # purchase = Purchases.create_line(
        #     coin_id=coin_id, qty=qty, price_at_purchase=bid, current_price=bid gain_loss=0.0)
        # db.session.add(purchase)
        # db.session.commit()

        logging.info(
            f"{qty} of {coin_id} fulfilled at {current_time} on {current_date} at a price of {bid}.")

    except:
        print(
            f"An error occurred in the submit function at {GLOBAL_CHECK_TIME}.")


# Message for when a user loads the app.


print("Welcome to the Crypto Tracker!")
print("Every hour, this app will check the price of the top 3 cryptos and execute an order to buy if the price is lower than the average")

initialize_portfolio()

# if you want to change it from an hour to a day, change 3600 seconds to 86400 seconds
s.enter(3600, 100, hour_check, (s,))
s.run()
