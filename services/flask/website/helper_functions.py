"""
@author:    Zuicie
@date:      December 12, 2024

Contains functions designed to modify functionality or abstract out commonly used functions.
"""

from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


def user_permissions(permission):
    """
    Provides a custom decorator that checks if a user has a permission before
    allowing access to a route.

    Args:
        permission (str): The friendly name of the permission to check.

    Returns:
        The requested page if the user is authenticated and has a permission. If not, it
        redirects to the home page.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the current user is authenticated and has the given permission.
            if current_user.is_authenticated and current_user.has_permission(permission):
                return f(*args, **kwargs)
            else:
                # If the user isn't logged in or doesn't have the required permissions,
                # redirect them to a designated page, in this case views.home.
                return redirect(url_for('views.home'))
        return decorated_function
    return decorator




