import requests
import json
from src.error import InputError
import requests
import json
from src.error import InputError
from src import config

URL = f'http://127.0.0.1:{config.port}'

def test_clear_register(clear):
    '''
    Register a user, clear, then register the same user. Expect no errors.
    '''
    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200
    
    requests.delete(f"{URL}/clear", json = {'admin_pass' : 'Jelly2022'})
    
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200
    
def test_clear_login(clear):
    '''
    Register a user, clear, then login the same user. Expect InputError.
    '''
    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200
    
    requests.delete(f"{URL}/clear", json = {'admin_pass' : 'Jelly2022'})
    
    response = requests.post(f"{URL}/user/login", json = request_body)
    assert response.status_code == InputError.code


def test_not_authorised_clear(clear):
    request_body = {
        'email' : 'Good@gmail.com',
        'password' : 'password',
    }
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 200
    r = requests.delete(f"{URL}/clear")
    assert r.status_code == 403
    response = requests.post(f"{URL}/user/register", json = request_body)
    assert response.status_code == 400
