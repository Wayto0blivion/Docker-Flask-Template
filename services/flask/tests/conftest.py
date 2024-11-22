"""
@author :   Zuicie
@date   :   November 19, 2024

Used by pytest to share fixtures across multiple test files.
"""

import pytest
from website import create_app, db as _db
from sqlalchemy import event
from sqlalchemy.engine import Engine


# Ensure SQLite enforces foreign key constraints
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    if 'sqlite' in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


@pytest.fixture(scope='function')
def app():
    """
    Create and configure a new app instance for each test.
    """
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db(app):
    """
    Create a new database for the test.
    """
    _db.app = app
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    """
    A test client for the app.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """
    A test runner for the Flask CLI
    """
    return app.test_cli_runner()



