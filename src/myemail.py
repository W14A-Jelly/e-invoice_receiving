from audioop import reverse
#from multiprocessing.reduction import duplicate
from src import blacklist
from src.error import InputError, AccessError
import imaplib
import base64
import os
import email
import threading
from datetime import datetime, timedelta, timezone
from imbox import Imbox
from src import report
from src.database import Database
from src.helper import decode_token, validate_xml, is_duplicate
from lxml import etree
from email.utils import parsedate_tz, mktime_tz
import os
import pytz
from src.blacklist import *

from bs4 import BeautifulSoup
from src.render import render_invoice


def email_set(token, email_address, email_pass):
    # validate email can be logged into
    # host = imaplib.IMAP4_SSL("imap.gmail.com")

    decode_data = decode_token(token)
    if decode_data == None:
        raise AccessError('Invalid token')

    try:
        host = "imap.gmail.com"
        mail = Imbox(host, username=email_address, password=email_pass,
                     ssl=True, ssl_context=None, starttls=False)
        mail.logout
        # login_status, acc = mail.login(email_address, email_pass)
    except:
        raise AccessError(
            'Could not update email, given credentials are invalid')
    '''
    if login_status != 'OK':
        raise AccessError(
            'Could not update email, given credentials are invalid')
            '''
    # Update database with new email and password
    user_id = decode_token(token)['user_id']

    if len(Database.get_id('Email', decode_data['user_id'])) == 0:
        insert_data = {'user_id': decode_data['user_id'],
                       'password': email_pass,
                       'email_receive': email_address,
                       'latest_xml_id': ' ',
                       'time_stamp': datetime.now(),
                       'is_retrieve': False,
                       'is_comm_report': False
                       }
        Database.insert('Email', insert_data)

    updated_data = {'password': email_pass, 'email_receive': email_address}
    Database.update('Email', user_id, updated_data)
    return {}


def email_retrieve_start(token):
    '''
    descriptions: start retrieving emails from pre-set eamail address
    parameters: token
    returns; {}
    '''
    decode = decode_token(token)
    if decode == None:
        raise AccessError('Bad token')
    user_id = decode['user_id']
    # from the database, select email_receive, password and is_retrieve from email receive
    i = Database.get_id('Email', user_id)[0]
    email_address = i.email_receive
    is_retrieve = i.is_retrieve
    password = i.password

    if is_retrieve == True:
        raise AccessError('There is an active retrieving session already')
    params = [email_address, password, datetime.now(
        pytz.timezone('Australia/Sydney')).timestamp(), user_id, token]
    Database.update('Email', user_id, {'is_retrieve': True})
    t = threading.Thread(target=retrival2, args=params)
    t.start()
    return {}


'''
def help_check_inbox(email_address, password,timestamp,user_id ):
    # DATABASE select is retrieve from email retrieve where email = email_address
    is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    login_status, acc = mail.login(email_address, password)
    if login_status != 'OK':
        raise AccessError('Login using given crenditial failed')
    while is_retrieve == True:
        inbox_status, data = mail.select('Inbox')
        if inbox_status != 'OK':
            raise AccessError("Cannot search inbox")
        # loop through inboxes
        for count,mid in enumerate(data[0].split())
            message_status, msg_info = mail.fetch(mid, '(RFC822)')
            # m = email.message_from_string(msg_info[0][1])
            m = email.message_from_string(msg_info[0][1])
            # Not sure if the keyword need to be Date or Time, need to makeup a gmail for further test
            if n == 0:
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
            if mid == Database.get_id('Email',user_id)[0].latest_xml_id:
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
                    fp = os.path.join(os.getcwd(),'invoices',
                                      str(user_id),file_name)
                    if not os.path.isfile(fp):
                        # attatchment type checking
                        if 'xml' in part.get_payload()[1].get_content_type():
                            rp_name =create_new(file_name)
                            if validate_xml(part.get_payload(decode = True)):
                                try:
                                    fp = open(fp, 'wb')
                                    fp.write(part.get_payload(decode = True))
                                    fp.close()
                                    report.update_successful(rp_name)
                                    Database.insert('Ownership', {user_id: user_id, xml_id = file_name})
                                except:
                                    report.update_unsuccessful(
                                        rp_name,'cannot save invoice')
                            else:
                                report.update_unsuccessful(
                                    rp_name, 'Not UBL standard')

        # sleep(30)
        is_retrieve = Database.get_id('Email', user_id)[0].is_retrieve

    mail.close()
    mail.logout()
'''


