"""
@author :   Zuicie
@date   :   November 19, 2024

Used by pytest to share fixtures across multiple test files.
"""

import pytest
from website import create_app, db as _db
from sqlalchemy import event
from sqlalchemy.engine import Engine
from werkzeug.security import generate_password_hash


# Ensure SQLite enforces foreign key constraints
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    if _db.engine.url.drivername == 'sqlite':
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


@pytest.fixture(scope='session')
def app():
    """
    Create and configure a new app instance for each test session.
    """
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def db(app):
    """
    Create a database for the tests.
    """
    _db.app = app
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """
    Create a new database session for a test.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    A test runner for the Flask CLI
    """
    return app.test_cli_runner()



