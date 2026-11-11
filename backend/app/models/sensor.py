from sqlalchemy.sql import func
from ..db import db


class Sensor(db.Model):
    __tablename__ = "sensors"

    __table_args__ = (
        db.UniqueConstraint("pin", name="uq_sensors_pin"),
        db.UniqueConstraint("plant_id", name="uq_sensors_plant_id"),
        db.ForeignKeyConstraint(
            ["plant_id"],
            ["plants.id"],
            name="fk_readings_plant_id"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(10), nullable=False)
    plant_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    plant = db.relationship("Plant", back_populates="sensor")
    readings = db.relationship(
        "HumidityReading",
        cascade="all, delete-orphan"
    )

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_pin(cls, pin):
        return cls.query.filter_by(pin=pin).first()