import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(script_info=None):

    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    from src.api.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from src.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
