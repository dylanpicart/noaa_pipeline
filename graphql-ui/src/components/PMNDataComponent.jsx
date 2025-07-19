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
    <div>
      {data.getPmnData.map(item => (
        <div key={item.time}>
          <p><strong>Time:</strong> {item.time}</p>
          <p><strong>Altitude:</strong> {item.altitude} m</p>
          <p><strong>Latitude:</strong> {item.latitude}</p>
          <p><strong>Longitude:</strong> {item.longitude}</p>
          <p><strong>Fluorescence:</strong> {item.fluorescence}</p>
        </div>
      ))}
    </div>
  );
};

export default PMNDataComponent;
