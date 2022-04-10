from time import strptime
from src.helper import decode_token
from src.database import Database
from datetime import datetime


def list_filenames(user_token):
    # returns list of invoice file names belonging to a user
    user_id = decode_token(user_token)['user_id']
    file_names = []
    raw_list = Database.get_id('Ownership', user_id)
    for item in raw_list:
        file_names.append(f"{user_id}_{item.xml_id}")
    return {'filenames': file_names}


def list_filter(user_token, sender, min_time, max_time, min_price, max_price):
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

    filtered_list = filter(lambda item: price_filter(str(item.price), min_price, max_price),
                           filter(lambda item: time_filter(item.time.strftime("%Y-%m-%d"), min_time, max_time),
                                  filter(lambda item: sender_filter(item.sender, sender), unfiltered_list)))

    file_names = []
    for item in filtered_list:
        file_names.append(f"{user_id}_{item.xml_id}")
    return {'filenames': file_names}


def sender_filter(element, sender):
    if sender == "" or element == sender:
        return True
    return False


def time_filter(element, min_time, max_time):
    # Case where user gives no min or max time
    if (min_time == "" and max_time == ""):
        return True

    # Convert parameters to date time objets
    element = datetime.strptime(element, "%Y-%m-%d")
    min_time = datetime.strptime(min_time, "%Y-%m-%d")
    max_time = datetime.strptime(max_time, "%Y-%m-%d")

    # Sees if datetime object lies between two times
    if element >= min_time and element <= max_time:
        return True

    # Else
    return False


def price_filter(element, min_price, max_price):
    # Case where user gives no min or max price
    if (min_price == "" and max_price == ""):
        return True

    # Convert parameters to floats
    element = float(element)
    min_price = float(min_price)
    max_price = float(max_price)

    # Sees if price(float) lies between two prices
    if element >= min_price and element <= max_price:
        return True

    # Else
    return False


if __name__ == "__main__":
    # print(price_filter("1.0", "0.5", "0.7"))
    # print(time_filter("2022-03-12", "2022-02-12", "2022-02-12"))
