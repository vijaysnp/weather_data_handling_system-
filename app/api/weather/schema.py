from app.constant import constant
from app.api.core import validation
from pydantic import BaseModel, ConfigDict, field_validator



class HistoricWeatherRequest(BaseModel):
    latitude: float
    longitude: float
    days: int
    
    model_config = ConfigDict(from_attributes=constant.STATUS_TRUE, json_schema_extra={
        "example": {
            "latitude": 52.52,
            "longitude": 13.41,
            "days": 5
        }
    })
    
    @field_validator('latitude')
    @classmethod
    def name_must_be_required(cls, v):
        return validation.ValidationMethods().check_float_validator(v, 'latitude')

    @field_validator('longitude')
    @classmethod
    def name_must_be_required(cls, v):
        return validation.ValidationMethods().check_float_validator(v, 'longitude')

