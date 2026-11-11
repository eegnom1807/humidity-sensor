from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge, InternalServerError
from .db import db


class ApiError(HTTPException):
    # raise ApiError("Plant not found", 404) -> {"message": "Plant not found"}, 404
    # handled by http_error, like any other HTTP error
    def __init__(self, message, status_code):
        super().__init__(description=message)
        self.code = status_code


def register_error_handlers(app):
    # 422: valid JSON but the data does not pass the schema validation
    @app.errorhandler(ValidationError)
    def validation_error(e):
        return {"message": e.messages}, 422

    # 409 / 400: database constraint violations (unique, foreign key)
    @app.errorhandler(IntegrityError)
    def integrity_error(e):
        db.session.rollback()
        error_msg = str(e.orig).lower()

        if "unique" in error_msg:
            return {"message": "Resource already exists"}, 409

        if "foreign key" in error_msg:
            return {"message": "Invalid reference"}, 400

        return {"message": "Integrity error"}, 400

    # 413: uploaded file bigger than MAX_CONTENT_LENGTH
    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(e):
        max_mb = app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)
        return {"message": f"File too large. Max size is {max_mb}MB"}, e.code

    # ApiError and any other HTTP error (404, 405, ...) as JSON instead of HTML
    @app.errorhandler(HTTPException)
    def http_error(e):
        return {"message": e.description}, e.code

    # 500: any unexpected error (in debug mode Flask shows the debugger instead)
    @app.errorhandler(InternalServerError)
    def internal_error(e):
        return {"message": "Internal server error"}, e.code
