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
    validate = 0
    all_email = [user.email for user in Database.get_table('Register')]
    for email in all_email: 
        if email == email_address:
            validate = 1
            match = email
            break
    # how do we get user_id from database?
    newToken = jwt.encode({'user_id': user_id, 'session_id': session_id}, SECRET_KEY, algorithm='HS256')

    for user in Database.get_table('Register'):
        if user.email == email_address:
            if user.password == password:
                validate = 1
                Database.update('Login', token_data['user_id'], {'email' : email})
    
    if validate == 0:
        raise InputError(description='Email not in the list or password is incorrect')
    
    return {'token' : 'newToken'}

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