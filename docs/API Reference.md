### 🧪 **1. Phytoplankton (PMN dataset)**

*Wave Organ region phytoplankton data:*

```http
https://www.ncei.noaa.gov/erddap/tabledap/bedi_PMN.csv?
time,latitude,longitude,sample_site,water_temp,salinity
&latitude>=37.7&latitude<=37.8
&longitude>=-122.9&longitude<=-122.7
&.limit=1000
```

---

### 🌊 **2. Buoy Data (Wave Organ Buoy 46026)**

*NOAA buoy environmental data (Wave Organ vicinity):*

```http
https://erddap.sensors.ioos.us/erddap/griddap/gov-ndbc-46026.csv
```

*Metadata and query builder:*
[https://erddap.sensors.ioos.us/erddap/info/gov-ndbc-46026/index.html](https://erddap.sensors.ioos.us/erddap/info/gov-ndbc-46026/index.html)

---

### 🌡️ **3. Climate Anomalies (Climate-at-a-Glance)**

*Monthly temperature anomalies for Wave Organ coordinates:*

```http
https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/coords/tavg/land_ocean/12/0/2020-2024/data.json?coords=37.75,-122.84
```

---

### 🛰️ **4. Satellite Chlorophyll-a (VIIRS Daily, NOAA CoastWatch ERDDAP)**

*Daily chlorophyll-a data (working link you provided):*

```http
https://coastwatch.noaa.gov/erddap/griddap/noaacwNPPN20VIIRSDINEOFDaily.csv?
chlor_a[(2023-01-01T00:00:00Z):(2023-01-07T23:59:59Z)][(0)]
[(37.7):(37.8)][(-122.9):(-122.7)]
```
