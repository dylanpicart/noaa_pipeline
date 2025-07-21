import React from 'react';
import { useQuery } from "@apollo/client";
import { GET_BUOY_DATA } from "../queries/buoyDataQuery";

const BuoyDataComponent = ({ stationId }) => {
  const { loading, error, data } = useQuery(GET_BUOY_DATA, {
    variables: { stationId, limit: 100 }
  });

  if (loading) return <p>Loading Buoy Data...</p>;
  if (error) return <p>Error loading Buoy Data: {error.message}</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Wave Height (m)</th>
          <th>SST (°C)</th>
          <th>Air Temp (°C)</th>
          <th>Atmospheric Pressure (hPa)</th>
          <th>Station</th>
        </tr>
      </thead>
      <tbody>
        {data.getBuoyData.map((item, idx) => (
          <tr key={idx}>
            <td>{new Date(item.timestamp).toLocaleString()}</td>
            <td>{item.waveHeight}</td>
            <td>{item.sst}</td>
            <td>{item.airTemp}</td>
            <td>{item.atmosphericPressure}</td>
            <td>{item.station}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default BuoyDataComponent;
