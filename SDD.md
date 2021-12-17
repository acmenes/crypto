# Crypto Tracker App

## Overview

The Crypto Tracker App is simple- it's a bot that watches crypto prices that automatically fulfills an order when the price of any given crypto is lower than its average. This bot will watch several currencies.

## Authors

Alyssa Menes

## Terminology

"Check" - The action described when the app checks crypto prices each hour. The results from a "check" are logged in a database.

"Movement" - A term describing the comparitive price of the crypto. Did it go up or down compared to the averge of the last ten checks?

"Average Price" - A term describing the average price over the course of ten checks (ten hours).

"Purchase" - Describing the event that takes place if the current crypto price is lower than the average. A purchase is automatically fulfilled by the program for one coin of the currency being checked. eg. The app performs a check for Dogecoin. The average price of Dogecoin over the past ten hours was 21 cents. During a check, the price is 19 cents. An automated function then runs to purchase 1 Dogecoin for 19 cents. 

"Trade Log" - A term describing records kept by the app upon a successful purchase of crypto.

"Portfolio" - A term describing a user's crypto portolfio (the amount of currencies they own)

## Design Flow

The Crypto Tracker App is designed to track cryptocurrency prices (always on the move) every hour. Data from these "checks" is stored in a database. The "movement" is also stored in the database. 

The app is designed to fulfill a purchase for 1 coin upon performing a check that results in an amount that is lower than the average.

## Installing dependencies

In your terminal:
poetry install

## Starting up the databases

docker exec -it db bash
mysql -u root -p
enter the password
\r crypto

There was some trouble using the sql file to seed the database (Error 2, file not found, so run the following commands:)

CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY 
);

CREATE TABLE top_cryptos (
    symbol VARCHAR(3),
    crypto_name VARCHAR(20) PRIMARY KEY,
    current_price FLOAT NOT NULL,
    date VARCHAR(20) NOT NULL,
    time VARCHAR(20) NOT NULL
);

CREATE TABLE purchases (
    portfolio_id INTEGER REFERENCES portfolios,
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(20) NOT NULL REFERENCES top_cryptos,
    symbol VARCHAR(3), 
    qty FLOAT NOT NULL,
    price_at_purchase FLOAT NOT NULL,
    current_price FLOAT NOT NULL, 
    gain_loss FLOAT 
);


## Tech stack

- Python
- PSQL
- SQLAlchemy (ORM for interfacing between PostgreSQL and Python)
- CoinGecko Crypto API
- DBDiagram.io (to design db schema)

## Issues to solve

- When connecting to the provided database using the SQL Pro GUI, this error occurs: MySQL said: Protocol mismatch; server version = 11, client version = 10
- When attempting to connect to my own PostgreSQL database instead using SQLAlchemy, this error occurs: Is the server running locally and accepting connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
- Calculating gain/loss- I created a column for gain/loss in the db. I know how I want to implement this feature (checking the current price of a coin against the price purchased and calculating the difference), but I am feeling blocked by my database issues at the moment.