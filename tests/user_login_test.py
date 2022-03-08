import requests
import json
from src import config

URL = f'http://127.0.0.1:{config.port}'
# TODO make sure we create config file later
# add clear to fixture later
def test_help_create_user():
    '''
    This function only register a user for following login test to use
    '''
    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200

def test_successful_login():
    request_body = {
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response1 = requests.post(f"{URL}/user/login", json = request_body)
    response2 = requests.post(f"{URL}/user/login", json = request_body)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()['token'] != response2.json()['token']

def test_username_not_exist():
    '''
    Test the case where the user name is not registerd
    '''
    request_body = {
        'password' : 'password',
        'user_name' : 'Notexist',
    }
    response = requests.post(f"{URL}/user/login", json = request_body)
    assert response.status_code == 400

def test_pass_nomatch():
    '''
    Test the case where the password is wrong for existing user
    '''
    request_body = {
        'password' : 'Iforgotit',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/login", json = request_body)
    assert response.status_code == 400
