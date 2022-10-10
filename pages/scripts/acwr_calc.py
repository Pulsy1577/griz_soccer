import sys
from gspread_pandas import Spread, Client
import pandas as pd
import numpy as np
import plotly.express as px
import plotly

# this creates the date range to fill on missing dates
START_DATE = pd.to_datetime("2022-08-02").strftime("%Y-%m-%d")
END_DATE = pd.to_datetime("today").strftime("%Y-%m-%d")
TODAY = pd.to_datetime("today")
TWO_WEEKS_BACK = TODAY - pd.Timedelta(days=14)


def calc_loads(v1, v2):
    return round(v1 * v2, 2)


def start_aewma(load):
    a_alpha = 2 / (7 + 1)
    return round(load * a_alpha, 2)


def start_cewma(load):
    c_alpha = 2 / (28 + 1)
    return round(load * c_alpha, 2)


def calc_aewma(load, p_ewma):
    a_alpha = 2 / (7 + 1)
    a_mod = 1 - a_alpha
    p_aewma = p_ewma
    a_ewma = (load * a_alpha) + (p_aewma * a_mod)
    return round(a_ewma, 2)


def calc_cewma(load, p_ewma):
    a_alpha = 2 / (28 + 1)
    a_mod = 1 - a_alpha
    p_aewma = p_ewma
    c_ewma = (load * a_alpha) + (p_aewma * a_mod)
    return round(c_ewma, 2)


def get_acwr(a_ewma, c_ewma):
    acwr = a_ewma / c_ewma
    return round(acwr, 2)


def merge_data(p_dict):
    # merge all data frames into one
    df = pd.concat(p_dict, ignore_index=True)
    df = df.sort_values(by=["Name", "Date"])
    df = df.reset_index(drop=True)
    return df


def create_acwr(df):
    df["Event Date"] = pd.to_datetime(df["Event Date"])
    df.drop(
        [
            "aEWMAspt",
            "cEWMAspt",
            "acwr_spt",
            "L1_aewma",
            "L1",
            "L2",
            "L1_aewma",
            "L1_cewma",
            "L2_aewma",
            "L2_cewma",
            "acwr_l1",
            "acwr_l2",
            "ACWR_AVG",
        ],
        inplace=True,
        axis=1,
    )

    # create date range (change end to current day)
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
    #
    # create unique list of names
    UniqueNames = df["Player Name"].unique()

    # create a data frame dictionary to store your data frames
    PlayerDict = {elem: pd.DataFrame() for elem in UniqueNames}

    # loop over each name and add data to the dataframe for each name
    for key in PlayerDict.keys():
        PlayerDict[key] = df[:][df["Player Name"] == key]
        PlayerDict[key].set_index("Event Date", inplace=True)
        PlayerDict[key] = (
            PlayerDict[key].groupby(PlayerDict[key].index).sum(numeric_only=True)
        )
        PlayerDict[key] = PlayerDict[key].reindex(date_range, fill_value=0)
        PlayerDict[key].reset_index(inplace=True)
        PlayerDict[key].rename(columns={"index": "Event Date"}, inplace=True)
        PlayerDict[key].insert(1, "Player Name", key)
        PlayerDict[key]["L1"] = calc_loads(PlayerDict[key]["Total_Distance"], 1)
        PlayerDict[key]["L2"] = calc_loads(PlayerDict[key]["Hard_Running"], 1)
        PlayerDict[key]["L1_aewma"] = np.NaN
        PlayerDict[key]["L1_cewma"] = np.NaN
        PlayerDict[key]["L2_aewma"] = np.NaN
        PlayerDict[key]["L2_cewma"] = np.NaN
        PlayerDict[key]["aEWMAspt"] = np.NaN
        PlayerDict[key]["cEWMAspt"] = np.NaN
        PlayerDict[key]["acwr_spt"] = np.NaN
        PlayerDict[key]["acwr_l1"] = np.NaN
        PlayerDict[key]["acwr_l2"] = np.NaN
        PlayerDict[key]["ACWR_AVG"] = np.NaN
        PlayerDict[key].at[0, "aEWMAspt"] = start_aewma(
            PlayerDict[key].at[0, "Load_2D"]
        )
        PlayerDict[key].at[0, "cEWMAspt"] = start_cewma(
            PlayerDict[key].at[0, "Load_2D"]
        )
        PlayerDict[key].at[0, "L1_aewma"] = start_aewma(PlayerDict[key].at[0, "L1"])
        PlayerDict[key].at[0, "L1_cewma"] = start_cewma(PlayerDict[key].at[0, "L1"])
        PlayerDict[key].at[0, "L2_aewma"] = start_aewma(PlayerDict[key].at[0, "L2"])
        PlayerDict[key].at[0, "L2_cewma"] = start_cewma(PlayerDict[key].at[0, "L2"])
        rows = len(PlayerDict[key].index)
        for row in range(1, rows, 1):
            PlayerDict[key].at[row, "aEWMAspt"] = calc_aewma(
                PlayerDict[key].at[row, "Load_2D"],
                PlayerDict[key].at[row - 1, "aEWMAspt"],
            )
            PlayerDict[key].at[row, "cEWMAspt"] = calc_cewma(
                PlayerDict[key].at[row, "Load_2D"],
                PlayerDict[key].at[row - 1, "cEWMAspt"],
            )
            PlayerDict[key].at[row, "L1_aewma"] = calc_aewma(
                PlayerDict[key].at[row, "L1"], PlayerDict[key].at[row - 1, "L1_aewma"]
            )
            PlayerDict[key].at[row, "L1_cewma"] = calc_cewma(
                PlayerDict[key].at[row, "L1"], PlayerDict[key].at[row - 1, "L1_cewma"]
            )
            PlayerDict[key].at[row, "L2_aewma"] = calc_aewma(
                PlayerDict[key].at[row, "L2"], PlayerDict[key].at[row - 1, "L2_aewma"]
            )
            PlayerDict[key].at[row, "L2_cewma"] = calc_cewma(
                PlayerDict[key].at[row, "L2"], PlayerDict[key].at[row - 1, "L2_cewma"]
            )

        PlayerDict[key]["acwr_spt"] = get_acwr(
            PlayerDict[key]["aEWMAspt"], PlayerDict[key]["cEWMAspt"]
        )
        PlayerDict[key]["acwr_l1"] = get_acwr(
            PlayerDict[key]["L1_aewma"], PlayerDict[key]["L1_cewma"]
        )
        PlayerDict[key]["acwr_l2"] = get_acwr(
            PlayerDict[key]["L2_aewma"], PlayerDict[key]["L2_cewma"]
        )
        PlayerDict[key]["ACWR_AVG"] = round(
            PlayerDict[key][["acwr_spt", "acwr_l1", "acwr_l2"]].mean(axis=1), 2
        )
        PlayerDict[key].rename(
            columns={"Event Date": "Date", "Player Name": "Name"}, inplace=True
        )

    merged_data = merge_data(PlayerDict)
    merged_data.to_csv("merged_data.csv", index=False)
    return merged_data


def get_data(spt_df):
    acwr_data = create_acwr(spt_df)
    return acwr_data


def main():
    df = pd.read_csv("Data/soccer_data_10_4.csv")
    new_data = get_data(df)
    print(new_data)


def save_data(p_dict):
    """Save data to csv"""
    for key in p_dict.keys():
        p_dict[key].to_csv(f"{key}.csv", index=False, columns=p_dict[key].columns)


if __name__ == "__main__":
    main()
