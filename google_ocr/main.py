from re import match, compile, sub
from os import getenv
from base64 import b64decode
from json import loads, dumps

from google.cloud import pubsub_v1
from google.cloud import vision

vision_client = vision.ImageAnnotatorClient()
publisher = pubsub_v1.PublisherClient()

project_id = getenv('GCP_PROJECT')

def detect_text(event, context):
    message_in = b64decode(event['data']).decode('utf-8')
    # required for json.loads
    r = compile(r"\n")
    message_in = r.sub(r"\\n", message_in)
    message_in = loads(message_in)

    uri_list = message_in["uri_list"]
    uri_count = len(uri_list)
    try:
        message_out = {"pages_count": uri_count, "doc_id": message_in["doc_id"]}
    except:
        message_out = {"pages_count": uri_count}

    for i in range(uri_count):
        uri = uri_list[i]
        image = vision.types.Image()
        image.source.image_uri = uri
        text_detection_response = vision_client.text_detection(image=image)
        annotations = text_detection_response.text_annotations
        if len(annotations) > 0:
            text = annotations[0].description
            message_out["page"+str(i+1)] = text
        else:
            message_out["page"+str(i+1)] = ""

    message_out = dumps(message_out).encode('utf-8')

    topic_name = message_in["topic_name"]
    topic_path = publisher.topic_path(project_id, topic_name)
    publisher.publish(topic_path, data=message_out)
    
    

    

    
