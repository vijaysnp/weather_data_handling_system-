import os
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
from app.utils import helper
from fastapi import status
from sqlalchemy.orm import Session
from app.constant import constant
from app.api.core import db_methods
from fastapi.encoders import jsonable_encoder
from app.api.core.db_methods import BaseMethod
from app.utils.message import InfoMessage, ErrorMessage
from app.utils.standard_response import StandardResponse


class WeatherDataService:

    def get_historic_weather_data(self, db: Session, body: dict):
        """
        Retrieves historic weather data for a given location and time period.ss

        Args:
            db (Session): The database session.
            body (dict): The request body containing the latitude, longitude, and optional number of days.

        Returns:
            StandardResponse: The response object containing the weather data or an error message.

        Raises:
            Exception: If there is an error retrieving the weather data.
        """
        try:
            data = body.dict()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            days = data.get('days', 1)

            # Setup the Open-Meteo API client with cache and retry on error
            cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
            retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
            openmeteo = openmeteo_requests.Client(session = retry_session)

            url = os.environ.get("OPENMETEO_URL")
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": ["temperature_2m", "precipitation", "cloud_cover"],
                "past_days": days,
                "forecast_days": constant.STATUS_ONE
            }

            responses = openmeteo.weather_api(url, params=params)
            # Process first location
            response = responses[0]
            
            # Process hourly data. The order of variables needs to be the same as requested.
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
            hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            ).strftime('%Y-%m-%d %H:%M:%S').tolist()}
            
            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["precipitation"] = hourly_precipitation
            hourly_data["cloud_cover"] = hourly_cloud_cover

            hourly_dataframe = pd.DataFrame(data = hourly_data)
            response_data = {"data" : hourly_dataframe.to_dict(orient='records')}
        
            return StandardResponse(status.HTTP_200_OK, response_data, InfoMessage.weatherdatafetched).make
        except Exception as e:
            return StandardResponse(status.HTTP_400_BAD_REQUEST, constant.STATUS_NULL, ErrorMessage.somethingWentWrong).make
        
