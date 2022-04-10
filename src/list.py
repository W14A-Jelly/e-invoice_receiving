from src.helper import decode_token
from src.database import Database
from datetime import datetime


def list_filenames(user_token):
    # returns list of invoice file names belonging to a user
    user_id = decode_token(user_token)['user_id']
    file_names = []
    new = []
    paid = []
    raw_list = Database.get_id('Ownership', user_id)
    for item in raw_list:
        file_names.append(f"{user_id}_{item.xml_id}")
        new.append(item.new)
        paid.append(item.paid)
    return {'filenames': file_names, 'new':new, 'paid':paid}


def list_filter(user_token, sender, time, price):
    # filter invoices by sender, time and price
    user_id = decode_token(user_token)['user_id']
    unfiltered_list = Database.get_id('Ownership', user_id)

    # handle cases where textboxes are empty on frontend
    if sender == "\"\"" or sender == '\'\'':
        sender = ""
    if time == "\"\"" or time == '\'\'':
        time = ""
    if price == "\"\"" or price == '\'\'':
        price = ""

    filtered_list = filter(lambda item: price_filter(str(item.price), price),
                           filter(lambda item: time_filter(item.time.strftime('%Y-%m-%d'), time),
                                  filter(lambda item: sender_filter(item.sender, sender), unfiltered_list)))

    file_names = []
    new = []
    paid = []
    for item in filtered_list:
        file_names.append(f"{user_id}_{item.xml_id}")
        new.append(item.new)
        paid.append(item.paid)
    return {'filenames': file_names, 'new':new, 'paid':paid}


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


def get_stats(token, year):
    # return the expense of each month for corresponding year.
    price = [0,0,0,0,0,0,0,0,0,0,0,0]
    user_id = decode_token(user_token)['user_id']
    data = Database.get_id('Ownership', user_id)
    for tup in data:
        time = tup.time
        month = int(time.datetime.strftime("%m"))
        invoice_year = time.datetime.strftime("%Y")
        if invoice_year == year and month <=12 and month > 0:
            price[month-1] += tup.price

    return price


