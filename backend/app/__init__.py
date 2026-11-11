from flask import Flask, send_from_directory
from .db import db, migrate
from .errors import register_error_handlers
from .routes import register_routes
from . import models
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)

    # SQLite config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///plants_humidity_data.db")

    # upload files config
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "..",
        os.getenv("UPLOAD_FOLDER", "uploads")
    )
    max_mb = int(os.getenv("MAX_CONTENT_LENGTH_MB", 5))
    app.config["MAX_CONTENT_LENGTH"] = max_mb * 1024 * 1024

    # global error handlers, always JSON (see errors.py)
    register_error_handlers(app)

    #initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # cors config
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins}})

    # register routes
    register_routes(app, os.getenv("API_PREFIX", "/api/v1"))

    # serves uploaded files
    @app.route("/uploads/<path:filename>")
    def uploaded_files(filename):
        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename
        )

    return app