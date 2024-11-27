"""
@author : Zuicie
@date : 2024-10-20
"""
from email.policy import default

from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Stores user information such as email, username, and password.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    permissions = db.relationship("UserPermissions")


class UserPermissions(db.Model):
    """
    Stores user permissions such as admin, DebugToolbar, etc.
    Can be extended for any granular permissions.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    debug = db.Column(db.Boolean, default=False, nullable=False)