def retrival2(email_address, password, timestamp, user_id, token):

    while (Database.get_id('Email', user_id)[0].is_retrieve):
        host = "imap.gmail.com"
        try:
            mail = Imbox(host, username=email_address, password=password,
                         ssl=True, ssl_context=None, starttls=False)
        except:
            raise AccessError("cannot login with given crenditial")

        mail_messages = mail.messages(unread=True)

        m = {'m_id': [],
             'message': []}
        i = 0
        for m_id, message in mail_messages:
            m['m_id'] = [m_id, *m['m_id']]
            m['message'] = [message, *m['message']]
            i += 1

        for x in range(i):
            m_id = m['m_id'][x]
            message = m['message'][x]
            mail.mark_seen(m_id)
            message_time = mktime_tz(parsedate_tz(message.date))
            if timestamp > message_time:
                break
            # sender's email
            email = message.sent_from[0]['email']
            update_senders_table(user_id, email)
            # does the user have their spam filter enabled
            spam_filter = is_spam_filter_on(user_id)
            # is the sender blacklisted
            blacklisted = is_blacklisted(user_id, email)
            if not blacklisted:
                for attachment in message.attachments:
                    if 'xml' in attachment['content-type']:
                        file_name = attachment['filename']
                        rp_name = report.create_new(file_name)
                        data = attachment.get('content').read()
                        fp = os.path.join(os.getcwd(), 'invoices',
                                          f"{user_id}_{attachment['filename']}")

                        d_successful = False
                        try:
                            with open(fp, 'wb') as f:
                                f.write(data)

                            d_successful = True
                        except:
                            param = "%s Failed to save" % (
                                attachment['filename'])
                            report.update_unsuccessful(rp_name, param)
                            report.email_error_report(
                                fp, rp_name, email, email_address)
                        if d_successful == True:
                            valid = validate_xml(fp)
                            if valid == False:
                                param = "%s Not UBL standard" % (
                                    attachment['filename'])
                                report.update_unsuccessful(rp_name, param)
                                report.email_error_report(
                                    fp, rp_name, email, email_address)
                                if spam_filter:
                                    increment_invalid_counter(user_id, email)
                                    if check_exceeds_spam_limit(user_id, email):
                                        t = threading.Thread(target=time_out_sender, args=[
                                            token, email, email_address])
                                        t.start()

                                os.remove(fp)
                            elif is_duplicate(user_id, f"invoices/{user_id}_{attachment['filename']}"):
                                # If duplicate continues as normal, however file name will say duplicate

                                d_file_name = attachment['filename'].replace(
                                    ".xml", ".xml")
                                new_fp = os.path.join(os.getcwd(), 'invoices',
                                                      f"{user_id}_{d_file_name}")
                                os.rename(
                                    fp, new_fp)
                                report.update_successful(rp_name)
                                info = xml_extract(new_fp)
                                data = {
                                    'user_id': user_id, 'xml_id': d_file_name, 'sender': info['sender'], 'time': info['time'], 'price': info['price']}
                                Database.insert('Ownership', data)
                                render_invoice(f"{user_id}_{d_file_name}")
                                # Duplicate will be processed before user is balacklisted
                                if spam_filter:
                                    increment_duplicate_counter(user_id, email)
                                    if check_exceeds_spam_limit(user_id, email):
                                        t = threading.Thread(target=time_out_sender, args=[
                                            token, email, email_address])
                                        t.start()
                            else:
                                report.update_successful(rp_name)
                                info = xml_extract(fp)
                                data = {
                                    'user_id': user_id, 'xml_id': attachment['filename'], 'sender': info['sender'], 'time': info['time'], 'price': info['price']}
                                Database.insert('Ownership', data)
                                render_invoice(
                                    f"{user_id}_{attachment['filename']}")
            else:
                print("%s is blacklisted" % (email))


'''
                    else:
                        report.update_unsuccessful(rp_name, f'%s Not UBL standard', attachment['filename'])'''


def email_retrieve_end(token):
    '''
    description: Stop retrieving xml for the given token user
    parameter:{token}
    return value: {reports: []}
    '''
    decode = decode_token(token)
    if decode == None:
        raise AccessError('bad token')
    user_id = decode['user_id']
    email_info = Database.get_id('Email', user_id)
    if email_info == []:
        raise AccessError(
            "The user has no email credential for retrieving emails from")
    elif email_info[0].is_retrieve == False:
        raise AccessError("There is no active retrieving process")
    else:
        updated = {
            'user_id': email_info[0].user_id,
            'email_receive': email_info[0].email_receive,
            'password': email_info[0].password,
            'latest_xml_id': email_info[0].latest_xml_id,
            'time_stamp': email_info[0].time_stamp,
            'is_retrieve': False,
            'is_comm_report': email_info[0].is_comm_report}

        Database.update('Email', user_id, updated)
        reports = report.return_reports()
    return {'reports': reports}


def xml_extract(path_to_file):
    '''
    given a path. This file extract supplier, issued date and price from the given invoice file path
    '''
    with open(path_to_file) as fp:
        soup = BeautifulSoup(fp, features='xml')

    supplier = soup.find(name='cac:AccountingSupplierParty')
    supplier = supplier.find(name='cac:Party')
    supplier = supplier.find(name='cac:PartyName')
    supplier = supplier.find(name='cbc:Name')
    supplier = str(supplier.contents[0])

    time = soup.find(name='cbc:IssueDate')
    time = str(time.contents[0])
    datetime_object = datetime.strptime(time, '%Y-%m-%d').date()

    price = soup.find(name='cac:LegalMonetaryTotal')
    price = price.find(name='cbc:TaxInclusiveAmount')
    price = float(price.contents[0])

    return ({'sender': supplier, 'time': datetime_object, 'price': price})


if __name__ == "__main__":
    print(validate_xml("invoices/example1.xml"))
