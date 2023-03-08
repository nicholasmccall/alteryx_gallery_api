import requests

from gallery_authentication import GalleryAuthenticationMethod
from request_methods.methods import Method


class BaseApi:
    def __init__(self, base_url: str, authenticator: GalleryAuthenticationMethod):
        self._base_url = base_url
        self._authenticator = authenticator

    def _make_request(self, method: Method, endpoint, headers={}, params={}, body=None) -> requests.Response:
        url = f'{self._base_url}/{endpoint}'
        api_request = requests.Request(method=method, url=url, headers=headers, params=params, data=body)
        authed_api_request = self._authenticator.authenticate(api_request)
        prepared_request = authed_api_request.prepare()
        response = requests.Session().send(prepared_request)
        return response
