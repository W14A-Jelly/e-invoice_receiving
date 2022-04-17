from src.helper import decode_token
from src.database import Database
from datetime import datetime, date
import sys



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


def list_filter(user_token, sender, min_time, max_time, min_price, max_price):
    # filter invoices by sender, time and price
    user_id = decode_token(user_token)['user_id']
    unfiltered_list = Database.get_id('Ownership', user_id)

    # handle cases where textboxes are empty on frontend
    if sender == "\"\"" or sender == '\'\'':
        sender = ""
    if min_time == "\"\"" or min_time == '\'\'':
        min_time = ""
    if max_time == "\"\"" or max_time == '\'\'':
        max_time = ""
    if min_price == "\"\"" or min_price == '\'\'':
        min_price = ""
    if max_price == "\"\"" or max_price == '\'\'':
        max_price = ""

    filtered_list = filter(lambda item: price_filter(str(item.price), min_price, max_price),
                           filter(lambda item: time_filter(item.time.strftime("%Y-%m-%d"), min_time, max_time),
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


def time_filter(element, min_time, max_time):
    # Case where user gives no min or max time
    if (min_time == "" and max_time == ""):
        return True
    # Case where no lower bound is given
    elif (min_time == ""):
        max_time = datetime.strptime(max_time, "%Y-%m-%d")
        min_time = datetime.min
    # Case where no upper bound is given
    elif (max_time == ""):
        min_time = datetime.strptime(min_time, "%Y-%m-%d")
        max_time = datetime.max
    # Convert both parameters to date time objets if both bounds given
    else:
        min_time = datetime.strptime(min_time, "%Y-%m-%d")
        max_time = datetime.strptime(max_time, "%Y-%m-%d")

    element = datetime.strptime(element, "%Y-%m-%d")

    # Sees if datetime object lies between two times
    if element >= min_time and element <= max_time:
        return True

    # Else
    return False


def price_filter(element, min_price, max_price):
    # Case where user gives no min or max price
    if (min_price == "" and max_price == ""):
        return True

    # Case where no lower bound is given
    elif (min_price == ""):
        min_price = sys.float_info.min
        max_price = float(max_price)
    # Case where no upper bound is given
    elif (max_price == ""):
        max_price = sys.float_info.max
        min_price = float(min_price)
    # Case where both bounds are given
    else:
        min_price = float(min_price)
        max_price = float(max_price)

    element = float(element)

    # Sees if price(float) lies between two prices
    if element >= min_price and element <= max_price:
        return True

    # Else
    return False

def get_stats(token, year):
    # return the expense of each month for corresponding year.
    price = [0,0,0,0,0,0,0,0,0,0,0,0]
    user_id = decode_token(token)['user_id']
    data = Database.get_id('Ownership', user_id)
    for tup in data:
        time = tup.time
        month = int(time.datetime.strftime("%m"))
        invoice_year = time.datetime.strftime("%Y")
        if invoice_year == year and month <=12 and month > 0:
            price[month-1] += tup.price

    return {'price':price}

if __name__ == "__main__":
    # print(price_filter("1.0", "0.5", "0.7"))
    # print(time_filter("2022-03-12", "2022-02-12", "2022-02-12"))
    pass

