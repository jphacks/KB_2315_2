import requests

import kb_2315_2.config as config
from kb_2315_2.sensor import envirionment_sensor


def parser(
    url: str = f"http://{config.read_config(dir=config.root_dir).client_ip}/data",
) -> dict[str, envirionment_sensor] | None:
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch sensor data")
        return None

    else:
        ret: dict[str, envirionment_sensor] = {}

        for k, v in response.json().items():
            e: envirionment_sensor = envirionment_sensor().model_validate_json(v)

            ret[k] = e

        return ret
