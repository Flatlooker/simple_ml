from base64 import b64decode
from re import match, compile, sub
from json import loads, dumps
from uuid import uuid4
from requests import get
from os import getenv, path, remove
from google.cloud import storage
from google.cloud import pubsub_v1

storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

project_id = getenv('GCP_PROJECT')

def get_extension(response):
    content_type = response.headers.get('content-type').lower()
    extensions = {
        'image/jpe?g': 'jpg',
        'image/png': 'png',
        'image/tiff': 'tiff',
        'application/pdf': 'pdf',
    }

    file_extension = 'txt'
    for regex, extension in extensions.items():
        if match('^{}$'.format(regex), content_type):
            file_extension = extension

    return file_extension

def url_to_storage(urls, doc_id, webhook_url):
    message_out = {"uri_list": [], "topic_name": getenv("TOPIC_DOCUMENT_POSTPROCESSING"), "doc_id": doc_id, "webhook_url": webhook_url}
    for url in urls:
        response = get(url, allow_redirects=True)

        # file name
        file_hash = uuid4()
        file_extension = get_extension(response)
        file_name = 'document_{}.{}'.format(file_hash, file_extension)

        # save file to google storage
        bucket = storage_client.bucket(getenv("BUCKET_DOCUMENTS"))
        blob = bucket.blob(file_name)
        blob.upload_from_string(response.content)

        uri = 'gs://{}/{}'.format(getenv("BUCKET_DOCUMENTS"), file_name)
        message_out["uri_list"].append(uri)

    # send message to topic
    message_out = dumps(message_out).encode('utf-8')
    topic_name = getenv("TOPIC_OCR_GOOGLE")
    topic_path = publisher.topic_path(project_id, topic_name)
    publisher.publish(topic_path, data=message_out)


def detect_text(event, context):
    message_in = b64decode(event['data']).decode('utf-8')
    # required for json.loads
    r = compile(r"\n")
    message_in = r.sub(r"\\n", message_in)
    message_in = loads(message_in)

    # custom model : one prediction at a time
    model_params = message_in["instances"][0]
    webhook_url = message_in["webhook_url"]
    url_to_storage(model_params["urls"], model_params["doc_id"], webhook_url)

