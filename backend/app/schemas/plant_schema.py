from marshmallow import Schema, fields, validate
from ..utils import get_date


class PlantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )
    image_url = fields.Str(
        allow_none=True,
        validate=validate.Length(max=255)
    )
    # changed only by POST /readings, not by the client
    active = fields.Bool(dump_only=True)
    updated_at = fields.Method("format_updated_at")

    def format_updated_at(self, obj):
        return get_date(obj.updated_at)

plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)