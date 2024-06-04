import pandas as pd
import numpy as np


def parse_hour(hour_str: str) -> int:
    """Convert hours from "HH_HH" format to single hour int."""
    try:
        return int(hour_str.split("_")[0])
    except Exception:
        return np.nan


def load_data(en_files: list, gp_files: list) -> pd.DataFrame:
    """
    Read data from csv files and group them into one DataFrame.

    Args:
        en_files (str): ***_en.csv files
        gp_files (str): ***_gp.csv files

    Return:
        en_grouped (pd.DataFrame): grouped data from en_files
        gp_grouped (pd.DataFrame): grouped data from gp_files
    """
    en_df_list = []

    for file in en_files:
        en_df = pd.read_csv(file)
        en_df["hours"] = en_df["hours"].apply(parse_hour)
        en_df["datetime"] = pd.to_datetime(en_df[["year", "month", "day", "hours"]])
        en_df_list.append(en_df)
    en_df = pd.concat(en_df_list)
    en_grouped = (
        en_df.groupby(["Warehouse", "cargotype", "traffic_stream", "datetime"])[
            "klk_EN"
        ]
        .sum()
        .reset_index()
    )

    gp_df_list = []
    for file in gp_files:
        gp_df = pd.read_csv(file)
        gp_df["datetime"] = pd.to_datetime(gp_df[["Year", "Month", "Day", "Hour"]])
        gp_df_list.append(gp_df)
    gp_df = pd.concat(gp_df_list)
    gp_grouped = (
        gp_df.groupby(["Warehouse", "Traffic_stream", "datetime"])[
            ["total_count", "total_sum"]
        ]
        .sum()
        .reset_index()
    )

    return en_grouped, gp_grouped
