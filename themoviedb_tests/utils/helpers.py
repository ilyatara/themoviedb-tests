import json
from os.path import abspath, dirname, join

import allure
from allure_commons.types import AttachmentType
from requests import sessions
from curlify import to_curl
from jsonschema.validators import validate


def get_path(*segments):
    project_root = abspath(dirname(dirname(dirname(__file__))))
    return abspath(join(project_root, *segments))


def validate_schema(response, path_to_schema):
    with open(path_to_schema) as file:
        schema = json.loads(file.read())
    validate(instance=response.json(), schema=schema)

