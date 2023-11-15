from datetime import datetime
from pathlib import Path
from uuid import uuid4

import kb_2315_2.config as config


conf: config.env = config.read_config(dir=config.root_dir)


def create_csv() -> Path:
    (config.root_dir / "data").mkdir(exist_ok=True)

    filename: str = datetime.now().strftime("%Y%m%d-%H%M%S-") + str(uuid4())[:8]

    while (config.root_dir / "data" / f"{filename}.csv").exists():
        filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + str(uuid4())[:8]

    return config.root_dir / "data" / f"{filename}.csv"
