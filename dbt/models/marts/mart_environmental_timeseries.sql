-- models/mart_environmental_timeseries.sql

SELECT 
    pmn.week_start,
    pmn.avg_pmn_count,
    buoy.avg_wave_height,
    buoy.avg_sst,
    climate.avg_temperature_anomaly,
    chloro.avg_chlorophyll_a
FROM {{ ref('pmn_weekly') }} AS pmn
LEFT JOIN {{ ref('buoy_weekly') }} AS buoy ON pmn.week_start = buoy.week_start
LEFT JOIN {{ ref('climate_weekly') }} AS climate ON pmn.week_start = climate.week_start
LEFT JOIN {{ ref('chlorophyll_weekly') }} AS chloro ON pmn.week_start = chloro.week_start;
