import requests
import json
from src.error import InputError, AccessError
from src import config

URL = f'http://127.0.0.1:{config.port}'

def test_valid_token(clear, user_1):
    '''
    Test a valid case. Expect no errors.
    '''
    token = user_1['token']
    request_body = {'token' : token}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200

def test_invalid_token(clear):
    '''
    An invalid token is given. Expect an AccessError.
    '''
    request_body = {'token' : 'invalid'}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == AccessError.code

def test_activate_active_retrieve(clear, user_1):
    '''
    While retrieve process is active, try to activate it again. 
    Expect AccessError.
    '''
    token = user_1['token']
    request_body = {'token' : token}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200

    request_body = {'token' : token}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == AccessError.code

def test_two_active_retrievals(clear, user_1, user_2):
    '''
    Have two users start retrieve. Expect no errors.
    '''
    token1 = user_1['token']
    token2 = user_2['token']

    request_body = {'token' : token1}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200

    request_body = {'token' : token2}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200