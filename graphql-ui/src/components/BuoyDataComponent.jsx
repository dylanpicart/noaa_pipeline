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
    <div>
      {data.getBuoyData.map(item => (
        <div key={item.timestamp}>
          <p><strong>Time:</strong> {item.timestamp}</p>
          <p><strong>Wave Height:</strong> {item.waveHeight} m</p>
          <p><strong>Sea Surface Temp:</strong> {item.sst} °C</p>
          <p><strong>Station:</strong> {item.station}</p>
        </div>
      ))}
    </div>
  );
};

export default BuoyDataComponent;
