import { gql } from "@apollo/client";

export const GET_PMN_DATA = gql`
  query GetPMNData($limit: Int!) {
    getPmnData(limit: $limit) {
      time
      altitude
      latitude
      longitude
      fluorescence
    }
  }
`;
