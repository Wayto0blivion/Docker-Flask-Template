"""
@author :   Zuicie
@date   :   November 19, 2024
Actual test functions for pytest.
"""

from itsdangerous import URLSafeTimedSerializer
import pytest
from website.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def new_user(db):
    """Create a new user for testing."""
    user = User(
        email='testuser@example.com',
        username='testuser',
        name='Test User',
        password=generate_password_hash('password123', method='pbkdf2:sha256')
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_home_page(client):
    """Test that the homepage is accessible."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data  # Adjust based on home page content


def test_signup(client):
    """Test user registration."""
    response = client.post('/signup', data={
        'email': 'newuser@example.com',
        'username': 'newuser',
        'name': 'New User',
        'password': 'password123',
        'confirm_password': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # Adjust based on login page content
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None


def test_login(client, new_user):
    """Test user login."""
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data  # Adjust based on navbar or page content


def test_profile_requires_login(client):
    """Test that profile page redirects when not logged in."""
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # Should redirect to the login page


def test_profile_access(client, new_user):
    """Test accessing the profile page when logged in."""
    # Log the user in first
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123',
    }, follow_redirects=True)

    # Access the profile page
    response = client.get('/profile')
    assert response.status_code == 200
    assert b'Profile' in response.data  # Adjust based on profile page content


def test_logout(client, new_user):
    """Test user logout."""
    # Log the user in first
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123',
    }, follow_redirects=True)

    # Logout the user
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # Adjust based on login page content


def test_password_change(client, new_user):
    """Test password change."""
    # Log the user in.
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123',
    }, follow_redirects=True)

    # Change the user's password
    response = client.post('/profile', data={
        'current_password': 'password123',
        'new_password': 'test_py',
        'new_password_verify': 'test_py',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    # Log the user in using the new password.
    login_response =     client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'test_py',
    }, follow_redirects=True)
    assert login_response.status_code == 200
    assert b'Logout' in login_response.data


def test_forgot_password_get(client):
    """Ensure GET /forgot-password renders the form."""
    response = client.get('/forgot-password')
    assert response.status_code == 200
    assert b'Forgot Password' in response.data


def test_forgot_password_post_exists(client, new_user, monkeypatch):
    """Test POST /forgot-password with a valid user email."""
    # Mock out mail.send to avoid sending a real email
    def mock_send(self, msg):
        print("[MOCK] Email sent to", msg.recipients)
        assert new_user.email in msg.recipients

    monkeypatch.setattr("flask_mail.Mail.send", mock_send)

    response = client.post('/forgot-password', data={
        'email': 'testuser@example.com',
    }, follow_redirects=True)
    assert response.status_code == 200
    # The route always flashes the same message, so check for that
    assert b'If that email is in our system' in response.data


def test_forgot_password_post_doesnt_exist(client, monkeypatch):
    """Test POST /forgot-password with a non-existent user email."""
    def mock_send(self, msg):
        pytest.fail('mail.send should not be called for non-existent user')

    monkeypatch.setattr("flask_mail.Mail.send", mock_send)

    response = client.post('/forgot-password', data={
        'email': 'notreal@example.com',
    }, follow_redirects=True)
    assert response.status_code == 200
    # The same generic message is shown
    assert b'If that email is in our system' in response.data


def test_reset_password_get_valid_token(client, new_user, app):
    """Test GET /reset-password/<token> with a valid token"""
    with app.app_context():
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt="password-reset-salt")
        token = s.dumps(new_user.id)  # Generate a valid token

    response = client.get(f'/reset-password/{token}')
    assert response.status_code == 200
    assert b'Reset Password' in response.data


def test_reset_password_post_valid_token(client, new_user, app):
    """Test POST /reset-password/<token> to actually change the password."""
    with app.app_context():
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt="password-reset-salt")
        token = s.dumps(new_user.id)

    response = client.post(f'/reset-password/{token}', data={
        'new_password': 'new_secret',
        'confirm_password': 'new_secret'
    }, follow_redirects=True)

    # Verify user's password changed.
    from website.models import User
    updated_user = User.query.filter_by(id=new_user.id).first()
    from werkzeug.security import check_password_hash
    assert check_password_hash(updated_user.password, 'new_secret') is True


def test_reset_password_invalid_token(client):
    """Test GET /reset-password/<token> with invalid/expired token."""
    invalid_token = "some.invalid.token"

    response = client.get(f'/reset-password/{invalid_token}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Your reset link is invalid' in response.data






