'''
import requests
import json
from src.error import InputError, AccessError
from src import config

URL = f'http://127.0.0.1:{config.port}'


def test_invalid_token(clear):
    Provided token is invalid. Raises an AccessError.
    
    request_body = {
        'token' : 'bad',
        'query_str' : 'Hi'
    }
    response = requests.get(f"{URL}/search/v1", params=request_body)
    assert response.status_code == AccessError.code

def test_ok_for_channel(clear, one_user, new_user):
    
    Tests that messages contained in channel is returned in messages given the query.
    
    token1 = one_user['token']
    token2 = new_user['token']
    ch_id1 = create_channel(token1, 'name', True)['channel_id']
    ch_id2 = create_channel(token1, 'name1', True)['channel_id']
    
    request_body = {
        'token': token1,
        'channel_id': ch_id1,
        'message' : 'Hello'
    }
    requests.post(f'{URL}/message/send/v1', json = request_body)

    request_body = {
        'token': token1,
        'channel_id': ch_id2,
        'message' : 'Hello'
    }
    requests.post(f'{URL}/message/send/v1', json = request_body)

    request_body = {
        'token': token1,
        'channel_id': ch_id1,
        'message' : 'Hello'
    }
    requests.post(f'{URL}/message/send/v1', json = request_body)
    #checking if search for something with no result
    request_body = {
        'token' : token1,
        'query_str' : 'Hi'
    }
    response = requests.get(f"{URL}/search/v1", params=request_body)
    assert response.status_code == 200
    assert len(response.json()['messages']) == 0
    #checking partially matched string
    request_body = {
        'token' : token1,
        'query_str' : 'He'
    }
    response = requests.get(f"{URL}/search/v1", params=request_body)
    assert response.status_code == 200
    assert len(response.json()['messages']) == 3

    # checking for someone with no joined channel
    request_body = {
        'token' : token2,
        'query_str' : 'He'
    }
    response = requests.get(f"{URL}/search/v1", params=request_body)
    assert response.status_code == 200
    assert len(response.json()['messages']) == 0
'''