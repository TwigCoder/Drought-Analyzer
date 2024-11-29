import requests
import pandas as pd
import time


def get_precipitation_data(
    url, headers, start_date, end_date, dataset_id="GHCND", station_id=None
):

    params = {
        "datasetid": dataset_id,
        "datatypeid": "PRCP",
        "startdate": start_date,
        "enddate": end_date,
        "limit": 1000,
    }

    if station_id:
        params["stationid"] = station_id

    url = url[0:41] + "data"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        print("Error: ", response.status_code)
        print(response.text)
        return None


def fetch_global_precipitation(url, headers, start_year, end_year):
    all_data = []

    for year in range(start_year, end_year + 1):

        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        print(f"Fetching data for year: {year}")
        data = get_precipitation_data(url, headers, start_date, end_date)

        if data:
            all_data.extend(data)

        time.sleep(1)

    return all_data


def save_data_to_csv(data, filename="data/precipitation_data.csv"):
    print(f"Saving precipitation data...\n")
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
