-- Merge holdings_raw into holdings table, ensuring no duplicates
WITH deduplicated_raw AS (
    SELECT DISTINCT ON (business_date, portfolio_id, nav, daily_pnl, ytd_return)
        business_date,
        portfolio_id,
        nav,
        daily_pnl,
        ytd_return,
        sharpe_ratio,
        volatility,
        var_95
    FROM finance.portfolio_raw
    ORDER BY business_date, portfolio_id, nav, daily_pnl, ytd_return, sharpe_ratio, volatility, var_95 -- Choose the "latest" or preferred rows to keep in case of duplicates
)
INSERT INTO finance.portfolio (
    business_date,
    portfolio_id,
    nav,
    daily_pnl,
    ytd_return,
    sharpe_ratio,
    volatility,
    var_95
)
SELECT
    business_date,
    portfolio_id,
    nav,
    daily_pnl,
    ytd_return,
    sharpe_ratio,
    volatility,
    var_95
FROM deduplicated_raw
ON CONFLICT (business_date, portfolio_id, nav, daily_pnl, ytd_return)
DO UPDATE SET
    sharpe_ratio = EXCLUDED.sharpe_ratio,
    volatility = EXCLUDED.volatility,
    var_95 = EXCLUDED.var_95;