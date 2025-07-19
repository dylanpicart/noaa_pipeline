import React from 'react';
import BuoyDataComponent from './components/BuoyDataComponent';
import PMNDataComponent from './components/PMNDataComponent';
import ClimateDataComponent from './components/ClimateDataComponent';

function App() {
  return (
    <div className="App">
      <h1>NOAA Data Dashboard</h1>

      <section>
        <h2>Buoy Data</h2>
        <BuoyDataComponent stationId="46042" />
      </section>

      <section>
        <h2>PMN Data</h2>
        <PMNDataComponent />
      </section>

      <section>
        <h2>Climate Data</h2>
        <ClimateDataComponent 
          datasetId="GHCND" 
          locationId="CITY:US390029"
          startDate="2024-01-01"
          endDate="2024-01-31"
        />
      </section>
    </div>
  );
}

export default App;
