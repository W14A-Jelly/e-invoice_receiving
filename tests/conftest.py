import pytest
import requests
import json
from src import config

URL = f'http://127.0.0.1:{config.port}'

@pytest.fixture
def clear():
    requests.delete(f"{URL}/clear")

@pytest.fixture
def user_1():
    '''
    Register 1st user with a valid email for retrieval
    '''
    valid_email = 'einvoice.retrieve@gmail.com'
    email_pass = 'retrieve@jelly'

    # Register user1
    request_body = {
                'user_name' : 'user1',
                'password' : 'password',
                'email_address' : 'example1@gmail.com'
                }
    register = requests.post(f"{URL}/user/register", json=request_body)
    assert register.status_code == 200
    token = register.json()['token']

    # Email set
    request_body = {
                    'token' : token,
                    'email_address' : valid_email,
                    'email_pass' : email_pass
                    }
    email_set = requests.post(f"{URL}/email/set", json=request_body)
    assert email_set.status_code == 200

    return {'token': token}

@pytest.fixture
def user_2():
    '''
    Register 2nd user with a valid email for retrieval
    '''
    valid_email = 'einvoice.retrieve2@outlook.com'
    email_pass = 'retrieve2@jelly'

    # Register user2
    request_body = {
                'user_name' : 'user2',
                'password' : 'password',
                'email_address' : 'example2@gmail.com'
                }
    register = requests.post(f"{URL}/user/register", json=request_body)
    assert register.status_code == 200
    token = register.json()['token']

    # Email set
    request_body = {
                    'token' : token,
                    'email_address' : valid_email,
                    'email_pass' : email_pass
                    }
    email_set = requests.post(f"{URL}/email/set", json=request_body)
    assert email_set.status_code == 200

    return {'token': token}