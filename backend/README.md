# humidity_sensor_api

## Clone the repository
https://github.com/eegnom1807/humidity-sensor-api.git

## Create virtual env
- python3 -m venv venv

## Install dependencies: 
- pip install -r requirements.txt

## Create migrations:
- flask db init     # just one time
- flask db migrate -m "create sensor table"
- flask db upgrade

## Run app locally:
- python run.py after create th env environment and install the dependencies

## Freeze dependencies when add a new one:
- pip freeze > requirements.txt