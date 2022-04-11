import sys
import signal
from json import dumps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config
from src.clear import clear
from src.user import user_register, user_login, user_logout, user_update_email, user_update_password
from src.myemail import email_set, email_retrieve_start, email_retrieve_end
from src.database import Database
from src.list import list_filter, list_filenames, get_stats
from src.render import render_invoice
from src.error import InputError, AccessError
from src.database import Database
from src.blacklist import blacklist_add, blacklist_remove, blacklist_list, spam_filter_on, spam_filter_off


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__, static_url_path='/static')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
'''
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
'''


@APP.route("/", methods=['GET'])
def defaultpath():
    return ('API document available at https://app.swaggerhub.com/apis/Jelly6/E-invoice-receiving-api/1.0.0#/')


@APP.route("/user/register", methods=['POST'])
def register_new_user():
    input = request.get_json()
    return dumps(user_register(input['email'], input['password']))


@APP.route("/user/login", methods=['POST'])
def login_user():
    input = request.get_json()

    return dumps(user_login(input['email'], input['password']))


@APP.route("/user/logout", methods=['POST'])
def logout_user():
    input = request.get_json()
    user_logout(input['token'])

    return dumps({})


@APP.route("/email/set", methods=['POST'])
def set_business_email():
    input = request.get_json()
    email_set(input['token'], input['email'], input['email_pass'])
    return dumps({})


@APP.route("/email/retrieve/start", methods=['PUT'])
def start_api():
    input = request.get_json()
    email_retrieve_start(input['token'])
    return dumps({})


@APP.route("/email/retrieve/end", methods=['PUT'])
def end_api():
    input = request.get_json()
    reports = email_retrieve_end(input['token'])
    return dumps(reports)


@APP.route("/list/filenames/filtered", methods=['GET'])
def filter_invoices():
    token = request.args.get('token')
    sender = request.args.get('sender')
    min_time = request.args.get('min_time')
    max_time = request.args.get('max_time')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    filtered_list = list_filter(
        token, sender, min_time, max_time, min_price, max_price)
    return dumps(filtered_list)


@APP.route("/list/filenames", methods=['GET'])
def list_invoices():
    token = request.args.get('token')
    file_names = list_filenames(token)
    return dumps(file_names)


@APP.route("/render/invoice", methods=['GET'])
def show_invoice():
    fn = request.args.get('filename')
    img_file_name = render_invoice(fn)

    return dumps({'img': img_file_name})


@APP.route("/blacklist/block", methods=['PUT'])
def block():
    input = request.get_json
    blacklist_add(input['token'], input['email'])
    return ({})


@APP.route("/blacklist/unblock", methods=['PUT'])
def unblock():
    input = request.get_json
    blacklist_remove(input['token'], input['email'])
    return ({})


@APP.route("/blacklist/list", methods=['GET'])
def unblock():
    token = request.args.get('token')
    blacklist = blacklist_list(token)
    return ({'blacklist': blacklist})


@APP.route("/blacklist/spamfilter/on", methods=['PUT'])
def unblock():
    input = request.get_json
    spam_filter_on(input['token'])
    return ({})


@APP.route("/blacklist/spamfilter/off", methods=['PUT'])
def unblock():
    input = request.args.get('token')
    spam_filter_off(input['token'])
    return ({})


@APP.route("/user/update/email", methods=['PUT'])
def update_email():
    input = request.get_json()
    user_update_email(input['token'], input['email'])

    return dumps({})


@APP.route("/user/update/password", methods=['PUT'])
def update_password():
    input = request.get_json()
    user_update_password(input['token'], input['password'])

    return dumps({})


@APP.route("/clear", methods=['DELETE'])
def data_clear():
    try:
        assert 'Jelly2022' == request.get_json()['admin_pass']
        clear()
        return {}
    except:
        raise AccessError('Not authorised')
        return {}


@APP.route('/get/stats')
def get_statistic():
    token = request.args.get('token')
    year = request.args.get('year')
    return dumps(get_stats(token, year))


'''
@APP.route("/invoice/upload", methods=['GET'])
def upload_xml():
    # TODO
    token = request.args.get('token')
    XML_body = request.args.get('XML_body')
    report = function_name4(token, XML_body)

    return dumps({"invoice_report": report})
'''


@APP.route('/static/<path:path>')
def send_js(path):
    removed_front = path.partition('renders/')[2]
    file_name = removed_front.partition('.jpg')[0]
    Database.update_invoice(file_name, {'new': False})
    return send_from_directory('', path)


if __name__ == "__main__":
    Database.start()
    Database.create_tables()
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(host='0.0.0.0', port=config.port,
            debug=True)  # Do not edit this port\
