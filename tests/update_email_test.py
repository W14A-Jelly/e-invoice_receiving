import requests
import json
from src.error import InputError, AccessError
from src import config

URL = f'http://127.0.0.1:{config.port}'

# Http test file for update email:

def test_update_email_valid_input(clear):
    '''
    Update an email correctly. Expect no errors.
    '''
    # Register a user
    request_body1 = {
        'email' : 'test@gmail.com',
        'password' : 'test1234',
    }
    response1 = requests.post(f"{URL}/user/register", json=request_body1)
    # Update their email
    request_body2 = {
        'token' : response1.json()['token'],
        'email' : 'testchange@gmail.com',
    }
    response2 = requests.put(f"{URL}/user/update/email", params=request_body2)
    # Empty dictionary is returned
    assert not response2.json()

def test_update_email_same_email(clear):
    '''
    Update email with the same email. Expect InputError.
    '''
    # Register a user
    request_body1 = {
        'email' : 'test@gmail.com',
        'password' : 'test1234',
    }
    response1 = requests.post(f"{URL}/user/register", json=request_body1)
    # Update their email to same email as before
    request_body2 = {
        'token' : response1.json()['token'],
        'email' : 'test@gmail.com',
    }
    response2 = requests.put(f"{URL}/user/update/email", params=request_body2)
    # Input Error
    assert response2.status_code == InputError.code

def test_update_email_already_exists(clear):
    '''
    Update email with an registered email. Expect InputError.
    '''
    # Register a user
    request_body1 = {
        'email' : 'test@gmail.com',
        'password' : 'test1234',
    }
    response1 = requests.post(f"{URL}/user/register", json=request_body1)
    # Register a 2nd user
    request_body2 = {
        'email' : 'testInUse@gmail.com',
        'password' : 'test1234',
    }
    response2 = requests.post(f"{URL}/user/register", json=request_body2)
    # Update their email to email of second user
    request_body3 = {
        'token' : response1.json()['token'],
        'email' : 'testInUse@gmail.com',
    }
    response3 = requests.put(f"{URL}/user/update/email", params=request_body3)
    # Input Error
    assert response3.status_code == InputError.code

def test_update_email_bad_token(clear):
    '''
    Update an email with an invalid token. Expect AccessError.
    '''
    # Update an email with invalid token
    request_body = {
        'token' : 'badtoken',
        'email' : 'testupdate@gmail.com',
    }
    response = requests.put(f"{URL}/user/update/email", params=request_body)
    # Input Error
    assert response.status_code == AccessError.code


