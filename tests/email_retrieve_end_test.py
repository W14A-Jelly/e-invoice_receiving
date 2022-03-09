import requests
import json
from src.error import InputError, AccessError
from src import config

URL = f'http://127.0.0.1:{config.port}'

def test_invalid_token(clear):
    '''
    An invalid token is given. Expect an AccessError.
    '''
    request_body = {'token' : 'invalid'}
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == AccessError.code

def test_valid_case(clear, user_1):
    '''
    Test a valid case where you end an active email retrieve. Expect no errors.
    '''
    token = user_1['token']
    request_body = {'token' : token}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200

    request_body = {'token' : token}
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == 200

def test_end_no_active_retrieve(clear, user_1):
    '''
    Try to end a non active retrieve. Expect AccessError.
    '''
    token = user_1['token']

    request_body = {'token' : token}
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == AccessError.code

def test_end_two_active_retrievals(clear, user_1, user_2):
    '''
    Have two users end their own retrieve and then end it again. Expect
    AccessError when ending a non active retrieve
    '''
    token1 = user_1['token']
    token2 = user_2['token']

    request_body = {'token' : token1}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200

    request_body = {'token' : token2}
    response = requests.put(f"{URL}/email/retrieve/start", json=request_body)
    assert response.status_code == 200

    request_body = {'token' : token1}
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == 200
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == AccessError.code

    request_body = {'token' : token2}
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == 200
    response = requests.put(f"{URL}/email/retrieve/end", json=request_body)
    assert response.status_code == AccessError.code