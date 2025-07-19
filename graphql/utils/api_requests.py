import requests
import logging
from graphql import GraphQLError
from requests.exceptions import RequestException, HTTPError, Timeout

logger = logging.getLogger(__name__)

def fetch_data(url, headers=None, timeout=10):
    try:
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # raises HTTPError for bad responses
        logger.info(f"Successful fetch: {url}")
        return response
    except HTTPError as e:
        logger.error(f"HTTP error ({response.status_code}) for URL {url}: {str(e)}")
        raise GraphQLError(f"HTTP error occurred: {response.status_code}")
    except Timeout:
        logger.error(f"Timeout while fetching URL: {url}")
        raise GraphQLError("Timeout occurred while fetching data.")
    except RequestException as e:
        logger.error(f"Error during request to {url}: {str(e)}")
        raise GraphQLError("General request error occurred.")

def fetch_pmn_data():
    url = (
        "https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMWcflhmday.json?"
        "fluorescence%5B(2024-08-16T12:00:00Z):1:(2024-09-15T12:00:00Z)%5D"
        "%5B(0.0):1:(0.0)%5D%5B(32):1:(49)%5D%5B(235):1:(243)%5D"
    )
    response = fetch_data(url)
    return response.json().get("table", {}).get("rows", [])

def fetch_buoy_data(station_id):
    url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"
    response = fetch_data(url)
    lines = response.text.splitlines()[2:]
    if not lines:
        logger.warning(f"No buoy data available for station: {station_id}")
        raise GraphQLError("No buoy data available for this station.")
    return lines

def fetch_climate_data(dataset_id, location_id, start_date, end_date, token):
    headers = {"token": token}
    url = (
        f"https://www.ncdc.noaa.gov/cdo-web/api/v2/data?"
        f"datasetid={dataset_id}&locationid={location_id}"
        f"&datatypeid=AWND,WDF2,WSF2"
        f"&startdate={start_date}&enddate={end_date}&limit=1000"
    )
    response = fetch_data(url, headers=headers)
    return response.json().get("results", [])
