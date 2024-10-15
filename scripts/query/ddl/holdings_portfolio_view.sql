CREATE VIEW finance.holdings_portfolio_view AS
(
    SELECT a.business_date,
           a.portfolio_id,
           a.security_id,
           a.exchange,
           a.quantity,
           a.market_value,
           a.currency,
           b.nav,
           b.daily_pnl,
           b.ytd_return,
           b.sharpe_ratio,
           b.volatility,
           b.var_95
    FROM finance.holdings a
    INNER JOIN finance.portfolio b
    ON a.business_date = b.business_date
    AND a.portfolio_id = b.portfolio_id
);