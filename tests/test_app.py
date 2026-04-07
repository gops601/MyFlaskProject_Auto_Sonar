import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['LOGIN_DISABLED'] = False
    with app.test_client() as client:
        yield client

# ---------------------------
# Test Login Page (GET)
# ---------------------------
def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

# ---------------------------
# Test Valid Login
# ---------------------------
def test_valid_login(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'home' in response.data or b'Home' in response.data

# ---------------------------
# Test Invalid Login
# ---------------------------
def test_invalid_login(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong'
    })

    assert b'Invalid Credentials' in response.data

# ---------------------------
# Test Protected Route (without login)
# ---------------------------
def test_home_requires_login(client):
    response = client.get('/home')
    assert response.status_code == 302  # Redirect to login

# ---------------------------
# Test Logout Flow
# ---------------------------
def test_logout(client):
    # Login first
    client.post('/login', data={
        'username': 'admin',
        'password': 'password'
    })

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200