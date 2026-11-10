from flask import Blueprint
from ..models import HumidityReading, Sensor
from ..utils import require_api_key, load_json
from ..errors import ApiError
from ..schemas.reading_schema import reading_schema
from ..db import db

# errors are turned into JSON in errors.py:
# ApiError -> its status, ValidationError -> 422
readings_bp = Blueprint("readings", __name__)


@readings_bp.post("/readings")
@require_api_key
def create_reading():
    validated_data = load_json(reading_schema)

    sensor = Sensor.get_by_pin(validated_data["pin"])
    if not sensor:
        raise ApiError("Sensor not found", 404)

    reading = HumidityReading(
        sensor_id=sensor.id,
        humidity=validated_data["humidity"]
    )

    db.session.add(reading)
    # active plant
    sensor.plant.active = True

    db.session.commit()

    message = {"message": "Reading created", "data": reading_schema.dump(reading)}
    return message, 201
