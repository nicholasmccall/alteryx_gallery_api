import requests

from api_v1.baseapi import BaseApi
from gallery_authentication import GalleryAuthenticationMethod
from request_methods.methods import Method


class Jobs(BaseApi):
    def __init__(self, base_url: str, authenticator: GalleryAuthenticationMethod):
        """
        The Jobs class represents the jobs endpoint and all the methods associated with it
        :param base_url: The base URL of your Gallery API as defined in your server settings
        :param authenticator: A GalleryAuthenticationMethod object representing the method for authentication to your Gallery instance (e.g. Oauth1 or Oauth2)
        """
        super().__init__(base_url=base_url, authenticator=authenticator)

    def get_job(self, job_id: str, headers=None, params=None) -> requests.Response:
        """
        Retrieves the job and its current state
        :param job_id: The id representing the job
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return:
        """
        endpoint = f'v1/jobs/{job_id}'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_job_output(self, job_id: str, output_id: str, headers=None, params=None) -> requests.Response:
        """
        Get output for a given job.  It is important to pass the 'format' parameter as a param.  The consumer
        of the api is responsible for writing the raw content to a file.
        :param job_id: The id representing the job.
        :param output_id: The id representing the particular output to retrieve.
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A request response containing the contents being retrieved
        """
        endpoint = f'v1/jobs/{job_id}/output/{output_id}'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

