import React from 'react';
import { useQuery } from '@apollo/client';
import { GET_CHLOROPHYLL_DATA } from '../queries/chlorophyllDataQuery';

const ChlorophyllDataComponent = ({ startDate, endDate }) => {
  const { loading, error, data } = useQuery(GET_CHLOROPHYLL_DATA, {
    variables: { startDate, endDate, limit: 100 }
  });

  if (loading) return <p>Loading Chlorophyll data...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Latitude</th>
          <th>Longitude</th>
          <th>Chlorophyll-a (mg/m³)</th>
        </tr>
      </thead>
      <tbody>
        {data.getChlorophyllData.map((item, idx) => (
          <tr key={idx}>
            <td>{new Date(item.time).toLocaleString()}</td>
            <td>{item.latitude}</td>
            <td>{item.longitude}</td>
            <td>{item.chlorophyllA}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ChlorophyllDataComponent;
