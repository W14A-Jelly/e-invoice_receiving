import json
import requests
import pytest

def test_email_set(clear):
    '''
    Basic test for email_set()
    User provides their email to be used as the receiving address. Expect token to be generated correctly.
    '''
    response = requests.post(f"{url}/email/set", json = {
    "email": "user1@gmail.com",
    "password": "Strongpword1"
    })

    encode_token = generate_token(1, 1)
    assert json.loads(response.text) == {'token': encode_token}

def test_invalid_email_set(clear):
    '''
    Exception test for email_set()
    User provides an invalid email. Expect InputError.
    '''
    response = requests.post(f"{url}/email/set", json = {
    "email": "user1.com",
    "password": "Strongpword1"
    })

    assert response.status_code == 400

def test_email_set_two(clear):
    '''
    Exception test for email_set()
    User provides an email which is already in use. Expect InputError.
    '''
    response = requests.post(f"{url}/email/set", json = {
    "email": "user1@gmail.com",
    "password": "Strongpword1"
    })

    requests.delete(f"{url}/clear/v1")
    response = requests.post(f"{url}/email/set", json = {
    "email": "user1@gmail.com",
    "password": "Strongpword2"
    })
    assert response.status_code == 400
    
