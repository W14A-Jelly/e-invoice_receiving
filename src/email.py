import imaplib
from src.error import InputError, AccessError
from database import Database


def email_set(token, email_address, email_pass):
    # validate email can be logged into
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    login_status, acc = mail.login(email_address, email_pass)
    if login_status != 'OK':
        raise AccessError(
            'Could not update email, given credentials are invalid')

    # user_id will be extrapolated from the token
    # user_id = decode(token)

    Database.start()
    # Update database with new email and password
    updated_data = {'password': email_pass, 'email': email_address}
    Database.update('Email', user_id, updated_data)
    Database.stop()
    return {}


def email_retrieve_start(token):
    '''
    some description
    '''
    return {}


def email_validate_xml():
    # module to email_retrieve_start
    '''
    some description
    '''
    return {}


def email_output_report():
    # module to email_retrieve_start
    '''
    some description
    '''
    return {}


def email_retrieve_end(token):
    '''
    some description
    '''
    return {}
