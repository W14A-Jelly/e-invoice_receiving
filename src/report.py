import json

# Helper functions for generating a communication report

# Create new JSON file corresponding to a single invoice
def create_new(invoice_id):
    report_name = 'Invoice ' + str(invoice_id) + ' Report'
    template = {
        'invoice_id' : invoice_id,
        'status' : '-',
        'error' : '-',
    }
    json_template = json.dumps(template)
    # Create new JSON file containing report template
    with open(report_name, 'w') as f:
        json.dump(json_template, f)
        f.close()
    # Return the file's name
    return report_name

# Update report in case of succesful reception
def update_successful(report_name):
    with open(report_name, 'r+') as f:
        data = json.load(f)
        data['status'] = 'success'
        json.dump(data, f)
        f.close()

# Update report in case of unsuccessful reception with relevant error message
def update_unsuccessful(report_name, error_msg):
    with open(report_name, 'r+') as f:
        data = json.load(f)
        json.dump(data, f)
        data['status'] = 'unsuccessful'
        data['error'] = error_msg
        json.dump(data, f)
        f.close()


