import requests
import json
from src.error import InputError, AccessError
from src import config

URL = f'http://127.0.0.1:{config.port}'

# Http test file for update password:

def test_update_password_valid_input(clear):
    '''
    Update password correctly. Expect no errors.
    '''
    # Register a user
    request_body1 = {
        'email' : 'test@gmail.com',
        'password' : 'test1234',
    }
    response1 = requests.post(f"{URL}/user/register", json=request_body1)
    # Update their password
    request_body2 = {
        'token' : response1.json()['token'],
        'password' : 'testchange',
    }
    response2 = requests.put(f"{URL}/user/update/password", params=request_body2)
    # Empty dictionary is returned
    assert not response2.json()

def test_update_password_too_long(clear):
    '''
    Update password over 20 chars. Expect InputError.
    '''
    # Register a user
    request_body1 = {
        'email' : 'test@gmail.com',
        'password' : 'test1234',
    }
    response1 = requests.post(f"{URL}/user/register", json=request_body1)
    # Update their password to password greater than 20 characters
    request_body2 = {
        'token' : response1.json()['token'],
        'password' : '1233456789123456789123456789',
    }
    response2 = requests.put(f"{URL}/user/update/password", params=request_body2)
    # Input Error
    assert response2.status_code == InputError.code

def test_update_password_too_short(clear):
    '''
    Update password under 6 chars. Expect InputError.
    '''
    # Register a user
    request_body1 = {
        'email' : 'test@gmail.com',
        'password' : 'test1234',
    }
    response1 = requests.post(f"{URL}/user/register", json=request_body1)
    # Update their password to password less than 6 characters
    request_body2 = {
        'token' : response1.json()['token'],
        'password' : '1',
    }
    response2 = requests.put(f"{URL}/user/update/password", params=request_body2)
    # Input Error
    assert response2.status_code == InputError.code

def test_update_password_bad_token(clear):
    '''
    Update password with invalid token. Expect AccessError.
    '''
    # Update an email with invalid token
    request_body = {
        'token' : 'badtoken',
        'password' : 'test1234',
    }
    response = requests.put(f"{URL}/user/update/password", params=request_body)
    # Input Error
    assert response.status_code == AccessError.code


