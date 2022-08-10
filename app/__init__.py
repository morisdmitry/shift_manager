import os
from flask import Flask
from app.database import db
from config import Config
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)
    migrate = Migrate(
        app,
        db,
        directory=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "database/migrations"
        ),
    )

    from app.api import api, api_blueprint, routes

    api.init_app(api_blueprint)
    app.register_blueprint(api_blueprint)

    return app
