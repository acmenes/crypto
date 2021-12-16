\echo 'Delete and recreate crypto db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE crypto;
CREATE DATABASE crypto;
\connect crypto

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


