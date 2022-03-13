import json
import requests
import pytest
from src import config

url = f'http://127.0.0.1:{config.port}'

def test_invalid_email_set(clear, user_1):
    '''
    Exception test for email_set()
    User provides an invalid email. Expect InputError.
    '''
    
    response = requests.post(f"{url}/email/set", json = {
    'token' : user_1['token'],
    "email": "user1.com",
    "email_pass": "Strongpword1"
    })

    assert response.status_code == 403

def test_email_set_two(clear, user_1):
    '''
    Exception test for email_set()
    User provides an email which is already in use. Expect InputError.
    '''
    response = requests.post(f"{url}/email/set", json = {
    'token' : user_1['token'],
    "email": "user1@outlook.com",
    "email_pass": "Strongpword1"
    })

    assert response.status_code == 403
    
