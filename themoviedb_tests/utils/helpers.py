import json
from os.path import abspath, dirname, join

import allure
from allure_commons.types import AttachmentType
from requests import sessions
from curlify import to_curl
from jsonschema.validators import validate

import project


def get_path(*segments):
    project_root = abspath(dirname(dirname(dirname(__file__))))
    return abspath(join(project_root, *segments))


def validate_schema(response, path_to_schema):
    with open(path_to_schema) as file:
        schema = json.loads(file.read())
    validate(instance=response.json(), schema=schema)


def tmdb_request(method, relative_url, **kwargs):

    absolute_url = (project.config.tmdb_base_api_url +
                   project.config.tmdb_api_version +
                   relative_url)

    with allure.step(f'{method.upper()} {relative_url}'):
        with sessions.Session() as session:
            session.headers.update(
                {'Authorization': f'Bearer {project.config.tmdb_read_access_token}'}
            )
            response = session.request(method=method, url=absolute_url, **kwargs)

            curl = to_curl(response.request)
            allure.attach(
                body=curl.encode('utf8'),
                name='Curl',
                attachment_type=AttachmentType.TEXT,
                extension='txt'
            )

            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode('utf8'),
                    name='Response Json',
                    attachment_type=AttachmentType.JSON,
                    extension='json'
                )
            except json.JSONDecodeError:
                allure.attach(
                    body=response.text.encode('utf8'),
                    name='Response Text',
                    attachment_type=AttachmentType.TEXT,
                    extension='txt'
                )

    return response
