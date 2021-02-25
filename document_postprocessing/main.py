from base64 import b64decode
from re import match, compile, sub
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

    my_dict = {"has_first_name": 0}

    pages_count = message["pages_count"]
    for page_number in range(1, pages_count+1):
        page_text = message["page"+str(page_number)]
        if "first_name" in page_text:
            my_dict["has_first_name"] = 1
            break

    my_dict["doc_id"] = message["doc_id"]
    webhook_url = message["webhook_url"]
    response_json = {"predictions": [my_dict]}
    post(webhook_url, json=response_json)
    return my_dict
