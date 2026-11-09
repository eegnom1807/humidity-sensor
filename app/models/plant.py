from sqlalchemy.sql import func
from sqlalchemy import event
from ..utils import delete_file_if_exists
from ..db import db


class Plant(db.Model):
    __tablename__ = "plants"

    __table_args__ = (
        db.UniqueConstraint("name", name="uq_plants_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    sensor = db.relationship(
        "Sensor",
        back_populates="plant",
        uselist=False,
        cascade="all, delete-orphan"
    )

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
@event.listens_for(Plant, "after_delete")
def delete_plant_image(mapper, connection, target):
    delete_file_if_exists(target.image_url)