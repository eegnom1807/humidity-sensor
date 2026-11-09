from ..extensions import ma
from marshmallow import fields
from ..utils import get_date


class DashboardSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    image_url = fields.Str()
    active = fields.Bool()
    humidity = fields.Float()
    pin = fields.Str()
    last_reading = fields.Method("format_last_reading")

    def format_last_reading(self, obj):
        return get_date(obj["last_reading"]) if obj["last_reading"] is not None else ""

dashboard_schema = DashboardSchema(many=True)