"""
@author Zuicie
@date 2024-10-19
"""


from flask import Flask, redirect, session, url_for
from flask_bootstrap import Bootstrap5
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import current_user, LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .extensions import *
from .models import *
import os


def create_app(config_name=None):
    app = Flask(__name__)

    # If running unit tests, load the testing configuration.
    if config_name == 'testing':
        from config import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'documentation':
        from config import DocumentationConfig
        app.config.from_object(DocumentationConfig)
    else:
        # Default configuration
        from config import Config
        app.config.from_object(Config)

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
    # Initialize and setup the Login Manager.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    toolbar = RestrictToolbarExtension(app)  # Initialize the debug Toolbar.

    # Register the blueprints
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create a default user if one does not exist, only if not testing
    if not app.config.get("TESTING", False) and not os.getenv('FLASK_MIGRATING'):
        with app.app_context():
            try:
                default_user = User.query.filter_by(email=os.getenv('DEFAULT_USER_EMAIL')).first()
                if not default_user:
                    from werkzeug.security import generate_password_hash
                    new_user = User(
                        email=os.getenv('DEFAULT_USER_EMAIL'),
                        username=os.getenv('DEFAULT_USER_USERNAME'),
                        name=os.getenv('DEFAULT_USER_NAME'),
                        password=generate_password_hash(os.getenv('DEFAULT_USER_PASSWORD'), method='pbkdf2:sha256'),
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    print('Default user created.')

                    # Create the admin role if it does not exist as a permission.
                    # Ensure the admin permission exists
                    default_permission = UserPermissions.query.filter_by(name='Admin').first()
                    if not default_permission:
                        admin_permission = UserPermissions(name='Admin')
                        db.session.add(admin_permission)
                        db.session.commit()
                        default_permission = UserPermissions.query.filter_by(name='Admin').first()

                    # Assign the existing admin permission to the user, not create a new one
                    user = User.query.filter_by(email=os.getenv('DEFAULT_USER_EMAIL')).first()
                    user.permissions.append(default_permission)
                    db.session.commit()


            except Exception as e:
                import traceback
                traceback.print_exc()
                app.logger.error(f"Error creating default user: {e}")

    return app


class RestrictToolbarExtension(DebugToolbarExtension):
    """
    Restricts usage of Flask-DebugToolbar to users with Admin privileges.
    """
    def _show_toolbar(self):
        return current_user.is_authenticated and current_user.has_permission('Admin') and super()._show_toolbar()




