import imaplib
import helper
from error import InputError, AccessError
from database import Database


def email_set(token, email_address, email_pass):
    # validate email can be logged into
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    login_status, acc = mail.login(email_address, email_pass)
    if login_status != 'OK':
        raise AccessError(
            'Could not update email, given credentials are invalid')
    # Update database with new email and password
    user_id = helper.decode_token(token)['user_id']
    Database.start()
    updated_data = {'password': email_pass, 'email_receive': email_address}
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


if __name__ == '__main__':
    Database.start()
    Database.drop_tables()
    Database.create_tables()
    login_data = {'password': 'password',
                  'email': 'exmaple@gmail.com',
                  'session_id': '0 1',
                  'user_id': 0}

    Database.insert('Login', login_data)
    data = {'user_id': '0',
            'email_receive': 'test@gmail.com',
            'password': 'test1234',
            'latest_xml_id': 'xml_000',
            'time_stamp': '1:24pm',
            'is_retrieve': 'True',
            'is_comm_report': 'True'
            }
    Database.insert('Email', data)
    Database.print_table('Email')
    updated_data = {'email_receive': 'testchanged@gmail.com',
                    'password': 'testchanged'}
    Database.update('Email', 0, updated_data)
    Database.print_table('Email')
