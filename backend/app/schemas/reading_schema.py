from marshmallow import Schema, fields, validate
from .sensor_schema import ANALOG_PINS


class ReadingSchema(Schema):
    pin = fields.Str(required=True, validate=validate.OneOf(ANALOG_PINS))
    humidity = fields.Float(required=True)

reading_schema = ReadingSchema()