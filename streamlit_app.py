import os
import re
import duckdb
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
from utils.load_data import load_events, load_drivers, load_results, load_laps

st.set_page_config(layout = "wide")

events, gp_list = load_events()
drivers, driver_list = load_drivers()
results, top_drivers = load_results()

with st.sidebar:
    st.title("Grand Prix Selection")
    grand_prix = st.selectbox(
        label = "Grand Prix",
        options = gp_list
    )

    default_drivers = top_drivers[top_drivers["Location"] == grand_prix]["Abbreviation"].tolist()

    selected_drivers = st.multiselect(
        label = "Driver",
        options = driver_list,
        default = default_drivers
    )

event_name = events[events["Location"] == grand_prix]["OfficialEventName"].values[0]

st.title(f"🏁 {event_name}")

driver_colors = {row["Abbreviation"]: row["TeamColor"] for _, row in drivers.iterrows()}
driver_linestyles = {row["Abbreviation"]: "solid" for _, row in drivers.iterrows() if row["linestyle"] == "-"}

st.markdown("## 🏆 Podium")
podium = st.columns(3)

driver_pos = [row["Abbreviation"] for _, row in top_drivers[top_drivers["Location"] == grand_prix].iterrows()]

podium[0].metric("🥈 2nd Position", driver_pos[1], "18 Points", border=True, chart_type = "bar")
podium[1].metric("🏆 1st Position", driver_pos[0], "25 Points", border=True, chart_type = "bar")
podium[2].metric("🥉 3rd Position", driver_pos[2], "15 Points", border=True, chart_type = "bar")