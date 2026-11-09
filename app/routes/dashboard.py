from flask import Blueprint, jsonify
from ..models import HumidityReading
from ..schemas.dashboard_schema import dashboard_schema

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/plants/dashboard", methods=["GET"])
def plants_dashboard():
    data = HumidityReading.get_plants_readings()
    message = {"data": dashboard_schema.dump(data)}

    return jsonify(message), 200