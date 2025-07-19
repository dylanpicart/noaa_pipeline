import { gql } from "@apollo/client";

export const GET_BUOY_DATA = gql`
  query GetBuoyData($stationId: String!, $limit: Int!) {
    getBuoyData(stationId: $stationId, limit: $limit) {
      timestamp
      waveHeight
      sst
      station
    }
  }
`;
