import hmac
import os
from flask import request, current_app
from werkzeug.security import safe_join
from datetime import timezone, timedelta
from functools import wraps
from .db import db
from .errors import ApiError

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def get_date(date):
    # dates are stored in UTC; shown in the offset from .env (default UTC-6)
    offset = float(os.getenv("UTC_OFFSET_HOURS", -6))
    time_zone = timezone(timedelta(hours=offset))
    new_date = date.replace(tzinfo=timezone.utc).astimezone(time_zone)

    return new_date.strftime("%Y-%m-%d %H:%M:%S")

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def delete_file_if_exists(relative_path):
    # image_url always looks like "/uploads/<file>" (the public route),
    # while the real folder on disk comes from app config
    url_prefix = "/uploads/"
    if not relative_path or not relative_path.startswith(url_prefix):
        return

    filename = relative_path[len(url_prefix):]
    full_path = safe_join(current_app.config["UPLOAD_FOLDER"], filename)

    if full_path and os.path.isfile(full_path):
        os.remove(full_path)

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY", "")
        expected_key = os.getenv("API_KEY", "")
        # compare_digest takes the same time whether the key matches or not
        if not expected_key or not hmac.compare_digest(api_key, expected_key):
            raise ApiError("Invalid API key", 401)

        return f(*args, **kwargs)

    return wrapper

def load_json(schema):
    data = request.get_json(silent=True)
    if not data:
        # 400: empty body or not JSON
        raise ApiError("No input data", 400)

    # ValidationError -> 422 (handled in errors.py)
    return schema.load(data)

def get_or_404(model, id, message):
    obj = db.session.get(model, id)
    if obj is None:
        raise ApiError(message, 404)

    return obj
