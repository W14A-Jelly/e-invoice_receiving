from src.helper import decode_token
from src.database import Database
from src.schema import Blacklist, Login
from src.error import InputError


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


if __name__ == "__main__":
    # blacklist_add('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE', 'aaaaa@gmail.com')
    # blacklist_remove('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE', 'test@gmail.com')
    # print(blacklist_list('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE'))
    # spam_filter_on('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE')
    # spam_filter_off('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJzZXNzaW9uX2lkIjoiMCJ9.AF1mShROSkSXmVJ_4G7HrewpnQJvokH2DHMzn1HdhzE')
    pass
