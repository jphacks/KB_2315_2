import glob
import json
import os.path
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

from kb_2315_2.sensor import envirionment_sensor


NUM_SENSORS = 3


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == ("/" + "data"):
            self.do_json_service()

    def do_json_service(self) -> None:
        result_json: dict[str, str] = {}

        for i in range(NUM_SENSORS):
            result_json[f"sensor{i}"] = envirionment_sensor(
                temperature=random.uniform(0, 40),
                humidity=random.uniform(0, 100),
                pressure=random.uniform(900, 1100),
            ).model_dump_json()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result_json).encode("UTF-8"))


PORT = 80

httpd = HTTPServer(("", PORT), Handler)
httpd.serve_forever()
