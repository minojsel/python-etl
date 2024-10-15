-- Merge holdings_raw into holdings table, ensuring no duplicates
WITH deduplicated_raw AS (
    SELECT DISTINCT ON (business_date, portfolio_id, security_id, quantity, market_value)
        business_date,
        portfolio_id,
        security_id,
        exchange,
        quantity,
        market_value,
        currency
    FROM finance.holdings_raw
    ORDER BY business_date, portfolio_id, security_id, quantity, market_value, exchange -- Choose the "latest" or preferred rows to keep in case of duplicates
)
INSERT INTO finance.holdings (
    business_date,
    portfolio_id,
    security_id,
    exchange,
    quantity,
    market_value,
    currency
)
SELECT
    business_date,
    portfolio_id,
    security_id,
    exchange,
    quantity,
    market_value,
    currency
FROM deduplicated_raw
ON CONFLICT (business_date, portfolio_id, security_id, quantity, market_value)
DO UPDATE SET
    exchange = EXCLUDED.exchange,
    currency = EXCLUDED.currency;