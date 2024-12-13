"""
@author : Zuicie
@date : 2024-10-20
"""

from . import db
from .helper_functions import user_permissions
from .models import User, QueryConfiguration
from .forms import LoginForm, RegistrationForm, UserProfileForm, ForgotPasswordForm, ResetPasswordForm
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


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


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """

    Returns:

    """
    if current_user.is_authenticated:  # If the user is already logged in, take them back to the home page.
        return redirect(url_for('views.home'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.id)

            # Construct the URL for resetting the password
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            # TODO: Send an email (Replace below with actual sending of email)
            print(f"[DEBUG] Would send email to {user.email} with link: {reset_url}")

        flash('If that email is in our system, you will receive a password reset link.', category='info')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html', title="Forgot Password", form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """

    Args:
        token:

    Returns:

    """
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    user_id = verify_reset_token(token)
    if not user_id:
        flash('Your reset link is invalid or expired.', category='danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.get(user_id)
        if user:
            user.password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash('Your password has been updated!', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('User does not exist!', category='danger')
            return redirect(url_for('auth.forgot_password'))

    return render_template('reset_password.html', title="Reset Password", form=form, token=token)

def generate_reset_token(user_id, expires_sec=1800):
    """
    Generate a token that expires after 30 minutes (1800 seconds)
    Args:
        user_id: The id of the user requesting a password reset.
        expires_sec: How long to allow the link to persist for.

    Returns:
        Serialized token that has been salted for user reset functions.

    """
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt="password-reset-salt")
    return s.dumps(user_id)


def verify_reset_token(token, max_age=1800):
    """
    Verify token within 30 minutes (1800 seconds).
    Args:
        token: The token to verify.
        max_age: The maximum age the token can be.

    Returns:
        user_id or None

    """
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt="password-reset-salt")
    try:
        user_id = s.loads(token, max_age=max_age)
    except:
        return None
    return user_id



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


@auth.route('/show-users', methods=['GET', 'POST'])
@login_required
@user_permissions("Admin")
def show_users():
    """
    Shows a list of all users in the system, loaded into a dynamically generated table through data_loader.js.
    Returns:
        Table with all users.
    """
    query_id = str(uuid.uuid4())  # Generate a unique id for each query.
    config = QueryConfiguration(
        id=query_id,
        model_name='user',  # The __tablename__ of the model to user.
        filters={},  # Not filtering the results, so an empty dictionary is passed.
        columns=['id', 'email', 'name'],
        user_id=current_user.id if current_user.is_authenticated else 0
    )
    db.session.add(config)
    db.session.commit()

    return render_template('home.html', title="Users", data_endpoint=f"/api/data?query_id={query_id}")





