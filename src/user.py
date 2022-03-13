from src.error import InputError, AccessError
from src.database import Database
from re import fullmatch

def user_register(email_address, password, ):
    '''
    some description
    '''
    return {'token' : 'Change this'}

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
    
    # TODO Get user_id
    if token == 'not valid':
        return AccessError('Invalid token')
    elif fullmatch(regex, email) == None:
        return InputError('Invalid email format')

    all_email = [user.email for user in Database.get_table('Login')]
    if email in all_email:
        raise InputError('Email address already used')
        
    Database.update('Login', token.user_id, {'email' : email})

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