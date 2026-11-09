from .plants import plants_bp
from .sensors import sensors_bp
from .humidity_readings import readings_bp
from .dashboard import dashboard_bp


def register_routes(app, prefix):
    app.register_blueprint(plants_bp, url_prefix=prefix)
    app.register_blueprint(sensors_bp, url_prefix=prefix)
    app.register_blueprint(readings_bp, url_prefix=prefix)
    app.register_blueprint(dashboard_bp, url_prefix=prefix)