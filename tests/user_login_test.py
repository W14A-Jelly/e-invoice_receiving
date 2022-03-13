import requests
import json
from src import config

URL = f'http://127.0.0.1:{config.port}'
# TODO make sure we create config file later
# add clear to fixture later
def test_help_create_user(clear):
    '''
    This function only register a user for following login test to use
    '''
    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200

def test_successful_login(clear):
    '''
    Test successful login. Expect no errors.
    '''
    request_body = {
        'password' : 'password',
        'email' : 'Good@gmail.com',
    }
    response1 = requests.post(f"{URL}/user/login", json = request_body)
    response2 = requests.post(f"{URL}/user/login", json = request_body)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()['token'] != response2.json()['token']

def test_email_not_exist(clear):
    '''
    Test the case where the email is not registerd
    '''
    request_body = {
        'password' : 'password',
        'email' : 'Notexist@gmail.com',
    }
    response = requests.post(f"{URL}/user/login", json = request_body)
    assert response.status_code == 400

def test_pass_nomatch(clear):
    '''
    Test the case where the password is wrong for existing user
    '''
    request_body = {
        'password' : 'Iforgotit',
        'email' : 'Good@gmail.com',
    }
    response = requests.post(f"{URL}/user/login", json = request_body)
    assert response.status_code == 400
