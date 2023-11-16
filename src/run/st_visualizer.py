from operator import contains
from pathlib import Path
from time import sleep
from typing import Any

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots

from kb_2315_2.func.data_sampler import sampler
import kb_2315_2.config as config

import pandas as pd
import streamlit as st

colors: list[str] = px.colors.qualitative.Plotly
file_list: list[str] = [f.name for f in (config.root_dir / "data").iterdir() if f.suffix.lower() == ".csv"]

st.set_page_config(
    page_title="Real-Time Sensor Viewer",
    layout="wide",
)

# Sidebar

st.sidebar.title("Analyze")

st.sidebar.subheader("Select a DataSource")
st.session_state.file_name = st.sidebar.selectbox("file name", file_list)

# main

st.subheader("Temperature")
plhT = st.empty()

st.subheader("Humidity")
plhH = st.empty()

st.subheader("Pressure")
plhP = st.empty()


while True:
    if st.session_state.file_name is None:
        pass
    else:
        df = pd.read_csv(config.root_dir / "data" / st.session_state.file_name)

        cols = df.columns.tolist()

        figT = go.Figure()
        for i, co in enumerate([col for col in cols if "temperature" in col]):
            figT.add_trace(
                go.Scatter(x=df["Unnamed: 0"], y=df[co], name=co.split("_")[0], line=dict(color=colors[i])),
            )

        figH = go.Figure()
        for i, co in enumerate([col for col in cols if "humidity" in col]):
            figH.add_trace(
                go.Scatter(x=df["Unnamed: 0"], y=df[co], name=co.split("_")[0], line=dict(color=colors[i])),
            )

        figP = go.Figure()
        for i, co in enumerate([col for col in cols if "pressure" in col]):
            figP.add_trace(
                go.Scatter(x=df["Unnamed: 0"], y=df[co], name=co.split("_")[0], line=dict(color=colors[i])),
            )

        plhT.plotly_chart(figT, use_container_width=True)
        plhH.plotly_chart(figH, use_container_width=True)
        plhP.plotly_chart(figP, use_container_width=True)

    sleep(3)
