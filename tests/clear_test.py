import pytest
from src.other import clear

from src.error import InputError
from src.error import AccessError

from src.data_store import data_store

def test_clear_database():
    register_data = {
        'email_address' : 'user1@gmail.com',
        'password' : 'Strongpassword',
        'session_id' : '0 1',
        'user_id' : 1
    }
    userData = {'email' : 'user1@gmail.com', 'password' : 'Strongpassword'}
    Database.update('Register', 0, userData)

    logoutData = {'email' : 'user1@gmail.com'}
    Database.update('Logout', 0, logoutData)

    Database.update('Login', 0 , userData)
    assert response.status_code == AccessError.code