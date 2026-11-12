from .plants import plants_bp
from .sensors import sensors_bp
from .humidity_readings import readings_bp
from .dashboard import dashboard_bp
from .uploads import uploads_bp


def register_routes(app, prefix):
    app.register_blueprint(plants_bp, url_prefix=prefix)
    app.register_blueprint(sensors_bp, url_prefix=prefix)
    app.register_blueprint(readings_bp, url_prefix=prefix)
    app.register_blueprint(dashboard_bp, url_prefix=prefix)
    # no prefix: public file URLs aren't part of the versioned API
    app.register_blueprint(uploads_bp)