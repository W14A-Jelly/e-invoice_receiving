from urllib import response
import requests
import json
import zipfile
import io
import os


def render_invoice(invoice_filename):
    base_url = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering"

    # Open invoice and make http post request
    file = {'file': open(f"invoices/{invoice_filename}", 'rb')}
    response = requests.post(url=f"{base_url}/upload", files=file)
    file_id = json.loads(response.text)['file_ids'][0]

    # Make http get request using file_id from previous request
    response = requests.get(
        url=f"{base_url}/download?file_id={file_id}&file_type=JPEG")

    # Extract zipped response to renders directory
    zipped_file = zipfile.ZipFile(io.BytesIO(response.content))
    extracted = zipped_file.namelist()
    zipped_file.extractall("src/static/renders")
    render_filename = extracted[0]

    return render_filename


if __name__ == "__main__":
    print(render_invoice("example1.xml"))
