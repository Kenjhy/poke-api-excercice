from pydantic import BaseModel


class Berry(BaseModel):
    name: str
    growth_time: int