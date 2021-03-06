"""Crypto Interview Assessment Module."""

from models import db, engine, session, Portfolios, Purchases, Top_Cryptos
from datetime import datetime

import crypto_api as ca
import time
import sched
import logging

GLOBAL_HOUR_CHECK = 3600
GLOBAL_DAY_CHECK = 86400

# This will allow us to log the results of trades.
logging.basicConfig(filename='storage/logs/app.log',
                    encoding='utf-8', level=logging.DEBUG)

# this will allow you to call a scheduler in any function you want to schedule
# as this app runs automatically, it requires functions to be scheduled
s = sched.scheduler(time.time, time.sleep)


def initialize_portfolio():
    '''Starts the app with a new portfolio'''

    new_portfolio = Portfolios.create_portfolio()
    # session.add(new_portfolio)
    # session.commit()
    print("New portfolio created")


def auto_check(sc):
    '''Automated function that checks the prices and returns data for the top 3 coins

    If you change the first param in the scheduler, you can run this check as often or as infrequently as you want.'''

    try:
        check = ca.get_coins()
        top3 = [check[0], check[1], check[2]]

        x = 0
        top3_names = []

        current_date = datetime.date(datetime.now())
        current_time = datetime.time(datetime.now())

        print("****************")
        print(
            f"Here are the top 3 cryptos on {current_date} at {current_time}.")

        while x < len(top3):
            top3_names.append(top3[x].get("id"))
            # While checking prices, check if we already have one of those coins in our portfolio
            coin_by_id = session.query(Purchases).filter(
                Purchases.coin_id == top3[x].get("id"))
            # here you would change the coin_by_id current price to match the current price found by this function
            # then you use the current price data to check against the price bought to find the percent difference

            # if coin_by_id:
            #   coin_by_id.current_price = average_price(coin_id)
            #   coin_by_id.gain_loss = ((coin_by_id.price_purchased - current_price) /
            #   ((coin_by_id.price_purchased + current_price) / 2)) * 100

            # to get percent diff:

            # ((value1 - value2) / ((value1 + value2) / 2)) * 100
            # if value 1 is larger it should be displayed positively, if value 2 is larger it should be
            # displayed as a negative

            # replace the current_price field with the result of the average price function
            print("Currency: %s" % top3[x].get("id"))
            print("Current Price: %s" % top3[x].get("current_price"))
            print("Average Price: %s" % average_price(f"{top3_names[x]}"))
            check = Top_Cryptos.create_entry(symbol=top3[x].get("id"), name=top3[x].get(
                "id"), current_price=top3[x].get("current_price"), date=current_date, time=current_time)
            # db.session.add(check)
            # db.session.commit()
            if float(average_price(f"{top3_names[x]}")) > float(top3[x].get("current_price")):
                submit_order({top3_names[x]}, 1, top3[x].get("current_price"))
            x += 1

        s.enter(3, 100, auto_check, (sc,))

    except:
        print("An error occurred in the auto check function.")


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
        print("An error occured in the average function at.")


def submit_order(coin_id: str, qty: int, bid: float):
    '''Submits an order of one unit of a coin and logs it to the log file'''

    try:

        ca.submit_order(coin_id, qty, bid)

        current_date = datetime.date(datetime.now())
        current_time = datetime.time(datetime.now())

        print(
            f"Submitting order of {coin_id} for {qty} coin at a price of {bid}.")

        purchase = Purchases.create_line(
            coin_id=coin_id, qty=qty, price_at_purchase=bid, current_price=bid, gain_loss=0.0)
        # db.session.add(purchase)
        # db.session.commit()
        print("Your purchases were successful!")

        logging.info(
            f"{qty} of {coin_id} fulfilled at {current_time} on {current_date} at a price of {bid}.")

    except:
        print("An error occurred in the submit function.")


# Message for when a user loads the app.


print("Welcome to the Crypto Tracker!")
print("Every hour, this app will check the price of the top 3 cryptos and execute an order to buy if the price is lower than the average")

initialize_portfolio()

# Use GLOBAL_HOUR_CHECK to run an hourly check on prices, and GLOBAL_DAY_CHECK to run a check once per day
s.enter(3, 100, auto_check, (s,))
s.run()
