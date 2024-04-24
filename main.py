import os
import uvicorn
from app._init_ import app
from config import env_config
from app.constant import constant


# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host=os.environ.get('SERVER_HOST'),
                port=int(os.environ.get('SERVER_PORT')),reload=constant.STATUS_TRUE)
