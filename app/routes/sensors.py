from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from ..schemas.sensor_schema import sensor_schema, sensors_schema
from ..models import Sensor
from ..utils import get_date
from ..utils.errors_handler import handle_db_error
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..db import db

sensors_bp = Blueprint("sensors", __name__)


@sensors_bp.route("/sensors", methods=["GET"])
def get_all_sensors():
    sensors = Sensor.get_all()

    message = {"data": sensors_schema.dump(sensors)}
    return jsonify(message), 200

@sensors_bp.route("/sensors", methods=["POST"])
def add_sensor():
    request_data = request.get_json(silent=True)
    if not request_data:
        return {"message": "No input data"}, 400
    
    try:
        validated_data = sensor_schema.load(request_data)
    except ValidationError as err:
        return {"message": err.messages}, 422
    
    sensor = Sensor(
        pin=validated_data["pin"],
        plant_id=validated_data["plant_id"]
    )

    try:
        db.session.add(sensor)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)
    
    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "Internal server error"}, 500
    
    message = {"message": "Sensor created", "data": sensor_schema.dump(sensor)}
    return jsonify(message), 201

@sensors_bp.route("/sensors/<int:id>", methods=["GET"])
def get_sensor_by_id(id):
    sensor = Sensor.get_by_id(id)
    if sensor is None:
        return {"message":  "Sensor not found"}, 404
    
    message = {"data": sensor_schema.dump(sensor)}
    return jsonify(message), 200

@sensors_bp.route("/sensors/<int:id>", methods=["PUT"])
def update_sensor(id):
    sensor = Sensor.get_by_id(id)
    if sensor is None:
        return {"message":  "Sensor not found"}, 404
    
    request_data = request.get_json(silent=True)
    if not request_data:
        return {"message": "No input data"}, 400
    
    try:
        validated_data = sensor_schema.load(request_data)
    except ValidationError as err:
        return {"message": err.messages}, 422

    sensor.pin = validated_data["pin"]
    sensor.plant_id = validated_data["plant_id"]

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)
    
    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "Internal server error"}, 500

    message = {"message": "Sensor updated", "data": sensor_schema.dump(sensor)}
    return jsonify(message), 200

@sensors_bp.route("/sensors/<int:id>", methods=["DELETE"])
def delete_sensor(id):
    sensor = Sensor.get_by_id(id)
    if sensor is None:
        return {"message":  "Sensor not found"}, 404

    try:
        db.session.delete(sensor)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return handle_db_error(e)
    
    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "Internal server error"}, 500

    return {"message": "Sensor deleted"}, 200