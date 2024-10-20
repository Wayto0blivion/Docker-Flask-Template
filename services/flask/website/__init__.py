"""
@author Zuice
@date 2024-10-19
"""
from dotenv import load_dotenv
from flask import Flask, session
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os


# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # Handle setting the default theme if one is not in session.
    @app.before_request
    def set_theme():
        if 'theme' in session:
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = session['theme']
        else:
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'zephyr'  # Default Theme

    # Initialize the SQLAlchemy connection
    # db.init_app(app)
    # Initialize database migrations
    # migrate.init_app(app, db)
    # Initialize the bootstrap frontend
    bootstrap.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app






