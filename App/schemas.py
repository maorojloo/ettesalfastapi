from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel ,constr,Field
from typing import Optional
from typing import Set
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    authjwt_secret_key : str =os.getenv("authjwt_secret_key")

class User(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "pass"
            }
        }

datetimeValidation = '\d{4}\/\d{2}\/\d{2}T\d{2}:\d{2}:\d{2}'
class Conference(BaseModel):
    id : Optional[int]= Field(read_only=True, allow_blank=True)
    title : str
    description : str
    start_time : constr(regex=datetimeValidation)
    end_time : constr(regex=datetimeValidation)
    Capacity : int
    items : str

    class Config:
        schema_extra = {
            "example": {
                "title" : "meeting",
                "description" : "workshop",
                "start_time" : "1401/01/15T15:36:18",
                "end_time" : "1402/01/15T15:36:18",
                "Capacity" : 52,
                "items" : "some string",
            }
        }
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "Capacity": self.Capacity,
            "items": self.items,
        }
