from pydantic import BaseModel


class envirionment_sensor(BaseModel):
    temperature: float = 0.0
    humidity: float = 0.0
    pressure: float | None = None
