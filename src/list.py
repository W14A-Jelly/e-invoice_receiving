from src.helper import decode_token
from src.database import Database


def list_filter(user_token, sender, time, price):
    # filter invoices by sender, time and price
    user_id = decode_token(user_token)['user_id']
    filtered_list = []
    unfiltered_list = Database.get_id('Ownership', user_id)
    for item in unfiltered_list:
        if item.sender == sender or item.time == time or item.price == price:
            filtered_list.append(f"invoices/{user_id}_{item.xml_id}")
    return {'filenames': filtered_list}
