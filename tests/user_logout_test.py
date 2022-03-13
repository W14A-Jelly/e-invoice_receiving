import requests
import json
from src import config

URL = f'http://127.0.0.1:{config.port}'

def test_invalid_token(clear):
    '''
    Given invalid token to API
    '''
    request_body = {
        'token' : 'Notgood'
    }
    response = requests.post(f"{URL}/user/logout", json = request_body)
    assert response.status_code == 403

def logout_twice(clear):
    '''
    log out twice. After first logout the token should be deactivated
    Then the second logout should fail.
    '''

    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
        'user_name' : 'HarryMan',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    token = response.json()['token']
    request_body = {
        'token' : token
    }
    response = requests.post(f"{URL}/user/logout", json = request_body)
    assert response.status_code == 200
    response = requests.post(f"{URL}/user/logout", json = request_body)
    assert response.status_code == 403
