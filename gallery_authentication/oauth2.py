import requests
from datetime import datetime, timedelta

from .gallery_authentication_method import GalleryAuthenticationMethod


class OAuth2(GalleryAuthenticationMethod):
    def __init__(self, client_id, client_secret, gallery_auth_url):
        """
        The OAuth2 object is used to manage the authentication to the Alteryx Gallery API via
        OAuth 2.0 and assists in decorating requests with a bearer token.
        :param client_id: The client ID located in an API-enabled Alteryx profile
        :param client_secret: The client secret located in an API-enabled Alteryx profile
        :param gallery_auth_url: The authentication url e.g. https://{gallerysite}/webapi/oauth2/token
        :param gallery_base_url: The API root url defined in your gallery setting e.g. https://{gallerysite}/webapi
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._gallery_auth_url = gallery_auth_url
        self._bearer_token = None
        self._token_expiration = None

    def __str__(self):
        return str({
            "client_id": self._client_id,
            "client_secret": "******",
            "gallery_auth_url": self._gallery_auth_url,
            "bearer_token": self._bearer_token,
            "token_expiration": str(self._token_expiration)
        })

    def _get_bearer_token(self) -> None:
        """
        Attempts to get a bearer token using the client id, client secret, and auth url instance variables
        :return: None
        """
        auth_body = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }

        response = requests.post(self._gallery_auth_url, data=auth_body).json()

        if 'access_token' in response:
            self._bearer_token = f"Bearer {response['access_token']}"
            self._token_expiration = datetime.now() + timedelta(seconds=response['expires_in'])

        if 'error' in response:
            raise ConnectionError(
                f"The following error was returned when attempting to connect to Gallery: {response['error']}:{response['error_description']}")

    def _refresh_bearer_token(self) -> None:
        """
        Checks to see if a bearer token exists or is expired and creates a new one if it either doesn't
        exist or has expired.
        :return: None
        """
        if not self._bearer_token:
            self._get_bearer_token()

        if datetime.now() >= self._token_expiration:
            self._get_bearer_token()

    def get_bearer_token(self) -> str:
        """
        This method utilizes the OAuth2 instance variables specified in the constructor to return
        the current bearer token.  If the current bearer token is expired or doesn't exist, it creates
        a new token.
        :return: A string representing the active bearer token
        """
        self._refresh_bearer_token()
        return self._bearer_token

    def authenticate(self, request: requests.Request) -> requests.Request:
        """
        Decorates the passed in request with a bearer token used to authenticate to Gallery
        :param request: A request object that will be decorated with a bearer token
        :return: The original request object with the addition of a bearer token
        """
        self._refresh_bearer_token()
        request.headers['Authorization'] = self._bearer_token
        return request



