import csv
from datetime import datetime
from time import sleep

import requests

import kb_2315_2.config as config
from kb_2315_2.csv.io import create_csv
from kb_2315_2.sensor import envirionment_sensor


url: str = f"http://{config.read_config(dir=config.root_dir).client_ip}/data"

with open(create_csv(), "w") as f:
    writer = csv.writer(f)

    while True:
        response = requests.get(url)

        d = response.json()

        dh: list[envirionment_sensor] = []

        val: list[datetime | float] = [datetime.now()]

        for k, v in d.items():
            dh.append(envirionment_sensor().model_validate_json(v))

        for d in dh:
            val.append(d.temperature)
            val.append(d.humidity)
            val.append(d.pressure if d.pressure is not None else 0.0)

        writer.writerow(val)
        print("get")
        sleep(10)
