"""
@author : Zuicie
@date : 2024-10-20
"""
from website.extensions import db
from flask_login import UserMixin
import json
from sqlalchemy import func
from sqlalchemy.dialects.mysql import JSON
import uuid


class User(db.Model, UserMixin):
    """
    Stores user information such as email, username, and password.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    # Establish a many-to-many relationship to UserPermissions via the association table user_permission.
    permissions = db.relationship("Permissions", secondary='user_permission', backref='users')

    def has_permission(self, permission_name):
        """
        Check if the user has a given permission by name.
        """
        return any (p.name == permission_name for p in self.permissions)


class Permissions(db.Model):
    """
    Stores user permissions such as admin, DebugToolbar, etc.
    Can be extended for any granular permissions.
    """
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class UserPermissions(db.Model):
    """
    Association model for many-to-many user permissions.
    """
    __tablename__ = 'user_permission'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)


class QueryConfiguration(db.Model):
    """
    Stores query parameters in the database so they can be loaded in dynamically with the Fetch API.
    """
    __tablename__ = 'query_configurations'
    id = db.Column(db.String(36), primary_key=True)  # Store UUID as string
    model_name = db.Column(db.String(128), nullable=False)
    filters = db.Column(JSON, nullable=True)
    columns = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


def build_model_registry():
    """
    Build a model registry keyed by __tablename__.
    Designed to allow models to be called using a string related to tablename.
    Returns:
        registry (dict):
            keys:   __tablename__ related to the models in models.py
            values: The actual model, to be used with SQLAlchemy queries.
    """
    registry = {}
    # Iterate over all mappers in the model's registry
    for mapper in db.Model.registry.mappers:
        model_class = mapper.class_
        # only register classes that have __tablename__
        if hasattr(model_class, '__tablename__'):
            registry[model_class.__tablename__] = model_class

    return registry


# Build the registry described in build_model_registry:
model_registry = build_model_registry()


def get_model_by_name(name):
    """
    Trades the string key of __tablename__ for the corresponding model value.
    Args:
        name: (str) name of the model

    Returns:
        model: (obj) database to be used with SQLAlchemy queries.

    """
    return model_registry.get(name)



















