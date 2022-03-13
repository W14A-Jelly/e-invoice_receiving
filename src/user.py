from src.error import InputError, AccessError
from src.database import Database
from src.helper import decode_token
from re import fullmatch
from src.helper import decode_token

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
    validate = 0
    all_email = [user.email for user in Database.get_table('Login')]
    for email in all_email: 
        if email == email_address:
            validate = 1
            break
 
    for user in Database.get_table('Login'):
        if user.email == email_address:
            if user.password == password:
                validate = 1
                session = user.session_id
                userID = user.user_id
                Database.update('Login', userID, {'email' : email})
                break
    
    if validate == 0:
        raise InputError(description='Email not in the list or password is incorrect')

    newToken = jwt.encode({'user_id': userID, 'session_id': session}, SECRET_KEY, algorithm='HS256')
    return {'token' : newToken}

def user_logout(token):
    '''
    some description
    '''
    token_data = decode_token(token)
    if token_data == None:
        return AccessError('Invalid token')

    for user in Database.get_table('Login'):
        if user.user_id == token_data['user_id']:
            sessions = user.session_id
            sessionList = sessions.split(' ', 1)
            break
    i = 0
    for num in sessionList:        
        if num == token_data['session_id']:
            new_session_id = sessionList.pop(i)
            break
        i+=1
    Database.update('Login', token_data['user_id'], {'session_id' : new_session_id})


    return {}

def user_update_email(token, email):
    '''
    Change pre-existing email to the the given email.

    Arguments:
        token (string) - An encoded string.
        email (string) - Valid email structure with @.

    Exceptions:
        AccessError: Invalid token.
        InputError: Invalid email format, Email address already used.

    Return Value:
        Returns an empty dictionary on successful request.
    '''
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    
    token_data = decode_token(token)
    if token_data == None:
        return AccessError('Invalid token')
    elif fullmatch(regex, email) == None:
        return InputError('Invalid email format')

    all_email = [user.email for user in Database.get_table('Login')]
    if email in all_email:
        raise InputError('Email address already used')
        
    Database.update('Login', token_data['user_id'], {'email' : email})

    return {}

def user_update_password(token, password):
    '''
    Change pre-existing password to the the given password.

    Arguments:
        token (string) - An encoded string.
        password (string) - 6 to 20 character long string inclusive.

    Exceptions:
        AccessError: Invalid token.
        InputError: Password is not between length 6 to 20 inclusive.

    Return Value:
        Returns an empty dictionary on successful request.

    '''
    token_data = decode_token(token)
    if token_data == None:
        return AccessError('Invalid token')
    elif not (len(password) >= 6 and len(password) <= 20):
        return InputError('Password is not between length 6 to 20 inclusive')

    Database.update('Login', token_data['user_id'], {'password' : password})

    return {}