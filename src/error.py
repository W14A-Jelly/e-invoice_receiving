from werkzeug.exceptions import HTTPException

# By Hayden Smith from comp1531

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'