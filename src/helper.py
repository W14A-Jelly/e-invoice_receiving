from base64 import decode
from src.database import Database
from lxml import etree
import jwt
import os


def decode_token(token):
    '''
    This function converts a token into its corresponding user & session id

    Arguments:
        token (encoded string) - A user jwt needs to be decode

    Return Value:
        Returns {'user_id', 'session_id'} on success.
        If this token does not refer to a valid logged in user
        return None.
    '''
    secret_str = 'JELLY2021'

    try:
        users = [user.user_id for user in Database.get_table('Login')]
        decode_data = jwt.decode(token, secret_str, algorithms=['HS256'])
        session = Database.get_id('Login', decode_data['user_id'])[
            0].session_id
    except:
        return None
    session = session.split()
    if decode_data['user_id'] in users and decode_data['session_id'] in session:
        return {'user_id': decode_data['user_id'],
                'session_id': decode_data['session_id']}

    return None


def validate_xml(path_to_invoice):

    # Validate well-formedness
    try:
        invoice_root = etree.parse(path_to_invoice)

    except etree.XMLSyntaxError:
        return False

    # Validate against schema
    schema_root = etree.parse('xsd/UBL-Invoice-2.1.xsd')
    xmlschema = etree.XMLSchema(schema_root)
    try:
        xmlschema.assertValid(invoice_root)

    except etree.DocumentInvalid:
        return False

    # If no exceptions raised, xml is valid
    return True


def is_duplicate(user_id, path_to_xml):
    # Returns True if xml has already been sent to user
    pass
