import json
import os
import glob

# Helper functions for generating a communication report

# Create new JSON file corresponding to a single invoice


def create_new(invoice_id):
    report_name = 'reports/invoice_' + str(invoice_id) + '_report.json'
    template = {
        'invoice_id': invoice_id,
        'status': '-',
        'error': '-',
    }
    # Create new JSON file containing report template
    with open(report_name, 'w') as f:
        json.dump(template, f)
        f.close()
    # Return the file's name
    return report_name

# Update report in case of succesful reception


def update_successful(report_name):
    with open(report_name, 'r+') as f:
        data = json.load(f)
        data['status'] = 'success'
        data['error'] = 'none'
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()

# Update report in case of unsuccessful reception with relevant error message


def update_unsuccessful(report_name, error_msg):
    with open(report_name, 'r+') as f:
        data = json.load(f)
        data['status'] = 'unsuccessful'
        data['error'] = error_msg
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()

# Returns data from all reports as a list


def return_reports():
    all_reports = []
    directory = 'reports'
    for report in os.listdir(directory):
        with open(os.path.join(directory, report), 'r') as f:
            data = json.load(f)
            all_reports.append(data)
    return all_reports

# Clears all reports from the reports folder


def clear_reports():
    reports = glob.glob('reports/*')
    for report in reports:
        os.remove(report)


if __name__ == "__main__":
    report1 = create_new(1)
    update_successful(report1)

    # report2 = create_new(2)
    # update_unsuccessful(report2, 'invalid UBL format')

    # all_reports = return_reports()
    # print(all_reports)

    # clear_reports()
