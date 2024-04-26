from config import cors
from fastapi import FastAPI
from config import database
from app.constant import constant
from app.api.auth.view import authrouter
from app.api.weather.view import weatherrouter
from app.api.auth.models.model import Base as authbase

# Bind with the database, whenever new models find it's create it.
authbase.metadata.create_all(bind=database.engine)

# Create app object and add routes
app = FastAPI(title="weather data monitoring", middleware=cors.middleware)

# define router for different version
# router for version 1
app.include_router(
    authrouter, 
    prefix=f'{constant.API_V1}/auth',
                   tags=['Authentication'])

app.include_router(
    weatherrouter, 
    prefix=f'{constant.API_V1}',
                   tags=['weather API'])