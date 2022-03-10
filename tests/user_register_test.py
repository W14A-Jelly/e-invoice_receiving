import requests
import json
from src import config

URL = f'http://127.0.0.1:{config.port}'
# TODO make sure we create config file later
# add clear to fixture later

def register_successful(clear):
    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200
    request_body = {
        'email' : 'Goodhi@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryWoman',
    }
    response1 = requests.post(f"{URL}/user/register", json = request_body)
    assert response1.status_code == 200

    assert response.json()['token'] != response1.json()['token']

def test_register_email_invalid(clear):
    request_body = {
        'email' : 'InvalidEmail',
        'password' : 'password',
        'user_name' : 'HarryMan1',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400

    request_body = {
        'email' : 'InvalidEmail@',
        'password' : 'password',
        'user_name' : 'HarryMan2',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400

    request_body = {
        'email' : '@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan3',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400

def test_register_duplicate_email(clear):
    request_body = {
        'email' : 'Hello@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    request_body = {
        'email' : 'Hello@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan1',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    
    assert response.status_code == 400


def test_register_duplicate_username(clear):
    request_body = {
        'email' : 'Hello@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    request_body = {
        'email' : 'Hello1@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    
    assert response.status_code == 400

def test_pass_invalid(clear):
    '''
    Test when the password is more than 20 or less than 6 characters
    '''
    request_body = {
        'email' : 'good@gmail.com',
        'password' : 'ab',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400
    request_body = {
        'email' : 'good@gmail.com',
        'password' : 'a'*22,
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400

def test_register_pass_edgecase():
    '''
    Test when the password length is exactly 6 or 20, which should be registered successfully.
    '''
    request_body = {
        'email' : 'Hello1@gmail.com',
        'password' : 'a'*20,
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400

    request_body = {
        'email' : 'Hello2@gmail.com',
        'password' : 'a'*6,
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400.

