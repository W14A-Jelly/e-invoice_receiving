import requests
import pytest
from src import config

URL = f'http://127.0.0.1:{config.port}'

@pytest.fixture
def clear():
    '''
    Clears database data
    '''
    requests.delete(f"{URL}/clear")

@pytest.fixture
def user_1():
    '''
    Register 1st user with a valid email for invoice retrieval
    '''
    valid_email = 'einvoice.retrieve@gmail.com'
    email_pass = 'tqgj frum fezi kizp'

    # Register user1
    request_body = {
                    'password' : 'password',
                    'email' : 'example1@gmail.com'}
    register = requests.post(f"{URL}/user/register", json=request_body)
    assert register.status_code == 200
    token = register.json()['token']

    # Set email for user1
    request_body = {
                    'token' : token,
                    'email' : valid_email,
                    'email_pass' : email_pass}
    register = requests.post(f"{URL}/email/set", json=request_body)
    assert register.status_code == 200

    return {'token' : token}

@pytest.fixture
def user_2():
    '''
    Register 2nd user with a valid email for invoice retrieval
    '''
    valid_email = 'einvoice.retrieve2@gmail.com'
    email_pass = 'pyla htli bgft lonr'

    # Register user2
    request_body = {
                    'password' : 'password',
                    'email' : 'example2@gmail.com'}
    register = requests.post(f"{URL}/user/register", json=request_body)
    assert register.status_code == 200
    token = register.json()['token']

    # Set email for user2
    request_body = {
                    'token' : token,
                    'email' : valid_email,
                    'email_pass' : email_pass}
    register = requests.post(f"{URL}/email/set", json=request_body)
    assert register.status_code == 200

    return {'token' : token}