"""
@author Zuice
@date 2024-10-19
"""
from dotenv import load_dotenv
from flask import Flask, session
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os


# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
# Debug to check if the .env file is being loaded correctly.
if load_dotenv(os.path.join(basedir, '.env')):
    print("Environment variables loaded from .env")
else:
    print("Failed to load .env file")


bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # Handle setting the default theme if one is not in session.
    @app.before_request
    def set_theme():
        if 'theme' in session:
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = session['theme']
        else:
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'zephyr'  # Default Theme

    # Initialize the SQLAlchemy connection
    db.init_app(app)
    # Initialize database migrations
    migrate.init_app(app, db)
    # Initialize the bootstrap frontend
    bootstrap.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create a default user if one does not exist
    with app.app_context():
        default_user = User.query.filter_by(email=os.getenv('DEFAULT_USER_EMAIL')).first()
        if not default_user:
            from werkzeug.security import generate_password_hash
            new_user =  User(
                email=os.getenv('DEFAULT_USER_EMAIL'),
                username=os.getenv('DEFAULT_USER_USERNAME'),
                name=os.getenv('DEFAULT_USER_NAME'),
                password=generate_password_hash(os.getenv('DEFAULT_USER_PASSWORD'), method='pbkdf2:sha256'),
            )
            db.session.add(new_user)
            db.session.commit()
            print('Default user created.')

    return app






