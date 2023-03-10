from abc import ABC

import requests
from requests import Request


class GalleryAuthenticationMethod(ABC):
    def authenticate(self, request: Request) -> requests.Request:
        """
        This decorator function is used to pass the proper authorization header to an API function call.
        It expects the decorated function to expose an optional header parameter
        :param request: A request object that will be decorated with authentication
        :return: None
        """
        pass