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


def is_duplicate(user_id, path_to_sent):
    # Returns True if xml has already been sent to user
    sent_file_size = os.path.getsize(path_to_sent)
    for invoice_file_name in os.listdir("invoices"):
        # Makes sure sent file and README are not considered
        if (invoice_file_name != path_to_sent.split('/', 1)[1] and invoice_file_name != 'README.txt'):
            invoice_uid = int(invoice_file_name.split('_', 1)[0])
            invoice_size = os.path.getsize(f'invoices/{invoice_file_name}')
            # If invoice belongs to user and has the same filesize check if duplicate
            if (user_id == invoice_uid and sent_file_size == invoice_size):
                # Generators for yielding hashes from 1024 byte chunks of files
                generator_1 = hash_generator(path_to_sent)
                generator_2 = hash_generator(f'invoices/{invoice_file_name}')
                duplicate = True
                for hash_chunk_1, hash_chunk_2 in zip(generator_1, generator_2):
                    # If two hashes are not the same, break to stop generating hashes
                    # and compare next file. Set duplicate to False.
                    if (hash_chunk_1 != hash_chunk_2):
                        duplicate = False
                        break
                # If for loop exits without any two hashes being different (duplicate will
                # not have been set to False) there exists a duplicate, return True
                if duplicate == True:
                    return True
    # If all files have been read, there are no duplicates, return False
    return False


def hash_generator(path_to_file):
    # generates hashes from chunks of files, each chunk is 1024bytes
    file = open(path_to_file, 'rb')
    while True:
        chunk = file.read(1024)
        if not chunk:
            return
        yield hash(chunk)
