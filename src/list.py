from src.helper import decode_token
from src.database import Database


def list_filenames(user_token):
    # returns list of invoice file names belonging to a user
    user_id = decode_token(user_token)['user_id']
    file_names = []
    raw_list = Database.get_id('Ownership', user_id)
    for item in raw_list:
        file_names.append(f"invoices/{user_id}_{item.xml_id}")
    return {'filenames': file_names}


def list_filter(user_token, sender, time, price):
    # filter invoices by sender, time and price
    user_id = decode_token(user_token)['user_id']
    unfiltered_list = Database.get_id('Ownership', user_id)

    filtered_list = filter(lambda item: price_filter(str(item.price), price),
                           filter(lambda item: time_filter(item.time.strftime('%Y-%m-%d'), time),
                                  filter(lambda item: sender_filter(item.sender, sender), unfiltered_list)))

    file_names = []
    for item in filtered_list:
        file_names.append(f"invoices/{user_id}_{item.xml_id}")
    return {'filenames': file_names}


def sender_filter(element, sender):
    if sender == "" or element == sender:
        return True
    return False


def time_filter(element, time):
    if time == "" or element == time:
        return True
    return False


def price_filter(element, price):
    if price == "" or element == price:
        return True
    return False
