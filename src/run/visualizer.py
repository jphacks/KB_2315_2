from typing import Any

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots

from kb_2315_2.func.data_sampler import sampler


colors: list[str] = px.colors.qualitative.Plotly


s = sampler()

app = Dash(__name__)
app.layout = html.Div(
    html.Div(
        [
            html.H4(f"Realtime Sensor Viewer: {s.file_name}"),
            dcc.Graph(id="live-update-graph", style={"width": "100vw", "height": "90vh"}),
            dcc.Interval(
                id="interval-component",
                interval=5 * 1000,  # ミリ秒ごとに更新
                n_intervals=1000,  # 更新回数
            ),
        ]
    )
)


@callback(Output("live-update-graph", "figure"), Input("interval-component", "n_intervals"))
def update_graph_live(n: Any) -> Figure | None:
    s.sampler()
    if s.dataframe is None:
        return None
    else:
        cols = s.dataframe.columns.tolist()
        ins = s.dataframe.index.tolist()

        fig: Figure = make_subplots(
            rows=3,
            cols=1,
            subplot_titles=("Temperature", "Humidity", "Pressure"),
            shared_xaxes=True,
        )

        for i, co in enumerate([col for col in cols if "temperature" in col]):
            fig.add_trace(
                go.Scatter(x=ins, y=s.dataframe[co], name=co.split("_")[0], line=dict(color=colors[i])),
                row=1,
                col=1,
            )

        for i, co in enumerate([col for col in cols if "humidity" in col]):
            fig.add_trace(
                go.Scatter(x=ins, y=s.dataframe[co], name=co.split("_")[0], line=dict(color=colors[i])),
                row=2,
                col=1,
            )

        for i, co in enumerate([col for col in cols if "pressure" in col]):
            fig.add_trace(
                go.Scatter(x=ins, y=s.dataframe[co], name=co.split("_")[0], line=dict(color=colors[i])),
                row=3,
                col=1,
            )

        return fig


if __name__ == "__main__":
    app.run(debug=False)
