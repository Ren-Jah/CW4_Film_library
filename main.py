from flask import Flask
from flask_restx import Api

from app.config import Config
from app.database import db
from app.views.main.directors import director_ns
from app.views.main.genres import genre_ns
from app.views.main.movies import movie_ns
from app.views.auth.user import user_ns
from app.views.auth.auth import auth_ns
from app.utils import create_data


def create_app(config: Config):
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    create_data(app, db)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    app.run(host="localhost", port=7000, debug=True)