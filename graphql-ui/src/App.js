import React from 'react';
import BuoyDataComponent from './components/BuoyDataComponent';
import PMNDataComponent from './components/PMNDataComponent';
import ClimateDataComponent from './components/ClimateDataComponent';
import ChlorophyllDataComponent from './components/ChlorophyllDataComponent';

function App() {
  return (
    <div className="App">
      <h1>NOAA Data Dashboard</h1>

      <section>
        <h2>🌊 Buoy Data (Wave Organ)</h2>
        <BuoyDataComponent stationId="46026" />
      </section>

      <section>
        <h2>🧪 PMN Data</h2>
        <PMNDataComponent />
      </section>

      <section>
        <h2>🌡️ Climate Data</h2>
        <ClimateDataComponent 
          datasetId="tavg_land_ocean" 
          locationId="37.75,-122.84"
          startDate="2023-01-01"
          endDate="2023-01-31"
        />
      </section>

      <section>
        <h2>🛰️ Chlorophyll-a Data</h2>
        <ChlorophyllDataComponent 
          startDate="2023-01-01"
          endDate="2023-01-07"
        />
      </section>
    </div>
  );
}

export default App;
