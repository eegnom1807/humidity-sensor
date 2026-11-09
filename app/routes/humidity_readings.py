from flask import Blueprint, request, jsonify
from ..models import HumidityReading, Sensor
from ..utils import require_api_key
from marshmallow import ValidationError
from ..schemas.reading_schema import reading_schema
from ..db import db

readings_bp = Blueprint("readings", __name__)


@readings_bp.route("/readings", methods=["POST"])
@require_api_key
def create_reading():
    request_data = request.get_json(silent=True)
    if not request_data:
        return {"message": "No input data"}, 400
    
    try:
        validated_data = reading_schema.load(request_data)
    except ValidationError as err:
        return {"message": err.messages}, 422

    sensor = Sensor.get_by_pin(validated_data["pin"])
    if not sensor:
        return {"message": "Sensor not found"}, 404

    reading = HumidityReading(
        sensor_id=sensor.id,
        humidity=validated_data["humidity"]
    )

    db.session.add(reading)
    # active plant
    if not sensor.plant.active:
        sensor.plant.active = True
    
    db.session.commit()

    message = {"message": "Reading created", "data": reading_schema.dump(reading)}
    return jsonify(message), 201