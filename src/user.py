from src.error import InputError, AccessError
from database import Database

def user_register(user_name, password, email_address):
    '''
    some description
    '''
    return {'token' : 'Change this'}

def user_login(user_name, password):
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

def user_update_username(token, user_name):
    '''
    some description
    '''
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
    # TODO Get user_id
    if token == 'not valid':
        return AccessError('Invalid token')
    elif not (len(password) >= 6 and len(password) <= 20):
        return InputError('Password is not between length 6 to 20 inclusive')

    Database.update('Login', token.user_id, {'password' : password})

    return {}