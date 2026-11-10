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
        subquery = (
            db.session.query(
                HumidityReading.sensor_id,
                # max(id) instead of max(created_at): created_at has
                # 1-second resolution and ties would duplicate rows
                func.max(HumidityReading.id).label("last_id")
            )
            .group_by(HumidityReading.sensor_id)
            .subquery()
        )

        query = (
            db.session.query(
                Plant.id,
                Plant.name,
                Plant.image_url,
                Plant.active,
                HumidityReading.humidity,
                Sensor.pin,
                HumidityReading.created_at.label("last_reading"),
            )
            .outerjoin(Sensor, Sensor.plant_id == Plant.id)
            .outerjoin(
                subquery,
                subquery.c.sensor_id == Sensor.id
            )
            .outerjoin(
                HumidityReading,
                HumidityReading.id == subquery.c.last_id
            )
            .order_by(Plant.name)
        )

        return [dict(row._mapping) for row in query.all()]