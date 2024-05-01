from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    from .views import app_routes
    app.register_blueprint(app_routes)
    CORS(app)
    return app
