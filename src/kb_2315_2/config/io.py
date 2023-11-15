from dataclasses import asdict
from pathlib import Path

import toml

from kb_2315_2 import config


root_dir: Path = Path(__file__).parents[3]


def read_config(
    dir: Path = root_dir,
    name: str = "config.toml",
) -> config.env:
    file: Path = dir / name

    if not file.exists():
        write_config(conf=config.env())
        raise FileNotFoundError(f"Config file {file} not found")
    else:
        with file.open() as f:
            return config.env(**toml.loads(f.read()))


def write_config(
    conf: config.env,
    dir: Path = root_dir,
    name: str = "config.toml",
) -> None:
    file: Path = dir / name

    with file.open("w") as f:
        f.write(toml.dumps(asdict(conf)))


conf: config.env = read_config()
