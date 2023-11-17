from datetime import datetime
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from kb_2315_2 import sensor

import kb_2315_2.config as config
from kb_2315_2.csv.io import create_csv
from kb_2315_2.func.parser import parser
from kb_2315_2.sensor import envirionment_sensor


colors: list[str] = px.colors.qualitative.Plotly


class sampler:
    def __init__(self) -> None:
        self.file_name: str = create_csv()
        self.dataframe: pd.DataFrame | None = None
        self.figure: go.Figure | None = None

    def _write_to_csv(self) -> None:
        if self.dataframe is not None:
            self.dataframe.to_csv(config.root_dir / "data" / f"{self.file_name}.csv")

    def sampler(self) -> None:
        sensors: dict[str, envirionment_sensor] | None = parser()

        if sensors is not None:
            keys: list[str] = sorted(sensors.keys())

            if self.dataframe is None:
                cols: list[str] = []
                for name in keys:
                    cols += [f"{name}_temperature", f"{name}_humidity", f"{name}_pressure"]
                self.dataframe = pd.DataFrame(columns=cols)

            val = []

            for name in keys:
                val += [sensors[name].temperature, sensors[name].humidity, sensors[name].pressure]
            self.dataframe.loc[datetime.now().strftime("%Y/%m/%d-%H:%M:%S")] = val
            self._write_to_csv()
