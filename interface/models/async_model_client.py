from os import getenv
from json import dumps
from google.cloud import pubsub_v1
from .base_model_client import BaseModelClient

env = getenv('ENVIRONMENT')
project_id = getenv('GCP_PROJECT')
publisher = pubsub_v1.PublisherClient()

class AsyncModelClient(BaseModelClient):
    @property
    def is_async(self):
        return True

    @property
    def validator(self):
        return 'custom_validation'

    def call(self, body):
        body['webhook_url'] = self.webhook_url
        data = dumps(body).encode('utf-8')
        event = publisher.publish(self.__topic(), data=data)

        return event.result()

    def __topic(self):
        parts = [self.model]
        if env == 'staging':
            parts = ['staging', *parts]
        topic_name = '_'.join(parts)

        return publisher.topic_path(project_id, topic_name)
