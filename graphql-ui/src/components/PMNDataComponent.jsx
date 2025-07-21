import React from 'react';
import { useQuery } from "@apollo/client";
import { GET_PMN_DATA } from "../queries/pmnDataQuery";

const PMNDataComponent = () => {
  const { loading, error, data } = useQuery(GET_PMN_DATA, {
    variables: { limit: 100 }
  });

  if (loading) return <p>Loading PMN Data...</p>;
  if (error) return <p>Error loading PMN Data: {error.message}</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>Latitude</th>
          <th>Longitude</th>
          <th>Count (cells/L)</th>
          <th>Water Temp (°C)</th>
          <th>Salinity (PSU)</th>
        </tr>
      </thead>
      <tbody>
        {data.getPmnData.map((item, idx) => (
          <tr key={idx}>
            <td>{new Date(item.time).toLocaleString()}</td>
            <td>{item.latitude}</td>
            <td>{item.longitude}</td>
            <td>{item.count}</td>
            <td>{item.waterTemp}</td>
            <td>{item.salinity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default PMNDataComponent;
