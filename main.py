from api import return_api_key
import scraper, stations, spi, mapper
import pandas as pd

API_KEY = return_api_key()
headers = {"token": API_KEY}
prec_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datacategories"

print("Starting data fetch...\n")
print("Fetching precipitation data...")
data = scraper.fetch_global_precipitation(prec_url, headers, 1980, 2022)
print("\n")

if data:
    scraper.save_data_to_csv(data)
else:
    assert False, "Error fetching precipitation data"

print("Fetching station coordinates...\n")
stations.fetch_station_coordinates(
    "data/precipitation_data.csv",
    headers,
)
print("\n")

print("Reading data...\n")
spi_df = spi.spi_calculator("data/precipitation_data.csv")
station_df = pd.read_csv("data/station_coordinates.csv")

print("Plotting data...\n")
mapper.plot_map(spi_df, station_df)
