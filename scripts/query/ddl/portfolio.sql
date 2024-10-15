CREATE TABLE IF NOT EXISTS finance.portfolio
(
    business_date timestamp without time zone,
    portfolio_id text,
    nav double precision,
    daily_pnl double precision,
    ytd_return double precision,
    sharpe_ratio double precision,
    volatility double precision,
    var_95 double precision,
    PRIMARY KEY (business_date, portfolio_id, nav, daily_pnl, ytd_return)
);