import sys
import signal
from json import dumps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config
from src.clear import clear
from src.user import user_register, user_login, user_logout, user_update_email, user_update_password
from src.email import email_set, email_retrieve_start, email_retrieve_end
from src.database import Database
from src.error import InputError, AccessError

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


APP = Flask(__name__)
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


'''
@APP.route("/invoice/upload", methods=['GET'])
def upload_xml():
    # TODO
    token = request.args.get('token')
    XML_body = request.args.get('XML_body')
    report = function_name4(token, XML_body)

    return dumps({"invoice_report": report})
'''


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


if __name__ == "__main__":
    Database.start()
    Database.create_tables()
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port, debug=False)  # Do not edit this port\
