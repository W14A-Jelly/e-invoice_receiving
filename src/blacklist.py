from multiprocessing.reduction import duplicate
from posixpath import split
from src.helper import decode_token
from src.database import Database
from src.schema import Blacklist, Login, Senders
from src.error import InputError
import os
import hashlib

# Max number of duplicate/invalid files able to be sent before being blacklisted
DUPLICATE_LIMIT = 10
INVALID_LIMIT = 10


def blacklist_add(token, email):
    user_id = decode_token(token)['user_id']
    # Check if email is already blacklisted by user
    blacklist_table_rows = Database.get_id('Blacklist', user_id)
    for row in blacklist_table_rows:
        if (row.ignore == email):
            raise InputError('Email has already been blacklisted')
    # Adds given email to blacklist in database
    data = {
        'user_id': user_id,
        'ignore': email
    }
    Database.insert('Blacklist', data)


def blacklist_remove(token, email):
    # Removes given email from blacklist in database
    user_id = decode_token(token)['user_id']
    query = Blacklist.delete().where(
        Blacklist.user_id == user_id, Blacklist.ignore == email)
    query.execute()


def blacklist_list(token):
    # returns list of user's blacklisted emails
    user_id = decode_token(token)['user_id']
    blacklist_table_rows = Database.get_id('Blacklist', user_id)
    blacklist = []
    for row in blacklist_table_rows:
        blacklist.append(row.ignore)
    return blacklist


def spam_filter_on(token):
    # Turns the spam filter on
    user_id = decode_token(token)['user_id']
    user_row = Login.get(Login.user_id == user_id)
    user_row.spam_filter_on = True
    user_row.save()


def spam_filter_off(token):
    # Turns the spam filter off
    user_id = decode_token(token)['user_id']
    user_row = Login.get(Login.user_id == user_id)
    user_row.spam_filter_on = False
    user_row.save()


def is_blacklisted(user_id, email):
    # returns True if email is blacklisted by user, false if not
    blacklist_table_rows = Database.get_id('Blacklist', user_id)
    for row in blacklist_table_rows:
        if row.ignore == email:
            return True
    return False


def reset_spam_counters(user_id, email):
    # Reset duplicate/invalid counters to 0 in senders table
    sender_row = Senders.get(Senders.user_id == user_id,
                             Senders.sender_email == email)
    sender_row.invalid_counter = 0
    sender_row.duplicate_counter = 0
    sender_row.save()


def increment_duplicate_counter(user_id, email):
    # Increment duplicate counter by one in senders table
    sender_row = Senders.get(Senders.user_id == user_id,
                             Senders.sender_email == email)
    sender_row.duplicate_counter += 1
    sender_row.save()


def increment_invalid_counter(user_id, email):
    # Increment invalid counter by one in senders table
    sender_row = Senders.get(Senders.user_id == user_id,
                             Senders.sender_email == email)
    sender_row.invalid_counter += 1
    sender_row.save()


def is_spam_filter_on(user_id):
    # returns True if user's spam filter is on, false if not
    user_row = Login.get(Login.user_id == user_id)
    return user_row.spam_filter_on


def update_senders_table(user_id, email):
    # Creates entry to sender table if doesn't exist
    try:
        Senders.get(Senders.user_id == user_id,
                    Senders.sender_email == email)
    except:
        Senders.create(user_id=user_id, sender_email=email)


def is_duplicate(user_id, path_to_sent):
    # Returns True if xml has already been sent to user
    sent_file_size = os.path.getsize(path_to_sent)
    for invoice_file_name in os.listdir("invoices"):
        # Makes sure sent file and README are not considered
        if (invoice_file_name != path_to_sent.split('/', 1)[1] and invoice_file_name != 'README.txt'):
            invoice_uid = int(invoice_file_name.split('_', 1)[0])
            invoice_size = os.path.getsize(f'invoices/{invoice_file_name}')
            # If invoice belongs to user and has the same filesize check if duplicate
            if (user_id == invoice_uid and sent_file_size == invoice_size):
                # Generators for yielding hashes from 1024 byte chunks of files
                generator_1 = hash_generator(path_to_sent)
                generator_2 = hash_generator(f'invoices/{invoice_file_name}')
                duplicate = True
                for hash_chunk_1, hash_chunk_2 in zip(generator_1, generator_2):
                    num_chunks += 1
                    # If two hashes are not the same, break to stop generating hashes
                    # and compare next file. Set duplicate to False.
                    if (hash_chunk_1 != hash_chunk_2):
                        duplicate = False
                        break
                # If for loop exits without any two hashes being different (duplicate will
                # not have been set to False) there exists a duplicate, return True
                if duplicate == True:
                    return True
    # If all files have been read, there are no duplicates, return False
    return False


def hash_generator(path_to_file):
    # generates hashes from chunks of files, each chunk is 1024bytes
    file = open(path_to_file, 'rb')
    while True:
        chunk = file.read(1024)
        if not chunk:
            return
        yield hash(chunk)


if __name__ == "__main__":
    # blacklist_add('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE', 'test@gmail.com')
    # blacklist_remove('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE', 'test@gmail.com')
    # print(blacklist_list('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE'))
    # print(is_blacklisted(0, "test@gmail.com"))
    # print(is_spam_filter_on(0))
    # update_senders_table(0, "bb@gmail.com")
    # increment_invalid_counter(0, "bb@gmail.com")
    # increment_duplicate_counter(0, "bb@gmail.com")
    # spam_filter_on('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE')
    # spam_filter_off('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE')
    # print(is_duplicate(1, 'invoices/sent.xml'))
    pass

    # Check if spam filter is on
    # If on, check is sender is blacklisted
    # If blacklisted, dont process
    # Check if invalid
    # If invalid, increment counter
    # Check if counter greater than max
    # If greater than max, blacklist, don't process
    # Repeat check for duplicate
