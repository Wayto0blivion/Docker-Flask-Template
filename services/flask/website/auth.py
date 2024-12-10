"""
@author : Zuicie
@date : 2024-10-20
"""

from . import db
from .models import User
from .forms import LoginForm, RegistrationForm, UserProfileForm
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Allows the user to authenticate with unique credentials.
    """
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Check if the user actually exists and if credentials match
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', category='danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('views.home'))

    return render_template('login.html', title="Login", form=form)


@auth.route('/signup', methods=['GET', 'POST'])
# @login_required  # Uncommenting this will allow only users that are already in the system to create new users.
def signup():
    """
    Allows a new user to register with the application.
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        # Check if the email already exists for a user.
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered!", category='danger')
            return redirect(url_for('auth.signup'))
        # Check if username already exists.
        username_check = User.query.filter_by(username=username).first()
        if username_check:
            flash("Username already registered!", category='danger')
            return redirect(url_for('auth.signup'))

        # Otherwise, create a new user, and hash the password.
        new_user = User(email=email, username=username, name=form.name.data,
                        password=generate_password_hash(form.password.data, method='pbkdf2:sha256'))

        # Add the user to the database.
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template("login.html", title="Sign-Up", form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Logs the user out and returns them to the home page.
    Returns:
        Redirect to auth.login.
    """
    logout_user()
    # Get a reference to the current theme so that it isn't reset.
    session_theme = session.get('theme')
    session.clear()
    session['theme'] = session_theme
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Handles user account and profile information. Mostly for allowing user to change password.
    Returns:
        HTML template for profile page, profile.html
    """
    form = UserProfileForm()

    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.current_password.data):
            user = User.query.filter_by(id=current_user.id).first()
            user.password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            return redirect(url_for('auth.logout'))
        else:
            flash('The old password was incorrect!', category='danger')
    else:
        # Form was submitted but is not valid.
        if form.is_submitted():  # Ensure the form was actually submitted.
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in the {field} field: {error}")

    return render_template('profile.html', title="Profile", form=form)





