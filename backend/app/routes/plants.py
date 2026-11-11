from flask import Blueprint, request, current_app
from ..schemas.plant_schema import plant_schema, plants_schema
from ..models import Plant
from ..utils import allowed_file, delete_file_if_exists, load_json, get_or_404
from ..errors import ApiError
from ..db import db
import os
import time

# errors are turned into JSON in errors.py:
# ApiError -> its status, ValidationError -> 422, IntegrityError -> 409/400
plants_bp = Blueprint("plants", __name__)


@plants_bp.get("/plants")
def get_all_plants():
    plants = Plant.get_all()

    message = {"data": plants_schema.dump(plants)}
    return message, 200

@plants_bp.post("/plants")
def add_plant():
    validated_data = load_json(plant_schema)

    plant = Plant(
        name=validated_data["name"],
        # frontend expects "" (not null) when there is no image
        image_url=validated_data.get("image_url") or ""
    )

    db.session.add(plant)
    db.session.commit()

    message = {"message": "Plant created", "data": plant_schema.dump(plant)}
    return message, 201

@plants_bp.get("/plants/<int:id>")
def get_plant_by_id(id):
    plant = get_or_404(Plant, id, "Plant not found")

    message = {"data": plant_schema.dump(plant)}
    return message, 200

@plants_bp.put("/plants/<int:id>")
def update_plant(id):
    plant = get_or_404(Plant, id, "Plant not found")
    validated_data = load_json(plant_schema)

    # image is managed by POST /plants/<id>/image;
    # a missing or empty image_url keeps the current image
    new_image_url = validated_data.get("image_url")
    if new_image_url and new_image_url != plant.image_url:
        delete_file_if_exists(plant.image_url)
        plant.image_url = new_image_url

    plant.name = validated_data["name"]
    db.session.commit()

    message = {"message": "Plant updated", "data": plant_schema.dump(plant)}
    return message, 200

@plants_bp.delete("/plants/<int:id>")
def delete_plant(id):
    plant = get_or_404(Plant, id, "Plant not found")

    # delete the image only after the commit succeeds
    image_url = plant.image_url
    db.session.delete(plant)
    db.session.commit()
    delete_file_if_exists(image_url)

    return {"message": "Plant deleted"}, 200

@plants_bp.post("/plants/<int:id>/image")
def upload_image(id):
    plant = get_or_404(Plant, id, "Plant not found")

    if "image_url" not in request.files:
        raise ApiError("Photo file is required", 400)

    file = request.files["image_url"]
    if file.filename == "":
        raise ApiError("Empty filename", 400)

    if not allowed_file(file.filename):
        raise ApiError("Invalid file type", 400)

    delete_file_if_exists(plant.image_url)

    # the final name is built here, so only the (already validated) extension is used
    ext = file.filename.rsplit(".", 1)[1].lower()

    upload_dir = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "plants"
    )

    os.makedirs(upload_dir, exist_ok=True)
    # timestamp in the name so browsers don't show a cached old image
    final_filename = f"{plant.id}-{int(time.time())}.{ext}"
    file_path = os.path.join(upload_dir, final_filename)
    file.save(file_path)

    plant.image_url = f"/uploads/plants/{final_filename}"
    db.session.commit()

    return {
        "message": "Uploaded file",
        "data": plant_schema.dump(plant)
    }, 200
