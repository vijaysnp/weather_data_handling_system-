from fastapi import Depends, APIRouter, status
from app.constant import constant
from config import database
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from app.utils.message import InfoMessage, ErrorMessage
from app.api.auth.services import user_auth_service 
from app.utils.standard_response import StandardResponse
from app.api.weather.services import weather_data_service
                                

weatherrouter = APIRouter()
getdb = database.get_db


class Weatherdata():

    @weatherrouter.get("/historic-weather/data")
    async def get_historic_weather_data(latitude: float, longitude: float, days: int, 
                                    db: Session = Depends(getdb),
                                    Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
        except Exception as e:
            return StandardResponse(status.HTTP_403_FORBIDDEN, constant.STATUS_NULL, \
                     ErrorMessage.invalidToken).make
        current_user = Authorize.get_jwt_subject()
        response = weather_data_service.WeatherDataService(
        ).get_historic_weather_data(db, latitude, longitude, days)
        return response

    

