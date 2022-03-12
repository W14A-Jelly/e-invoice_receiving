from src.error import InputError, AccessError
import imaplib
import base64
import os
import email
import threading
from datetime import datetime, timedelta, timezone
def email_set(token, email_address, email_pass):
    '''
    some description
    '''
    return {}

def email_retrieve_start(token):
    '''
    some description
    '''
    #decode = validata_token(token)
    #user_id = decode['email_address']
    # from the database, select email_receive, password and is_retrieve from email receive
    email_receive 
    is_retrieve 

    if is_retrieve = True():
        raise AccessError('There is an active retrieving session already')
    params = [email_receive, password, datetime.now().replace(tzinfo=timezone.utc).timestamp()]
    t = threading.Thread(help_check_inbox, params)
    t.start()
    return {}

def help_check_inbox(email_address, password,timestamp,user_id ):
    #DATABASE select user_id from email receive where email_receive = email_address
    #DATABASE select is retrieve from email retrieve where email = email_address
    #TODO: figure out what I need to put in comms.
    successful_invoice = []
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    login_status, acc = mail.login(email_address, password)
    if login_status != 'OK':
        raise AccessError('Login using given crenditial failed')
    while is_retrieve == false:
        inbox_status, data = mail.select('Inbox')
        if inbox_status != 'OK':
            raises AccessError("Cannot search inbox")
        #loop through inboxes
        for mid in data[0].split()
            message_status, msg_info = mail.fetch(mid, '(RFC822)')
            #m = email.message_from_string(msg_info[0][1])
            m = email.message_from_string(msg_info[0][1])
            # Not sure if the keyword need to be Date or Time, need to makeup a gmail for further test
            if timestamp > m['Date'] :
                break
            # Go thgouh one particular.
            for part in m.walk():
                if part.get_content_maintype() == 'multipart':
                    pass
                elif part.get('Content-Disposition') is None:
                    pass
                else:
                    file_name = part.get_filename()

                if bool(file_name):
                    # make sure invoice directory is created when the server is running.
                    fp = os.path.join(os.getcwd(),'invoices', str(user_id),file_name)
                    if not os.path.isfile(fp):
                        # attatchment type checking
                        if 'xml' in part.get_payload()[1].get_content_type():
                            fp = open(fp, 'wb')
                            fp.write(part.get_payload(decode = True))
                            fp.close()
                            successful_invoice.append(file_name)
                        else: 
                            pass
                        #DATABASE: store (file_name,user_id) into Invoice Ownership
        #DATABASE select is retrieve from email retrieve where email = email_address
    mail.close()
    mail.logout()
    #TODO: call report output and give successful_invoice to it





        


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
    description: Stop retrieving xml for the given token user
    parameter:{token}
    return value: {}
    '''
    #decode = validata_token(token)
    #user_id = decode['email_address']
    email_info = Database.get_id('Email',user_id)
    if email_info == []:
        raise AccessError("The user has no email credential for retrieving emails from")
    elif email_info[0].is_retrieve == False:
        raise AccessError("There is no active retrieving process")
    else:
        email.info[0].is_retrieve = True
        updated = {
            user_id: email.info[0].user_id
            email_retrieve: email.info[0].email_retrieve
            password: email.info[0].password
            latest_xml_id: email.info[0].latest_xml_id
            time_stamp: email.info[0].timestamp
            is_retrieve: False
            is_comm_report = email.info[0].is_comm_report


        }
        Database.update('Email', user_id, email_info[0])
    return {}
