from flask import Flask
from flask_socketio import SocketIO
from flask_toastr import Toastr
import os

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
    toastr = Toastr(app)

    # Import and register blueprints
    from .routes.dashboard import dashboard_bp
    from .routes.communication import communication_bp
    from .routes.reports import reports_bp
    from .routes.scenarios import scenarios_bp
    from .routes.exercises import exercises_bp
    from .routes.injects import injects_bp
    from .routes.api import api_bp
    from .routes.config import config_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(communication_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(scenarios_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(injects_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(config_bp)

    socketio.init_app(app)

    return app
