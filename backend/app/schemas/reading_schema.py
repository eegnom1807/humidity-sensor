from ..extensions import ma
from marshmallow import fields, validate


class ReadingSchema(ma.Schema):
    pin = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=10)
    )
    humidity = fields.Float(required=True)

reading_schema = ReadingSchema()