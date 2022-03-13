from src.error import InputError, AccessError
from src.database import Database
from src.helper import decode_token
from re import fullmatch
from src.helper import decode_token
import jwt

SECRET_KEY = 'JELLY2021'

def user_register(email_address, password):
    '''
    some description
    '''

    #store = data_store.get()
    #users = store['users']
    reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    #check if email is valid
    if fullmatch(reg, email_address) is None:
        raise InputError(description='invalid email')
    elif not (len(password) >= 6 and len(password) <= 20):
        raise InputError('Password size is not between 6 to 20 inclusive')


    #if new user details are valid, add them to the list of 'users'

    user_id = Database.num_rows('Login')
    for user in Database.get_table('Login'):
        if user.email == email_address:
            raise InputError('')

    data = {'email': email_address,'password': password, 'user_id' : user_id, 'session_id' : '0'}
    
    Database.insert('Login', data)
    # generate_token
    newToken = jwt.encode({'user_id': user_id, 'session_id': '0'}, SECRET_KEY, algorithm='HS256')

    return {'token' : newToken}

def user_login(email_address, password):
    '''
    some description
    '''
    session = ''
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

    if session == '':
        session += '0'
    else: 
        session = ' ' + str(int(session.split()[-1]) + 1)

    if validate == 0:
        raise InputError(description='Email not in the list or password is incorrect')

    Database.update('Login', userID, {'session_id' : session})

    newToken = jwt.encode({'user_id': userID, 'session_id': session}, SECRET_KEY, algorithm='HS256')
    return {'token' : newToken}

def user_logout(token):
    '''
    some description
    '''
    token_data = decode_token(token)
    if token_data == None:
        raise AccessError('Invalid token')

    user = Database.get_id('Login', token_data['user_id'])[0]
    session = user.session_id
    sessionList = session.split()

    sessionList.remove(session)
    new_session_id = ' '.join(sessionList)

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
        raise AccessError('Invalid token')
    elif fullmatch(regex, email) == None:
        raise InputError('Invalid email format')

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
        raise AccessError('Invalid token')
    elif not (len(password) >= 6 and len(password) <= 20):
        raise InputError('Password is not between length 6 to 20 inclusive')

    Database.update('Login', token_data['user_id'], {'password' : password})

    return {}