import io
import json
import os

import requests
import zipfile

from api_v1.baseapi import BaseApi
from gallery_authentication.gallery_authentication_method import GalleryAuthenticationMethod
from request_methods.methods import Method


def _build_questions_list(questions={}) -> object:
    if len(questions) == 0:
        return {}

    # Define the outline of the request body expected by Gallery
    questions_body = {
        "questions": []
    }

    for key, value in questions.items():
        new_question = {
            "name": key,
            "value": value
        }

        questions_body["questions"].append(new_question)

    return questions_body


class Workflows(BaseApi):
    def __init__(self, base_url: str, authenticator: GalleryAuthenticationMethod):
        """
        The Workflows class represents the workflow endpoint and all the methods associated with it
        :param base_url: The base URL of your Gallery API as defined in your server settings
        :param authenticator: A GalleryAuthenticationMethod object representing the method for authentication to your Gallery instance (e.g. Oauth1 or Oauth2)
        """
        super().__init__(base_url=base_url, authenticator=authenticator)

    def get_subscription(self, headers={}, params={}) -> requests.Response:
        """
        Finds workflows in a subscription
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'v1/workflows/subscription'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def post_jobs(self, app_id: str, questions={}, headers={}) -> requests.Response:
        """
        Queues a job execution for the specified workflow with the supplied answers
        :param app_id: The id for the workflow to execute.
        :param questions: A dictionary representing the list of questions and answers to execute the workflow with.
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = f'v1/workflows/{app_id}/jobs'
        questions = _build_questions_list(questions=questions)
        questions = json.dumps(questions)
        headers['Content-Type'] = 'application/json'
        response = self._make_request(Method.POST.value, endpoint=endpoint, headers=headers, body=questions)
        return response

    def get_jobs(self, app_id: str, headers={}, params={}) -> requests.Response:
        """
        Returns the jobs for the given Alteryx Analytics App
        :param app_id: The id for the workflow to get jobs for.
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = f'v1/workflows/{app_id}/jobs'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_questions(self, app_id: str, headers={}, params={}) -> requests.Response:
        """
        Get the questions for the given Alteryx Analytics App
        :param app_id: The id for the workflow to get questions for.
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = f'v1/workflows/{app_id}/questions'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_package(self, app_id) -> requests.Response:
        """
        Returns the app that was requested
        :param app_id: The id of the package to retrieve.
        :return: Returns True when contents are saved
        """
        endpoint = f'/v1/workflows/{app_id}/package'

        response = self._make_request(Method.GET.value, endpoint=endpoint)
        return response

    def get_package_and_save(self, app_id: str, save_path: str) -> bool:
        """
        A helper method that wraps around the get_package call.  This method will retrieve
        a package from the API and save it to a designated path
        :param app_id: The id of the package to retrieve.
        :param save_path: A path representing where the package should be saved
        :return: Returns True when contents are saved
        """

        if not os.path.isdir(save_path):
            raise NotADirectoryError

        response = self.get_package(app_id=app_id)
        zipped_package = zipfile.ZipFile(io.BytesIO(response.content))
        zipped_package.extractall(save_path)

        return True


