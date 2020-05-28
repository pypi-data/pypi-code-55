from flask import Flask
from dotenv import load_dotenv
from .orm import init_orm

load_dotenv()


def create_app(config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    if config:
        app.config.from_object(config)
    else:
        from .config import DefaultConfig
        app.config.from_object(DefaultConfig)

    # init orm
    init_orm(app)

    return app
