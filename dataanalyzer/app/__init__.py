from flask import Flask
from .views import app_routes
from application import start_listener_thread


def create_app():
    application = Flask(__name__)
    application.register_blueprint(app_routes)  # Register the blueprint

    # Start the database listener in a separate thread
    start_listener_thread()

    return application
