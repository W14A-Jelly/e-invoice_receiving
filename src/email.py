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
    descriptions: start retrieving emails from pre-set eamail address
    parameters: token
    returns; {}
    '''
    #decode = validata_token(token)
    #user_id = decode['email_address']
    # from the database, select email_receive, password and is_retrieve from email receive
    i = Database.get_id('Email', user_id)[0]
    email_receive = i.email_retrieve
    is_retrieve = i.is_retrieve

    if is_retrieve = True():
        raise AccessError('There is an active retrieving session already')
    params = [email_receive, password, datetime.now().replace(tzinfo=timezone.utc).timestamp(),user_id]
    t = threading.Thread(help_check_inbox, params)
    t.start()
    return {}

def help_check_inbox(email_address, password,timestamp,user_id ):
    #DATABASE select is retrieve from email retrieve where email = email_address
    is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    login_status, acc = mail.login(email_address, password)
    if login_status != 'OK':
        raise AccessError('Login using given crenditial failed')
    while is_retrieve == false:
        inbox_status, data = mail.select('Inbox')
        if inbox_status != 'OK':
            raises AccessError("Cannot search inbox")
        #loop through inboxes
        for count,mid in enumerate(data[0].split())
            message_status, msg_info = mail.fetch(mid, '(RFC822)')
            #m = email.message_from_string(msg_info[0][1])
            m = email.message_from_string(msg_info[0][1])
            # Not sure if the keyword need to be Date or Time, need to makeup a gmail for further test
            if n = 0:
                # set latest email
                email_info = Database.get_id('Email',user_id)
                updated = {
                    user_id: email.info[0].user_id
                    email_retrieve: email.info[0].email_retrieve
                    password: email.info[0].password
                    latest_xml_id: mid
                    time_stamp: email.info[0].timestamp
                    is_retrieve: email.info[0].is_retrieve
                    is_comm_report = email.info[0].is_comm_report
                }
            if timestamp > m['Date']:
                Database.update('Email', user_id, updated)
                break
            if mid = Database.get_id('Email',user_id)[0].latest_xml_id:
                Database.update('Email', user_id, updated)
                break

            # Go thgouh one particular email.
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
                            rp_name =create_new(file_name)
                            if email_validate_xml(part.get_payload(decode = True)):
                                try:
                                    fp = open(fp, 'wb')
                                    fp.write(part.get_payload(decode = True))
                                    fp.close()
                                    report.update_successful(rp_name)
                                    Database.insert('Ownership', {user_id: user_id, xml_id = file_name})
                                except:
                                    report.update_unsuccessful(rp_name,'cannot save invoice')
                            else:
                                report update_unsuccessful(rp_name, 'Not UBL standard')

        #sleep(30)                       
        is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve

    mail.close()
    mail.logout()





        


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
