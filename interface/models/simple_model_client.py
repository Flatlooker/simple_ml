from os import getenv
from googleapiclient.errors import HttpError
import googleapiclient.discovery
from .base_model_client import BaseModelClient
from .errors import ModelUnknown

project_id = getenv('GCP_PROJECT')

class SimpleModelClient(BaseModelClient):
    @property
    def is_async(self):
        return False

    @property
    def validator(self):
        return 'tf_validation'

    def call(self, body):
        service = googleapiclient.discovery.build('ml', 'v1')
        name = 'projects/{}/models/{}'.format(project_id, self.model)

        try:
            response = service.projects().predict(name=name, body=body).execute()
        except:
            raise ModelUnknown

        return response
