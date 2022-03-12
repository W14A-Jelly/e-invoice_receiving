from base64 import decode
import jwt
from src.database import Database

def decode_token(token):
    '''
    This function converts a token into its corresponding user & session id

    Arguments:
    	token (encoded string) - A user jwt needs to be decode
    				  
    Return Value:
    	Returns {'user_id', 'session_id'} on success.
        If this token does not refer to a valid logged in user
        return None.
    '''
    secrete_string = 'JELLY2021'

    try:
        users = [user.user_id for user in Database.get_table('Login')]
        decode_data = jwt.decode(token, secrete_string, algorithms = ['HS256'])
        session = Database.get_id('Login', decode_data['user_id'])[0].session_id
    except:
        return None
    
    if decode_data['user_id'] in users and decode_data['session_id'] == session:
        return {'user_id': decode_data['user_id'], 
                'session_id': decode_data['session_id']}
    
    return None