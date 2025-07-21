-- V1_initial_startup.sql
-- Initial schema setup for NOAA pipeline database
-- Timestamp: YYYY-MM-DD (replace with actual date)

CREATE TABLE IF NOT EXISTS pmn_weekly (
    week_start DATE NOT NULL,
    avg_pmn_count FLOAT NOT NULL,
    avg_water_temp FLOAT NOT NULL,
    avg_salinity FLOAT NOT NULL,
    measurement_count INT NOT NULL,
    PRIMARY KEY (week_start)
);

CREATE TABLE IF NOT EXISTS climate_weekly (
    week_start DATE NOT NULL,
    avg_temperature_anomaly FLOAT NOT NULL,
    PRIMARY KEY (week_start)
);

CREATE TABLE IF NOT EXISTS chlorophyll_weekly (
    week_start DATE NOT NULL,
    avg_chlorophyll_a FLOAT NOT NULL,
    PRIMARY KEY (week_start)
);

CREATE TABLE IF NOT EXISTS buoy_weekly (
    week_start DATE NOT NULL,
    avg_wave_height FLOAT NOT NULL,
    avg_sst FLOAT NOT NULL,
    avg_air_temp FLOAT NOT NULL,
    avg_atm_pressure FLOAT NOT NULL,
    PRIMARY KEY (week_start)
);

-- Indexes (for performance optimization)
CREATE INDEX IF NOT EXISTS idx_pmn_week ON pmn_weekly (week_start);
CREATE INDEX IF NOT EXISTS idx_climate_week ON climate_weekly (week_start);
CREATE INDEX IF NOT EXISTS idx_chlorophyll_week ON chlorophyll_weekly (week_start);
CREATE INDEX IF NOT EXISTS idx_buoy_week ON buoy_weekly (week_start);
