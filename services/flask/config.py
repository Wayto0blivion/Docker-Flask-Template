"""
@author :   Zuicie
@date   :   November 19, 2024

Creates configurations for normal operation and for unit tests.
"""

import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Should be False in production


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'testing_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing purposes



