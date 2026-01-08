from pydantic import BaseModel

class Data(BaseModel):
    name:str
    mail:str
    address:str

class Del(BaseModel):
    mail:str