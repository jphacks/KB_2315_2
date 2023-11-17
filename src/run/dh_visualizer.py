from typing import Any

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots
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
from kb_2315_2.func.data_sampler import sampler

import kb_2315_2.config as config

colors: list[str] = px.colors.qualitative.Plotly
file_list: list[str] = [f.name for f in (config.root_dir / "data").iterdir() if f.suffix.lower() == ".csv"]

s = sampler()

app = Dash(__name__)
app.layout = html.Div(
    html.Div(
        [
            html.H1("Real-Time Sensor Viewer"),
            dcc.Dropdown(
                file_list,
                id="file_select",
                value="file_name",
            ),
            dcc.Graph(id="live-update-graph", style={"width": "100vw", "height": "85vh"}),
            dcc.Interval(
                id="interval-component",
                interval=5 * 1000,  # ミリ秒ごとに更新
                n_intervals=1000,  # 更新回数
            ),
        ]
    )
)


@callback(
    Output("live-update-graph", "figure"), [Input("interval-component", "n_intervals"), Input("file_select", "value")]
)
def update_graph_live(n: Any, value: str) -> Figure | None:
    global file_list
    file_list = [f.name for f in (config.root_dir / "data").iterdir() if f.suffix.lower() == ".csv"]
    fig: Figure = make_subplots(
        rows=3,
        cols=1,
        subplot_titles=("Temperature", "Humidity", "Pressure"),
        shared_xaxes=True,
    )
    try:
        df: pd.DataFrame = pd.read_csv(config.root_dir / "data" / value)

        cols: list[str] = df.columns.tolist()

        for i, co in enumerate([col for col in cols if "temperature" in col]):
            fig.add_trace(
                go.Scatter(x=df["Unnamed: 0"], y=df[co], name=co.split("_")[0], line=dict(color=colors[i])),
                row=1,
                col=1,
            )

        for i, co in enumerate([col for col in cols if "humidity" in col]):
            fig.add_trace(
                go.Scatter(x=df["Unnamed: 0"], y=df[co], name=co.split("_")[0], line=dict(color=colors[i])),
                row=2,
                col=1,
            )

        for i, co in enumerate([col for col in cols if "pressure" in col]):
            fig.add_trace(
                go.Scatter(x=df["Unnamed: 0"], y=df[co], name=co.split("_")[0], line=dict(color=colors[i])),
                row=3,
                col=1,
            )
    except FileNotFoundError:
        pass

    return fig


if __name__ == "__main__":
    app.run(debug=False)
