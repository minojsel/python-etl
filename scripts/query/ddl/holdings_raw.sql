CREATE TABLE IF NOT EXISTS finance.holdings_raw
(
    business_date timestamp without time zone,
    portfolio_id text,
    security_id text,
    exchange text,
    quantity double precision,
    market_value double precision,
    currency text
);