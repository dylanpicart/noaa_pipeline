-- PMN Weekly Data
CREATE TABLE IF NOT EXISTS pmn_weekly (
    week_start DATE PRIMARY KEY,
    avg_pmn_count FLOAT,
    avg_water_temp FLOAT,
    avg_salinity FLOAT,
    measurement_count INT
);

-- Climate Weekly Data
CREATE TABLE IF NOT EXISTS climate_weekly (
    week_start DATE PRIMARY KEY,
    avg_temperature_anomaly FLOAT
);

-- Chlorophyll Weekly Data
CREATE TABLE IF NOT EXISTS chlorophyll_weekly (
    week_start DATE PRIMARY KEY,
    avg_chlorophyll_a FLOAT
);

-- Buoy Weekly Data
CREATE TABLE IF NOT EXISTS buoy_weekly (
    week_start DATE PRIMARY KEY,
    avg_wave_height FLOAT,
    avg_sst FLOAT,
    avg_air_temp FLOAT,
    avg_atm_pressure FLOAT
);
