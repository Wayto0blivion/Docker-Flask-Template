"""
@author :   Zuicie
@date   :   November 19, 2024

Creates configurations for normal operation and for unit tests.
"""

# from distutils.util import strtobool
import os


class Config:
    """
    The default configuration used during normal operation.
    """
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # Prevent Flask-DebugToolbar from intercepting redirects.
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Should be False in production

    FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH')  # Set the theme for the admin panel.

    # Set options for Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = True if os.getenv('MAIL_USE_TLS') == 'True' else False
    MAIL_USE_SSL = True if os.getenv('MAIL_USE_SSL') == 'True' else False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Set debug options, generally related to Flask-DebugToolbar
    if os.getenv("FLASK_DEBUG", "0") == '1':  # Checks FLASK_DEBUG from .env and uses that as the value.
        DEBUG = True  # Sets the debug variable to True/False based on 0/1 value from .env
        SQLALCHEMY_RECORD_QUERIES = True  # Records information about each query. This is needed by Flask-DebugToolbar.
        SQLALCHEMY_ECHO = True  # This prints SQLAlchemy queries to the log file.
    else:
        DEBUG = False
        SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """
    Allows unit tests to be performed outside of Docker using an in-memory SQLite database.
    """
    TESTING = True
    SECRET_KEY = 'testing_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing purposes


class DocumentationConfig(Config):
    """
    Allows documentation to be built during development using Sphinx.
    """
    # Allows the in-memory database to be loaded with models and defaults during create_app().
    TESTING = True
    SECRET_KEY = 'documentation_secret_key'  # Dummy secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite for tests


