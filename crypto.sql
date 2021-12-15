\echo 'Delete and recreate crypto db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE crypto_db;
CREATE DATABASE crypto_db;
\connect crypto_db

CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY 
);

CREATE TABLE top_cryptos (
    symbol VARCHAR,
    name VARCHAR NOT NULL PRIMARY KEY NOT NULL,
    current_price FLOAT NOT NULL,
    date VARCHAR NOT NULL,
    time VARCHAR NOT NULL
);

CREATE TABLE purchases (
    portfolio_id INTEGER REFERENCES portfolios,
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR NOT NULL REFERENCES top_cryptos,
    symbol VARCHAR, 
    qty FLOAT NOT NULL,
    price_at_purchase FLOAT NOT NULL,
    current_price FLOAT NOT NULL, 
    gain_loss FLOAT 
);
