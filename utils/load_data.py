import os
import numpy as np
import pandas as pd

def load_events():
    events = pd.read_csv("data/events.csv")
    gp_list = events["Location"].tolist()
    return events, gp_list

def load_drivers():
    drivers = pd.read_csv("data/drivers.csv")
    driver_list = drivers["Abbreviation"].tolist()
    return drivers, driver_list

def load_results():
    results = pd.read_csv("data/results.csv")
    top_drivers = results[results["Position"] <= 3]
    return results, top_drivers

def load_laps(grand_prix: str, selected_drivers: list):
    laps = pd.read_csv("data/laps.csv")
    
    is_selected_gp = laps["Location"] == grand_prix
    is_selected_drivers = laps["Driver"].isin(selected_drivers)

    laps = laps[is_selected_gp & is_selected_drivers]

    return laps


def load_speed_stat(grand_prix: str):
    speed_stat = pd.read_csv("data/max_speed_stat.csv")
    speed_stat = pd.pivot_table(
        speed_stat[speed_stat["Location"] == grand_prix].drop("Location", axis = 1),
        index = "Driver", columns = ["Rank"],
        aggfunc = "max"
    )

    return speed_stat