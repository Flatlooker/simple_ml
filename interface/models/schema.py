from os import path
from yaml import safe_load as yaml_load
from cerberus import Validator


def load_schema(file_name):
    dir_path = path.dirname(path.realpath(__file__))
    file_path = '{}/{}.yml'.format(dir_path, file_name)
    with open(file_path, 'r') as stream:
        return yaml_load(stream)


def validate(body, schema_name):
    v = Validator()
    schema = load_schema(schema_name)

    return v.validate(body, schema)
