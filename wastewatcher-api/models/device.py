from pydantic import BaseModel

class DeviceIn(BaseModel):
    user_id: int

class DeviceOut(BaseModel):
    id: int
    user_id: int
