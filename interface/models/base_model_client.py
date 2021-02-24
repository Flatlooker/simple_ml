from os import getenv
from abc import ABC, abstractmethod
from .schema import validate
from .errors import InvalidInput, AsyncMismatch

class BaseModelClient(ABC):
    def __init__(self, model):
        self.model = model
        self.webhook_url = ''
        pass

    @property
    @abstractmethod
    def is_async(self):
        pass

    def set_webhook_url(self, webhook_url):
        self.webhook_url = webhook_url

    @property
    @abstractmethod
    def validator(self):
        pass

    def validate(self, body):
        if not validate(body, self.validator):
            raise InvalidInput
        if self.is_async and not self.webhook_url:
            raise AsyncMismatch

    @abstractmethod
    def call(self, body):
        pass

    def response(self, body):
        self.validate(body)
        return self.call(body)
