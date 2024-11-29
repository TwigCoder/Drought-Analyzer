import plotly.graph_objects as go
import pandas as pd


def plot_map(spi_df, station_coords_df):

    min_spi = -2
    max_spi = 2

    combined_df = pd.merge(
        station_coords_df, spi_df, left_on="station_id", right_on="station", how="inner"
    )
    combined_df["SPI_normalized"] = combined_df["SPI"].apply(
        lambda x: max(min(x, max_spi), min_spi)
    )
    combined_df["SPI_rounded"] = combined_df["SPI"].round(2)

    fig = go.Figure(
        data=[
            go.Scattergeo(
                lon=combined_df["longitude"],
                lat=combined_df["latitude"],
                text=combined_df["station_id"]
                + "<br>SPI: "
                + combined_df["SPI_rounded"].astype(str),
                hoverinfo="text",
                mode="markers",
                marker=dict(
                    size=8,
                    color=combined_df["SPI_normalized"],
                    colorscale="RdYlBu",
                    cmin=min_spi,
                    cmax=max_spi,
                    colorbar=dict(
                        title="SPI Index",
                        tickvals=[-2, -1, 0, 1, 2],
                        ticktext=["Very Dry", "Dry", "Neutral", "Wet", "Very Wet"],
                    ),
                    opacity=0.7,
                    line=dict(width=0.5, color="black"),
                ),
            )
        ],
        layout=go.Layout(
            geo=dict(
                showland=True,
                landcolor="lightgray",
                projection_type="orthographic",
                showcountries=True,
                countrycolor="black",
                lakecolor="white",
                projection_scale=1.6,
                showcoastlines=True,
                coastlinecolor="gray",
            ),
            title="Global 3D Globe with SPI Index",
            title_x=0.5,
            geo_projection_rotation=dict(lon=0, lat=0),
            template="plotly_white",
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
        ),
    )

    fig.show()
