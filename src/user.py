from src.error import InputError, AccessError

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
    some description
    '''
    return {}

def user_update_password(token, password):
    '''
    some description
    '''
    return {}