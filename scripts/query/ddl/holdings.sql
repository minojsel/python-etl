CREATE TABLE IF NOT EXISTS finance.holdings
(
    business_date timestamp without time zone,
    portfolio_id text COLLATE pg_catalog."default",
    security_id text COLLATE pg_catalog."default",
    exchange text COLLATE pg_catalog."default",
    quantity double precision,
    market_value double precision,
    currency text COLLATE pg_catalog."default",
    PRIMARY KEY (business_date, portfolio_id, security_id, quantity, market_value)
);