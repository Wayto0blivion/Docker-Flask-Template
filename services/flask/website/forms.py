"""
@author : Zuicie
@date : 2024-10-20
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length


class LoginForm(FlaskForm):
    """
    Allows a current user to login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """
    Allows a new user to register.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class UserProfileForm(FlaskForm):
    """
    Allows a user to edit their own profile.
    """
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Length(min=7, message='Password is too short!')])
    new_password_verify = PasswordField('New Password (Verify)', validators=[InputRequired(),
                                                                    EqualTo('new_password',
                                                                            message='Password Mismatch!')])
    submit = SubmitField('Reset Password')

