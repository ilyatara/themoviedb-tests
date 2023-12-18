import json

import requests
import allure
from allure_commons.types import AttachmentType
from curlify import to_curl
from jsonschema import validate

import project


def validate_schema(response_json, path_to_schema):
    with open(path_to_schema) as file:
        schema = json.loads(file.read())
    validate(instance=response_json, schema=schema)


def tmdb_request(method, relative_url, **kwargs):

    import project  # avoiding circular import

    absolute_url = project.config.tmdb_base_api_url + relative_url

    with allure.step(f'{method.upper()} {relative_url}'):
        with requests.sessions.Session() as session:
            session.headers.update(
                {'Authorization': f'Bearer {project.config.tmbd_read_access_token}'}
            )

            response = session.request(method=method, url=absolute_url, **kwargs)

            curl = to_curl(response.request)
            allure.attach(
                body=curl.encode('utf8'),
                name='Curl',
                attachment_type=AttachmentType.TEXT,
                extension='txt'
            )
            if 'json' in response.headers.get('Content-Type'):
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode('utf8'),
                    name='Response Json',
                    attachment_type=AttachmentType.JSON,
                    extension='json'
                )
            elif 'text' in response.headers.get('Content-Type'):
                allure.attach(
                    body=response.text.encode('utf8'),
                    name='Response Text',
                    attachment_type=AttachmentType.TEXT,
                    extension='txt'
                )

    return response


def get_tmdb_account_id():
    import project  # avoiding circular import
    response = tmdb_request('get', f'/account')
    account_id = response.json()['id']
    return account_id


def delete_all_rated_movies():
    response = tmdb_request('get', f'/account/{project.config.tmdb_account_id}/rated/movies')
    rated_movies_ids = [movie['id'] for movie in response.json()['results']]
    for movie_id in rated_movies_ids:
        tmdb_request('delete', f'/movie/{movie_id}/rating')


def delete_all_favorites():
    url_get = f'/account/{project.config.tmdb_account_id}/favorite/movies'
    url_post = f'/account/{project.config.tmdb_account_id}/favorite'
    response = tmdb_request('get', url_get)
    fav_ids = [fav['id'] for fav in response.json()['results']]
    for fav_id in fav_ids:
        body = {"media_type": "movie", "media_id": fav_id, "favorite": False}
        tmdb_request('post', url_post, json=body)
