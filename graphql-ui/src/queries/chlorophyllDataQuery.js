import { gql } from "@apollo/client";

export const GET_CHLOROPHYLL_DATA = gql`
  query GetChlorophyllData(
    $startDate: DateTime!,
    $endDate: DateTime!,
    $limit: Int!
  ) {
    getChlorophyllData(startDate: $startDate, endDate: $endDate, limit: $limit) {
      time
      latitude
      longitude
      chlorophyllA
    }
  }
`;
