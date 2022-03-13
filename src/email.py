from src.error import InputError, AccessError


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


def email_validate_xml(file_path):
    valid = True
    with open(file_path, 'r') as f:
        # Validating Wellformedness (Checking if the input is valid and the file itself has valid contents)
        # Syntax Rules (Validates EN16931 business rules) (Appendix B, BR Rules)

        # EPPOL rules (Validates Specific AUNZ business rules) (Appendix B, PEPPOL Rules)

        # Schema Validation (Validates the schema of the invoice)

        # If not valid, delete XML file from invoice directory
    if not valid:
        # TODO: delete file

    return valid


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
