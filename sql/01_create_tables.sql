CREATE TABLE IF NOT EXISTS raw_fx_rates (
    date DATE NOT NULL,
    base VARCHAR(3) NOT NULL,
    quote VARCHAR(3) NOT NULL,
    rate NUMERIC(18, 6) NOT NULL,
    loaded_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (date, base, quote)
);

CREATE INDEX IF NOT EXISTS idx_raw_fx_rates_date ON raw_fx_rates (date);