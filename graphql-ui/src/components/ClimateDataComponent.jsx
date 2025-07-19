import React from 'react';
import { useQuery } from "@apollo/client";
import { GET_CLIMATE_DATA } from "../queries/climateDataQuery";

const ClimateDataComponent = ({ datasetId, locationId, startDate, endDate }) => {
  const { loading, error, data } = useQuery(GET_CLIMATE_DATA, {
    variables: { datasetId, locationId, startDate, endDate, limit: 100 }
  });

  if (loading) return <p>Loading Climate Data...</p>;
  if (error) return <p>Error loading Climate Data: {error.message}</p>;

  return (
    <div>
      {data.getClimateData.map(item => (
        <div key={item.date + item.datatype}>
          <p><strong>Date:</strong> {item.date}</p>
          <p><strong>Type:</strong> {item.datatype}</p>
          <p><strong>Value:</strong> {item.value}</p>
          <p><strong>Station:</strong> {item.station}</p>
          <p><strong>Attributes:</strong> {item.attributes}</p>
        </div>
      ))}
    </div>
  );
};

export default ClimateDataComponent;
