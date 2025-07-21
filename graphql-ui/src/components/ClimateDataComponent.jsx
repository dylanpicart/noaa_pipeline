import React from 'react';
import { useQuery } from '@apollo/client';
import { GET_CLIMATE_DATA } from '../queries/climateDataQuery';

const ClimateDataComponent = ({ datasetId, locationId, startDate, endDate }) => {
  const { loading, error, data } = useQuery(GET_CLIMATE_DATA, {
    variables: { datasetId, locationId, startDate, endDate, limit: 100 }
  });

  if (loading) return <p>Loading climate data...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Latitude</th>
          <th>Longitude</th>
          <th>Temperature Anomaly (°C)</th>
        </tr>
      </thead>
      <tbody>
        {data.getClimateData.map((item, idx) => (
          <tr key={idx}>
            <td>{new Date(item.date).toLocaleDateString()}</td>
            <td>{item.latitude}</td>
            <td>{item.longitude}</td>
            <td>{item.temperatureAnomaly}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ClimateDataComponent;
