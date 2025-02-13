from pydantic import BaseModel, ConfigDict


class TuneModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
