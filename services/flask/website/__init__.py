"""
@author Zuicie
@date 2024-10-19
"""

from dotenv import load_dotenv
from flask import Flask, redirect, session, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_bootstrap import Bootstrap5
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import current_user, LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .extensions import *
from .models import *
import os


class AdminPermissionModelView(ModelView):
    """
    Custom ModelView that dynamically handles relationships and ensures permission checks.
    """

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('views.home'))

    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)

        # Dynamically configure relationship fields for many-to-many tables
        if hasattr(model, '__mapper__'):
            relationships = [
                rel.key for rel in model.__mapper__.relationships
                if rel.secondary is not None  # Many-to-Many relationships
            ]
            # Ensure form_columns is initialized properly
            self.form_columns = (getattr(self, 'form_columns', []) or ['id']) + relationships
            self.column_list = (getattr(self, 'column_list', []) or ['id']) + relationships



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
    toolbar = DebugToolbarExtension(app)  # Initialize the debug Toolbar.
    # Add Flask-Admin
    admin = Admin(app, name='Data', url='/data-admin', template_mode='bootstrap4')

    # Add all models to Flask-Admin dynamically
    for mapper in db.Model._sa_registry.mappers:
        model_class = mapper.class_
        if hasattr(model_class, '__tablename__'):
            admin.add_view(AdminPermissionModelView(model_class, db.session))

    # Add all association tables (lookup tables) dynamically
    mapped_table_names = [mapper.class_.__tablename__ for mapper in db.Model._sa_registry.mappers if
                          hasattr(mapper.class_, '__tablename__')]

    for table_name, table in db.metadata.tables.items():
        if table_name not in mapped_table_names:
            try:
                # Dynamically create a model for the table
                class LookupModel(db.Model):
                    __table__ = table

                admin.add_view(AdminPermissionModelView(LookupModel, db.session, name=f"{table_name.title()} Lookup"))
            except Exception as e:
                app.logger.warning(f"Could not add table {table_name} to admin: {e}")

    # Add a back button so that the homepage can be returned to from the Flask-Admin page.
    admin.add_link(MenuLink(name='Back', url='/'))

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






