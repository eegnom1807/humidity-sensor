from marshmallow import Schema, fields, validate, validates, ValidationError
from ..models.plant import Plant
from ..utils import get_date
from ..db import db

# Arduino UNO R4 WiFi analog pins
ANALOG_PINS = [f"A{i}" for i in range(6)]


class SensorSchema(Schema):
    id = fields.Int(dump_only=True)
    pin = fields.Str(required=True, validate=validate.OneOf(ANALOG_PINS))
    plant_id = fields.Int(required=True)
    updated_at = fields.Method("format_updated_at")

    def format_updated_at(self, obj):
        return get_date(obj.updated_at)

    @validates("plant_id")
    def validate_plant_exists(self, value, **kwargs):
        if db.session.get(Plant, value) is None:
            raise ValidationError("Plant does not exist")

sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)