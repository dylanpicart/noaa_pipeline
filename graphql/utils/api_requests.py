import requests
import logging
from graphql import GraphQLError
from requests.exceptions import RequestException, HTTPError, Timeout

logger = logging.getLogger(__name__)

def fetch_data(url, headers=None, timeout=10):
    try:
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        logger.info(f"Successful fetch: {url}")
        return response
    except HTTPError as e:
        status_code = e.response.status_code if e.response else 'Unknown'
        logger.error(f"HTTP error ({status_code}) for URL {url}: {str(e)}")
        raise GraphQLError(f"HTTP error occurred: {status_code}")
    except Timeout:
        logger.error(f"Timeout while fetching URL: {url}")
        raise GraphQLError("Timeout occurred while fetching data.")
    except RequestException as e:
        logger.error(f"Request error for URL {url}: {str(e)}")
        raise GraphQLError("General request error occurred.")

def fetch_pmn_data():
    url = (
        "https://www.ncei.noaa.gov/erddap/tabledap/bedi_PMN.json?"
        "time,latitude,longitude,count,water_temp,salinity"
        "&latitude>=37.7&latitude<=37.8"
        "&longitude>=-122.9&longitude<=-122.7"
        "&.limit=1000"
    )
    response = fetch_data(url)
    data = response.json().get("table", {}).get("rows", [])
    if not data:
        logger.warning("PMN API returned no data.")
        raise GraphQLError("PMN API returned no data.")
    return data

def fetch_buoy_data(station_id):
    url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"
    response = fetch_data(url)
    lines = response.text.splitlines()[2:]
    if not lines:
        logger.warning(f"No buoy data available for station: {station_id}")
        raise GraphQLError("No buoy data available for this station.")
    return lines

def _parse_location_id(location_id):
    if not isinstance(location_id, str):
        logger.error(f"Invalid location_id type: {location_id}")
        raise ValueError("location_id must be a string in the format 'lat,lon'.")
    parts = location_id.split(",")
    if len(parts) != 2:
        logger.error(f"Invalid location_id format: {location_id}")
        raise ValueError("location_id must be in the format 'lat,lon'.")
    try:
        latitude, longitude = map(float, parts)
    except ValueError:
        logger.error(f"location_id contains non-numeric values: {location_id}")
        raise ValueError("location_id must contain valid latitude and longitude numbers.")
    return latitude, longitude

def fetch_climate_data(dataset_id, location_id, start_date, end_date, token):
    headers = {"token": token}
    url = (
        f"https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/"
        f"coords/{dataset_id}/12/0/{start_date}/{end_date}/data.json?coords={location_id}"
    )

    latitude, longitude = _parse_location_id(location_id)

    response = fetch_data(url, headers=headers)
    raw_data = response.json().get("data", [])

    if not raw_data:
        logger.warning("Climate API returned no data.")
        raise GraphQLError("Climate API returned no data.")

    extracted_data = []
    for item in raw_data:
        if "date" not in item or "value" not in item:
            logger.error(f"Malformed climate data: {item}")
            raise ValueError("Malformed climate data: 'date' or 'value' field missing.")
        extracted_data.append({
            "date": item["date"],
            "latitude": latitude,
            "longitude": longitude,
            "temperature_anomaly": item["value"]
        })

    return extracted_data

def fetch_chlorophyll_data(start_date, end_date):
    url = (
        f"https://coastwatch.noaa.gov/erddap/griddap/noaacwNPPN20VIIRSDINEOFDaily.json?"
        f"chlor_a%5B({start_date}T00:00:00Z):({end_date}T23:59:59Z)%5D"
        f"%5B(0)%5D%5B(37.7):(37.8)%5D%5B(-122.9):(-122.7)%5D"
    )

    response = fetch_data(url)
    raw_data = response.json().get("table", {}).get("rows", [])

    if not raw_data:
        logger.warning("Chlorophyll API returned no data.")
        raise GraphQLError("Chlorophyll API returned no data.")

    extracted_data = []
    for item in raw_data:
        if len(item) < 4:
            logger.error(f"Malformed chlorophyll data: {item}")
            raise ValueError("Malformed chlorophyll data: expected at least 4 fields.")
        extracted_data.append({
            "time": item[0],
            "latitude": item[1],
            "longitude": item[2],
            "chlorophyll_a": item[3]
        })

    return extracted_data