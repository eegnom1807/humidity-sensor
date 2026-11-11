from marshmallow import Schema, fields
from ..utils import get_date


class DashboardSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    image_url = fields.Str()
    active = fields.Bool()
    humidity = fields.Float()
    pin = fields.Str()
    last_reading = fields.Method("format_last_reading")

    def format_last_reading(self, obj):
        return get_date(obj["last_reading"]) if obj["last_reading"] is not None else ""

dashboard_schema = DashboardSchema(many=True)