import os
from flask import request, current_app
from werkzeug.security import safe_join
from datetime import timezone, timedelta
from functools import wraps


def get_date(date):
    time_zone = timezone(timedelta(hours=-6))
    new_date = date.replace(tzinfo=timezone.utc).astimezone(time_zone)

    return new_date.strftime("%Y-%m-%d %H:%M:%S")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    
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
        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != os.getenv("API_KEY"):
            return {"message": "Invalid API key"}, 401
        
        return f(*args, **kwargs)
    
    return wrapper