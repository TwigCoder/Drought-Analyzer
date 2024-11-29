import requests
import pandas as pd
import csv


def get_station_coordinates(headers, station_id):

    stations_url = f"https://www.ncdc.noaa.gov/cdo-web/api/v2/stations/{station_id}"

    response = requests.get(stations_url, headers=headers)

    if response.status_code == 200:
        try:
            station_data = response.json()

            lat = station_data.get("latitude")
            lon = station_data.get("longitude")

            if lat is not None and lon is not None:
                print(f"Fetching data for station: {station_data.get('name')}")
                return lat, lon
            else:
                print(f"Error: Latitude or longitude missing for station {station_id}")
                return None, None
        except ValueError as err:
            print(f"Error parsing JSON for station {station_id}: {err}")
            return None, None
    else:
        print(
            f"Error fetching data for station {station_id}, Status code: {response.status_code}"
        )
        return None, None


def fetch_station_coordinates(
    input_file, headers, output_file="data/station_coordinates.csv"
):

    station_df = pd.read_csv(input_file)

    station_ids = station_df["station"].unique()

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["station_id", "latitude", "longitude"])

        for station_id in station_ids:
            lat, lon = get_station_coordinates(headers, station_id)
            if lat is not None and lon is not None:
                writer.writerow([station_id, lat, lon])
