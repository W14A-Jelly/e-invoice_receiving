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
    tokendecode = 

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