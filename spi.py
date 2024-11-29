import pandas as pd
import numpy as np


def spi_calculator(file_path):

    df = pd.read_csv(file_path)
    station_annual_precip = df.groupby("station")["value"].sum().reset_index()

    station_annual_precip["mean"] = df.groupby("station")["value"].transform("mean")
    station_annual_precip["std"] = df.groupby("station")["value"].transform("std")
    station_annual_precip["SPI"] = (
        station_annual_precip["value"] - station_annual_precip["mean"]
    ) / station_annual_precip["std"]
    station_annual_precip["SPI"] = station_annual_precip["SPI"].replace(
        [np.inf, -np.inf, np.nan], 0
    )

    # station_annual_precip.to_csv("spi_results.csv", index=False)
    return station_annual_precip[["station", "SPI"]]
