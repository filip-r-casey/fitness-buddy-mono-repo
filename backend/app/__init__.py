from flask import Flask
from flask_cors import CORS


def create_app():
    application = Flask(__name__)
    from .views import app_routes
    application.register_blueprint(app_routes)
    CORS(application)
    return application
