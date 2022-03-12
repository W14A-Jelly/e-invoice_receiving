'''
some description
'''
import sys
import signal
from json import dumps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config
from src.other import clear_v1
# add imports for all route files

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
@APP.route("/user/register", methods=['POST'])
def register_new_user():
    input = request.get_json()

    return dumps(user_register(input['email_address'],input['password']))

@APP.route("/user/login", methods=['POST'])
def login_user():
    input = request.get_json()

    return dumps(user_login(input['email_address'],input['password']))

@APP.route("/user/logout", methods=['POST'])
def logout_user():
    input = request.get_json()
    user_logout(input['token'])

    return dumps({})

@APP.route("/email/set", methods=['POST'])
def set_business_email():
    input = request.get_json()
    function_name(input['token'],input['email_address'], input['email_pass'])
    return dumps({})

@APP.route("/email/retrieve/start", methods=['PUT'])
def start_api():
    input = request.get_json()
    function_name2(input['token'])
    return dumps({})

@APP.route("/email/retrieve/end", methods=['PUT'])
def end_api():
    input = request.get_json()
    function_name3(input['token'])
    return dumps({})

@APP.route("/invoice/upload", methods=['GET'])
def upload_xml():
    input = request.get_json()
    report = function_name4(input['token'],input['XML_body'])

    return dumps({"invoice_report": report})

@APP.route("/user/update/email", methods=['PUT'])
def update_email():
    input = request.get_json()
    function_name5(input['token'],input['email'])
    
    return dumps({})

@APP.route("/user/update/password", methods=['PUT'])
def update_password():
    input = request.get_json()
    function_name6(input['token'],input['email'])
    
    return dumps({})

@APP.route("/clear/v1", methods=['DELETE'])
def data_clear():
    clear()
    return {}  
