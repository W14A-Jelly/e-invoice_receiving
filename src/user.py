from src.error import InputError, AccessError

import json
import requests
import pytest
import jwt
from jwt import DecodeError
SECRET_KEY = JELLY2021

def user_register(email_address, password):
    '''
    some description
    '''
    #TODO: update to work with database session_id & user_id
    #generate new session id
    #store = data_store.get()
    store['sessionTracker'] = store['sessionTracker'] + 1
    data_store.set(store)
    store['sessionTracker']
    # generate_token
    newToken = jwt.encode({'user_id': user_id, 'session_id': session_id}, SECRET_KEY, algorithm='HS256')

    #store = data_store.get()
    #users = store['users']
    reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    #check if email is valid
    if re.fullmatch(reg, email_address) is None:
        raise InputError(description='invalid email')
    
    #if new user details are valid, add them to the list of 'users'

    #new_user = {}
    #new_user['email'] = email_address
    #new_user['password'] = password
    data = {'email': email_address,'password': password}
    Database.update('Register', 0,data)

    return {'token' : newToken}

def user_login(email_address, password):
    '''
    some description
    '''
    return {'token' : 'Change this'}

def user_logout(token):
    '''
    some description
    '''
    return {}

def user_update_email(token, email):
    '''
    some description
    '''
    return {}

def user_update_password(token, password):
    '''
    some description
    '''
    return {}