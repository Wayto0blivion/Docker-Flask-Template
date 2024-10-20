"""
@author : Zuice
@date : 2024-10-20
"""

from . import db
from .forms import LoginForm, RegistrationForm
from flask import Blueprint, render_template


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html', title="Login", form=LoginForm())


@auth.route('/signup')
def signup():
    return render_template("login.html", title="Sign-Up", form=RegistrationForm())


@auth.route('/logout')
def logout():
    return 'Logout'










