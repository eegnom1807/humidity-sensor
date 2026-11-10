from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from .db import db


class ApiError(Exception):
    # raise ApiError("Plant not found", 404) -> {"message": "Plant not found"}, 404
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def handle_db_error(e):
    error_msg = str(e.orig).lower()

    if "unique" in error_msg:
        return {"message": "Resource already exists"}, 409

    if "foreign key" in error_msg:
        return {"message": "Invalid reference"}, 400

    return {"message": "Integrity error"}, 400


def register_error_handlers(app):
    # errors raised by the app itself
    @app.errorhandler(ApiError)
    def api_error(e):
        return {"message": e.message}, e.status_code

    # 422: valid JSON but the data does not pass the schema validation
    @app.errorhandler(ValidationError)
    def validation_error(e):
        return {"message": e.messages}, 422

    # 409 / 400: database constraint violations (unique, foreign key)
    @app.errorhandler(IntegrityError)
    def integrity_error(e):
        db.session.rollback()
        return handle_db_error(e)

    # any other HTTP error (404, 405, ...) as JSON instead of HTML
    @app.errorhandler(HTTPException)
    def http_error(e):
        return {"message": e.description}, e.code

    # 500: any unexpected error (in debug mode Flask shows the debugger instead)
    @app.errorhandler(500)
    def internal_error(e):
        return {"message": "Internal server error"}, 500
