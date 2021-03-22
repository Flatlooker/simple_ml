from base64 import b64decode
from re import match, compile, sub, findall
from requests import post
from os import getenv
from google.cloud import storage
from json import loads, dumps

def extract_data(event, context):
    message = b64decode(event['data']).decode('utf-8')
    # required for json.loads
    r = compile(r"\n")
    message = r.sub(r"\\n", message)
    message = loads(message)

    my_dict = {"list_of_emails": []}

    # find email
    r = re.compile(r'[A-Za-z0-9_%+-.]+@[A-Za-z0-9-.]+\.[A-Za-z]{2,}')

    pages_count = message["pages_count"]
    for page_number in range(1, pages_count+1):
        page_text = message["page"+str(page_number)]
        my_dict["list_of_emails"] += r.findall(page_text)

    my_dict["doc_id"] = message["doc_id"]
    webhook_url = message["webhook_url"]
    response_json = {"predictions": [my_dict]}
    post(webhook_url, json=response_json)
    return my_dict
