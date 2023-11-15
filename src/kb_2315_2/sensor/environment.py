from pydantic import BaseModel


class envirionment_sensor(BaseModel):
    name: str = "envirionment_sensor"
    temperature: float = 0.0
    humidity: float = 0.0
    pressure: float = 0.0
