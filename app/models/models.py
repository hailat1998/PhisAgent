from pydantic import BaseModel, Field
from datetime import datetime, timezone
import time



class ResponseModel(BaseModel):
    username: str
    message: str
    competence: float = Field(ge=0.0, le=1.0)
    certainty: float = Field(ge=0.0, le=1.0)
    affiliation: float = Field(ge=0.0, le=1.0)
    arousal: float = Field(ge=0.0, le=1.0) 
    resolution: float = Field(ge=0.0, le=1.0)
    selection_threshold: float = Field(ge=0.0, le=1.0)
    

    # class Config:
    #     allow_population_by_field_name = True
    #     schema_extra = {
    #         "example": {
    #             "username": "john_doe",
    #             "message": "Hello World",
    #             "competence": 0.8,
    #             "certainty": 0.9,
    #             "affiliation": 0.7
    #         }
    #     }



class RequestModel(BaseModel):
    username: str
    message: str
    competence: float = Field(ge=0.0, le=1.0)
    certainty: float = Field(ge=0.0, le=1.0)
    affiliation: float = Field(ge=0.0, le=1.0)
    arousal: float = Field(ge=0.0, le=1.0) 
    resolution: float = Field(ge=0.0, le=1.0)
    selection_threshold: float = Field(ge=0.0, le=1.0)
   


