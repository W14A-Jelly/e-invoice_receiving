from urllib import response
import requests
import json
import zipfile
import io


def render_invoice(path_to_invoice):
    base_url = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering"

    # Open invoice and make http post request
    file = {'file': open(path_to_invoice, 'rb')}
    response = requests.post(url=f"{base_url}/upload", files=file)
    file_id = json.loads(response.text)['file_ids'][0]

    # Make http get request using file_id from previous request
    response = requests.get(
        url=f"{base_url}/download?file_id={file_id}&file_type=JPEG")

    # Extract zipped response to renders directory
    zipped_file = zipfile.ZipFile(io.BytesIO(response.content))
    zipped_file.extractall("renders")


if __name__ == "__main__":
    render_invoice("invoices/example2.xml")
