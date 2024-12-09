"""
@author : Zuicie
@date : 2024-10-20
"""
from email.policy import default

from .extensions import db
from flask_login import UserMixin


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
    permissions = db.relationship("UserPermissions", secondary='user_permission', backref='users')

    def has_permission(self, permission_name):
        """
        Check if the user has a given permission by name.
        """
        return any (p.name == permission_name for p in self.permissions)


class UserPermissions(db.Model):
    """
    Stores user permissions such as admin, DebugToolbar, etc.
    Can be extended for any granular permissions.
    """
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# Association table for many-to-many user permissions. Purely a lookup table, doesn't require its own model class.
user_permission = db.Table(
    'user_permission',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True),
)



