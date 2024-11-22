"""
@author :   Zuicie
@date   :   November 19, 2024
Actual test functions for pytest.
"""

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




