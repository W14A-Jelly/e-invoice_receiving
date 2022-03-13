# from error import InputError, AccessError
from lxml import etree
import os


def email_set(token, email_address, email_pass):
    '''
    some description
    '''
    return {}


def email_retrieve_start(token):
    '''
    some description
    '''
    return {}


def email_validate_xml(path_to_invoice):
    try:
        # Validate well-formedness
        invoice_root = etree.parse(path_to_invoice)
        # Validate against schema
        schema_root = etree.parse('src/xmlschema.xsl')
        # xmlschema = etree.XMLSchema(schema_root)
        # xmlschema.assertValid(invoice_root)

    # if invalid, remove from invoices directory
    except (etree.XMLSyntaxError, etree.DocumentInvalid):
        os.remove(path_to_invoice)
        return False

    return True


def email_output_report():
    # module to email_retrieve_start
    '''
    some description
    '''
    return {}


def email_retrieve_end(token):
    '''
    some description
    '''
    return {}


if __name__ == '__main__':
    print(email_validate_xml('invoices/example1.xml'))
