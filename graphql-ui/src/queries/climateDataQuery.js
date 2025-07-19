import { gql } from "@apollo/client";

export const GET_CLIMATE_DATA = gql`
  query GetClimateData(
    $datasetId: String!,
    $locationId: String!,
    $startDate: DateTime!,
    $endDate: DateTime!,
    $limit: Int!
  ) {
    getClimateData(
      datasetId: $datasetId,
      locationId: $locationId,
      startDate: $startDate,
      endDate: $endDate,
      limit: $limit
    ) {
      date
      datatype
      value
      station
      attributes
    }
  }
`;
