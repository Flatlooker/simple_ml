from .base_model_client import BaseModelClient

class SyncModelClient(BaseModelClient):
    @property
    def is_async(self):
        return False

    @property
    def validator(self):
        return 'custom_validation'

    def call(self, body):
        return 'TEST'
