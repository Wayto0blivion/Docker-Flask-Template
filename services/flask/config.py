"""
@author :   Zuicie
@date   :   November 19, 2024

Creates configurations for normal operation and for unit tests.
"""

import os


class Config:
    """
    The default configuration used during normal operation.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Should be False in production


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


