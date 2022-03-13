# from error import InputError, AccessError
from validator import ReportValidator
import os

import xmlschema


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


def email_validate_xml():
    '''
    # Currently only validates in accordance with XMLSchema
    schema_validator = ReportValidator()
    valid = schema_validator.validate(report_path)
    if not valid:
        # delete from invoice folder
        os.remove(report_path)
    else:
        return valid

    xmlschema_doc = etree.parse('src/XMLSchema.xsl')
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse('invoices/example1.xml')
    result = xmlschema.validate(xml_doc)
    '''
    xsd = xmlschema.XMLSchema('src/UBL-CommonAggregateComponents-2.1.xsd')
    return xsd.is_valid('invoices/example1.xml')


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
    print(email_validate_xml())
