
from src.error import InputError, AccessError
import imaplib
import base64
import os
import email
import threading
from datetime import datetime, timedelta, timezone
from imbox import Imbox
=======
# from error import InputError, AccessError
from lxml import etree
import os



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
    decode = decode_token(token)
    if decode = None:
        raise AccessError('Bad token')
    user_id = decode['email_address']
    # from the database, select email_receive, password and is_retrieve from email receive
    i = Database.get_id('Email', user_id)[0]
    email_receive = i.email_retrieve
    is_retrieve = i.is_retrieve

    if is_retrieve = True():
        raise AccessError('There is an active retrieving session already')
    params = [email_receive, password, datetime.now().replace(tzinfo=timezone.utc).timestamp(),user_id]
    t = threading.Thread(retrival2, params)
    t.start()
    return {}


def help_check_inbox(email_address, password,timestamp,user_id ):
    #DATABASE select is retrieve from email retrieve where email = email_address
    is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    login_status, acc = mail.login(email_address, password)
    if login_status != 'OK':
        raise AccessError('Login using given crenditial failed')
    while is_retrieve == True:
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
            if timestamp > m['Date'].replace(tzinfo=timezone.utc).timestamp():
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
                                report.update_unsuccessful(rp_name, 'Not UBL standard')

        #sleep(30)                       
        is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve

    mail.close()
    mail.logout()


def retrival2(email_address, password,timestamp,user_id):
    is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve
    while is_retrieve == True:
        host = "imap.gmail.com"
        try:
            mail = Imbox(host,username = email_address, password = password, ssl = True, ssl_context = None, starttls = False)
        except:
            raise AccessError("cannot login with given crenditial")

        mail_messages = imbox.messages(unread = True)

        for (m_id, message) in mail_messages:
            if timestamp > message.date.replace(tzinfo=timezone.utc).timestamp():
                break
            for attachment in message.attachments:
                if 'xml' in attachment['content-type']:
                    rp_name = create_new(file_name)
                    data = attachment.get('content').read()
                    fp = os.path.join(os.getcwd(),'invoices', str(user_id),attachment['filename'])
                    d_successful = False
                    try:
                        f = open(fp,'wb')
                        f.write(data)
                        f.close()
                        Database.insert('Ownership', {user_id: user_id, xml_id = file_name})
                        d_successful = True
                    except:
                        report.update_unsuccessful(rp_name, f'failed to save %s',attachment['filename'])
                    if d_successful == True:
                        valid = email_validate_xml(fp)
                        if valid == False:
                            report.update_unsuccessful(rp_name, f'%s Not UBL standard', attachment['filename'])
                            os.remove(fp)
                        else:
                            report.update_successful(rp_name)



        is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve


        
'''
                    else:
                        report.update_unsuccessful(rp_name, f'%s Not UBL standard', attachment['filename'])'''


def email_validate_xml(path_to_invoice):

    # Validate well-formedness, if invalid remove xml from invoices
    try:
        invoice_root = etree.parse(path_to_invoice)

    except etree.XMLSyntaxError:
        os.remove(path_to_invoice)
        return False


    '''
    # Validate against schema, if invalid remove xml from invoices
    schema_root = etree.parse('src/xmlschema.xsl')
    xmlschema = etree.XMLSchema(schema_root)
    try:
        xmlschema.assertValid(invoice_root)

    except etree.DocumentInvalid:
        os.remove(path_to_invoice)
        return False
    '''
    return True


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
    print(email_validate_xml('invoices/example1.xml'))
