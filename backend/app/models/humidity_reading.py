from sqlalchemy.sql import func
from .plant import Plant
from .sensor import Sensor
from ..db import db


class HumidityReading(db.Model):
    __tablename__ = "humidity_readings"

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["sensor_id"],
            ["sensors.id"],
            name="fk_readings_sensor_id"
        ),
        # in SQLite the index also covers the rowid (id),
        # so max(id) per sensor is resolved from the index
        db.Index("ix_humidity_readings_sensor_id", "sensor_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    @classmethod
    def get_plants_readings(cls):
        # id of the latest reading of the plant's sensor
        # (max(id) instead of max(created_at): created_at has
        # 1-second resolution and ties would duplicate rows)
        latest_reading_id = (
            db.session.query(func.max(cls.id))
            .filter(cls.sensor_id == Sensor.id)
            .correlate(Sensor)
            .scalar_subquery()
        )

        query = (
            db.session.query(
                Plant.id,
                Plant.name,
                Plant.image_url,
                Plant.active,
                cls.humidity,
                Sensor.pin,
                cls.created_at.label("last_reading"),
            )
            .outerjoin(Plant.sensor)
            .outerjoin(cls, cls.id == latest_reading_id)
            .order_by(Plant.name)
        )

        return [dict(row._mapping) for row in query.all()]
