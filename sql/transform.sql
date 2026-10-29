DROP TABLE IF EXISTS mart_fx_daily;


CREATE TABLE mart_fx_daily AS 
WITH daily_rates AS (
    SELECT
        date,
        base,
        quote,
        rate,
        LAG(rate) OVER (
            PARTITION BY base, quote
            ORDER BY date
        ) AS prev_rate
    FROM raw_fx_rates
)
SELECT
    date,
    base,
    quote,
    rate,
    prev_rate,
    -- Изменение курса за день:
    ROUND(rate - prev_rate, 6) AS daily_change, 
    -- Изменение курса за день в %:
    ROUND(
        CASE
            WHEN prev_rate IS NOT NULL AND prev_rate <> 0
            THEN (rate - prev_rate) / prev_rate * 100
            ELSE NULL
        END,
        4
    ) AS daily_change_pct,
    -- Скользящее среднее за 7 дней:
    ROUND(
        AVG(rate) OVER (
            PARTITION BY base, quote
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW 
        ),
        6
    ) AS ma_7d,
    -- Скользящее среднее за 30 дней:
    ROUND(
        AVG(rate) OVER (
            PARTITION BY base, quote
            ORDER BY date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW 
        ),
        6
    ) AS ma_30d
    FROM daily_rates;


    CREATE INDEX IF NOT EXISTS idx_mart_fx_daily_date ON mart_fx_daily(date);

