from flask import Flask, send_from_directory, current_app
from werkzeug.exceptions import HTTPException
from .db import db, migrate
from .routes import register_routes
from . import models
from flask_cors import CORS
from .extensions import ma
import os


def create_app():
    app = Flask(__name__)

    # SQLite config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///plants_humidity_data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # upload files config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(
        BASE_DIR,
        "..",
        os.getenv("UPLOAD_FOLDER", "uploads")
    )
    max_mb = int(os.getenv("MAX_CONTENT_LENGTH_MB", 5))
    app.config["MAX_CONTENT_LENGTH"] = max_mb * 1024 * 1024

    @app.errorhandler(413)
    def file_too_large(e):
        return {"message": f"File too large. Max size is {max_mb}MB"}, 413

    # any other HTTP error (404, 405, ...) as JSON instead of HTML
    @app.errorhandler(HTTPException)
    def http_error(e):
        return {"message": e.description}, e.code

    #initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    #init Marshmallow for validation
    ma.init_app(app)

    # cors config
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    methods = os.getenv("METHODS", "GET,POST,PUT,DELETE").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins, "methods": methods}})

    # register routes
    register_routes(app, os.getenv("API_PREFIX", "/api/v1"))

    # serves uploaded files
    @app.route("/uploads/<path:filename>")
    def uploaded_files(filename):
        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

    return app