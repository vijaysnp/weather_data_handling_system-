## About The Project

Historic weather data handling system 

### Built With

* Python 3.11
* FastAPI


<!-- GETTING STARTED -->
## Getting Started

Instructions for setting up project locally.
To get a local copy up and running follow these simple steps.

## Install + configure the project

### 1. Linux
### Prerequisites

Requirement of Project
* Install Python 
  ```sh
  Python-Version : 3.11.0
  ```
* Create python virtual environment
  ```sh
  python3 -m venv venv
  ```
* Activate the python virtual environment
  ```sh
  source venv/bin/activate
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/vijaysnp/weather_data_handling_system
   ```
2. Upgrade pip version
    ```sh
   python -m pip install --upgrade pip==22.1.2
    ```
3. Install the requirements for the project into the virtual environment
   ```sh
   pip install -r requirements.txt
   ```
4. Install the dependencies of Fast API
   ```sh
   pip install "fastapi[all]"
   pip install "uvicorn[standard]"

   ```

### 2. Windows

1. Create python virtual environment
   ```
   conda create --name venv python=3.11
   ```

2. Activate the python virtual environment
   ```
   conda activate venv
   ```

3. Install the requirements for the project into the virtual environment in the following sequence:
   ```
   pip install -r requirements.txt
   ```

4. Install the dependencies of Fast API
   ```
   pip install "fastapi[all]"
   ```

5. Upgrade pip version
   ```
   python -m pip install --upgrade pip==22.1.2
   ```

### Use the alembic to Upgrade/Downgrade the database in the FastAPI
  Note: Because by default Fastapi is provide only initial migrations. 
  It doesn't support the upgrade and downgrade the database.
   so,to perform automatic migrations follow the following steps:


1. To create Migration folder
    ```
    python -m alembic init migrations
    ```
2. Update the sqlalchemy.url into alembic.ini file
    ```
    sqlalchemy.url = mysql+pymysql://user:pass@host/db_name
    ```

3. update the Migrations>>env.py file o auto migrate the database.
    ```
    from config.database import Base 
    target_database = Base.metadata
    ```

4. Perform the initial migrations
    ```
    alembic revision --autogenerate -m 'initials'
    ```

5. Apply the changes into the database (upgrade the database)
    ```
    alembic upgrade head
    ```

6. To downgrade the database if required
    ```
    alembic downgrade -1
    ```

## Run the server in development mode
 
Add environment variables (given in .env) by running following command in cmd/terminal:

Run the server
   ```
   python main.py
   ```
Browse Swagger API Doc at: http://localhost:8000/docs

Browse  Redoc at: http://localhost:8000/redoc

## Framework selection reasons

   1. FastAPI's Performance: FastAPI is known for its high performance. It leverages Python type hints to automatically generate API documentation, which reduces the amount of code you need to write while ensuring type safety. Additionally, it is built on top of Starlette and Pydantic, which are highly performant asynchronous libraries. This makes FastAPI suitable for handling authentication requests efficiently, especially in high-traffic applications.

   2. Asynchronous Support: FastAPI fully supports asynchronous programming, allowing you to handle multiple concurrent requests efficiently. Asynchronous programming is particularly useful for authentication APIs where you may need to perform tasks such as database queries or external API calls without blocking the event loop.

   3. Easy Integration with Pydantic: FastAPI integrates seamlessly with Pydantic, a powerful data validation library. Pydantic allows you to define data models with type annotations and validation rules, making it easy to validate and serialize incoming request data, including user credentials during the authentication process.
