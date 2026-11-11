from flask import Blueprint
from ..schemas.sensor_schema import sensor_schema, sensors_schema
from ..models import Sensor
from ..utils import load_json, get_or_404
from ..db import db

# errors are turned into JSON in errors.py:
# ApiError -> its status, ValidationError -> 422, IntegrityError -> 409/400
sensors_bp = Blueprint("sensors", __name__)


@sensors_bp.get("/sensors")
def get_all_sensors():
    sensors = Sensor.get_all()

    message = {"data": sensors_schema.dump(sensors)}
    return message, 200

@sensors_bp.post("/sensors")
def add_sensor():
    validated_data = load_json(sensor_schema)

    sensor = Sensor(
        pin=validated_data["pin"],
        plant_id=validated_data["plant_id"]
    )

    db.session.add(sensor)
    db.session.commit()

    message = {"message": "Sensor created", "data": sensor_schema.dump(sensor)}
    return message, 201

@sensors_bp.get("/sensors/<int:id>")
def get_sensor_by_id(id):
    sensor = get_or_404(Sensor, id, "Sensor not found")

    message = {"data": sensor_schema.dump(sensor)}
    return message, 200

@sensors_bp.put("/sensors/<int:id>")
def update_sensor(id):
    sensor = get_or_404(Sensor, id, "Sensor not found")
    validated_data = load_json(sensor_schema)

    sensor.pin = validated_data["pin"]
    sensor.plant_id = validated_data["plant_id"]
    db.session.commit()

    message = {"message": "Sensor updated", "data": sensor_schema.dump(sensor)}
    return message, 200

@sensors_bp.delete("/sensors/<int:id>")
def delete_sensor(id):
    sensor = get_or_404(Sensor, id, "Sensor not found")

    db.session.delete(sensor)
    db.session.commit()

    return {"message": "Sensor deleted"}, 200
