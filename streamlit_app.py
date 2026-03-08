import os
import re
import duckdb
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
from utils.load_data import load_events, load_drivers, load_results, load_laps, load_speed_stat

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
laps = load_laps(grand_prix, selected_drivers)

st.title(f"🏁 {event_name}")

driver_colors = {row["Abbreviation"]: row["TeamColor"] for _, row in drivers.iterrows()}
driver_linestyles = {row["Abbreviation"]: "solid" for _, row in drivers.iterrows() if row["linestyle"] == "-"}

st.markdown("## 🏆 Podium")
podium = st.columns(3)

driver_pos = [row["Abbreviation"] for _, row in top_drivers[top_drivers["Location"] == grand_prix].iterrows()]
driver_data = [
    results[results["Abbreviation"] == driver]["Points"].tolist()
    for driver in driver_pos
]

podium[0].metric("🥈 2nd Position", driver_pos[1], "18 Points", chart_data = driver_data[1], border=True, chart_type = "bar")
podium[1].metric("🏆 1st Position", driver_pos[0], "25 Points", chart_data = driver_data[0], border=True, chart_type = "bar")
podium[2].metric("🥉 3rd Position", driver_pos[2], "15 Points", chart_data = driver_data[2], border=True, chart_type = "bar")

st.markdown("## Position Change during Race")

fig = px.line(
    laps, x = "LapNumber", y = "Position", 
    color = "Driver", color_discrete_map = driver_colors, 
    line_dash = "Driver", line_dash_map = driver_linestyles,
    markers = "o"
)

fig.update_yaxes(range = [20.5, 0.5])

st.plotly_chart(fig)

speed_stat = load_speed_stat(grand_prix)

driver_dict = {row["Driver"]: row["Abbreviation"] for _, row in drivers.iterrows()}
abbreviations = [driver_dict[number] for number in speed_stat.index]

fig = px.imshow(speed_stat, y = abbreviations, text_auto = True, aspect="auto", title = "Race - Top Speed (km/h) for Each Lap")
fig.update_xaxes(showticklabels = False)
st.plotly_chart(fig, theme = None)