import json
import os
import glob
from pprint import pprint
import smtplib
import ssl
import email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    with open(report_name, 'w', encoding="utf-8") as f:
        json.dump(template, f)
        f.close()
    # Return the file's name
    return report_name

# Update report in case of succesful reception


def update_successful(report_name):
    with open(report_name, 'r+', encoding="utf-8") as f:
        data = json.load(f)
        data['status'] = 'success'
        data['error'] = 'none'
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()

# Update report in case of unsuccessful reception with relevant error message


def update_unsuccessful(report_name, error_msg):
    with open(report_name, 'r+', encoding="utf-8") as f:
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
        if report != "README.txt":
            with open(os.path.join(directory, report), 'r', encoding="utf-8") as f:
                data = json.load(f)
                all_reports.append(data)
    return all_reports

# Clears all reports from the reports folder


def clear_reports():
    reports = glob.glob('reports/*')
    for report in reports:
        if report != "README.txt":
            os.remove(report)


def email_error_report(path_to_XML, path_to_report, receiver_email, client_email):
    # Login details of email to send from
    sender_email = "einvoice.retrieve@gmail.com"
    password = 'hvxx qjly uoqj owgu'

    # Read error message from communication report
    with open(path_to_report, "r") as report:
        error_message = json.load(report)['error']

    # Subject and body of email
    subject = "Error Sending XML Invoice To %s" % (client_email)
    body = ("The following error was generated after your attempt to send an XML invoice to %s.\n\n"
            "\"%s.\"\n\n"
            "Please find your invoice attatched below:\n") % (client_email, error_message)

    # Create a multipart message
    message = MIMEMultipart()
    # Headers:
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # Body (plain text):
    message.attach(MIMEText(body, "plain"))

    # Invoice attatchment
    with open(path_to_XML, "rb") as attachment:
        invoice_part = MIMEBase("application", "octet-stream")
        # Set payload of part as file contents in binary
        invoice_part.set_payload(attachment.read())
        # Convert payload of part to ASCII
    encoders.encode_base64(invoice_part)
    # Add header as key/value pair to attachment part
    invoice_part.add_header(
        "Content-Disposition",
        f"attachment; filename= {path_to_XML}",
    )
    # Add attachment to message
    message.attach(invoice_part)

    # Convert message to string
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    port = 465
    smtp_server = 'smtp.gmail.com'

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


if __name__ == "__main__":
    '''
    report1 = create_new(1)
    update_successful(report1)

    report2 = create_new(2)
    update_unsuccessful(report2, 'Invalid UBL format')

    all_reports = return_reports()
    print(all_reports)

    email_error_report("invoices/example1.xml", "reports/invoice_2_report.json",
                       'se2y22g32@gmail.com', "client@gmail.com")
    clear_reports()
    '''
    pass
