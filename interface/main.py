from os import getenv
from json import loads, dumps
from requests import get
from models import AsyncModelClient, SyncModelClient, SimpleModelClient
from models.errors import InvalidInput, ModelUnknown, AsyncMismatch

async_models = getenv('ASYNC_MODELS').lower().split(',')
sync_models = getenv('SYNC_MODELS').lower().split(',')
auth_token = getenv('AUTH_TOKEN').lower()

def interface(request):
    model = request.args.get('model').lower()
    webhook_url = request.args.get('url')
    body = request.get_json()

    if not authenticate(request):
        return {'error': 'Unauthorized'}, 401

    try:
        client = make_client(model)
        if webhook_url:
            client.set_webhook_url(webhook_url)
        result = client.response(body)
    except InvalidInput:
        return { 'error': 'Bad request' }, 400
    except ModelUnknown:
        return { 'error': 'Model unknown' }, 404
    except AsyncMismatch:
        return {'error': 'Async mismatch'}, 405
    except:
        return { 'error': 'Internal Error' }, 500

    if client.is_async:
        return { 'status': 'OK' }, 202

    return { 'status': 'OK', 'data': result }, 200


def make_client(model):
    if model in async_models:
        client = AsyncModelClient(model)
    elif model in sync_models:
        client = SyncModelClient(model)
    else:
        client = SimpleModelClient(model)

    return client

def authenticate(request):
    token = request.headers.get('authorization').lower().replace('bearer ', '')
    return token == auth_token
