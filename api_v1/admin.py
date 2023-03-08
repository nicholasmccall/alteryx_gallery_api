import io
import os
import zipfile

import requests

from api_v1.baseapi import BaseApi
from gallery_authentication import GalleryAuthenticationMethod
from request_methods.methods import Method


class Admin(BaseApi):
    def __init__(self, base_url: str, authenticator: GalleryAuthenticationMethod):
        super().__init__(base_url=base_url, authenticator=authenticator)

    def get_package(self, app_id: str) -> requests.Response:
        """
        Returns the app that was requested
        :param app_id: The id of the package to retrieve.
        :return: Returns True when contents are saved
        """
        endpoint = f'admin/v1/{app_id}/package'
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

    def get_users(self, headers=None, params=None) -> requests.Response:
        """
        Finds users in a Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/users'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_schedules(self, headers=None, params=None) -> requests.Response:
        """
        Finds schedules in a Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/schedules'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_collections(self, headers=None, params=None) -> requests.Response:
        """
        Finds collections in a Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/collections'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_subscriptions(self, headers=None, params=None) -> requests.Response:
        """
        Find subscriptions in a Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/subscriptions'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_server_data_connections(self, headers=None, params=None) -> requests.Response:
        """
        Returns data connections created in a private Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/serverdataconnections'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_system_data_connections(self, headers=None, params=None) -> requests.Response:
        """
        Returns system data connections created on the server where Alteryx Server is installed
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/systemdataconnections'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_insights(self, headers=None, params=None) -> requests.Response:
        """
        Finds insights in a Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/insights'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_migratable_workflows(self, subscription_id: str, headers=None) -> requests.Response:
        """
        Finds workflows in a Gallery that have been marked ready for migration
        :param subscription_id: The id of the subscription to search for migratable workflows
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        params = {'subscriptionId': subscription_id}
        endpoint = 'admin/v1/workflows/migratable'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_audit_log(self, entity: str, page: int, page_size: int,  headers=None) -> requests.Response:
        """
        Retrieve audit log entries for a given entity type
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        params = {'entity': entity, 'page': page, 'pageSize': page_size}
        endpoint = 'admin/v1/auditlog'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_workflow_jobs(self, headers=None, params=None) -> requests.Response:
        """
        Returns the last run job and its current state for workflows
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/workflows/jobs'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_all_workflows(self, headers=None, params=None) -> requests.Response:
        """
        Return all workflows, optionally filtered by date
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/workflows/all'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def get_workflows(self, headers=None, params=None) -> requests.Response:
        """
        Finds workflows in a Gallery
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        endpoint = 'admin/v1/workflows'
        response = self._make_request(Method.GET.value, endpoint=endpoint, headers=headers, params=params)
        return response

    def post_workflows(self, headers=None, params=None) -> requests.Response:
        """
        Publishes a YXZP to the system
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        raise NotImplementedError

    def put_migration_flag(self, headers=None, params=None) -> requests.Response:
        """
        Updates an App's ready for migration flag
        :param headers: An optional parameter denoting any headers you would like to pass to the request
        :param params: An optional parameter denoting any parameters you would like to pass to the request
        :return: A requests Response (application/json) by default unless specified otherwise in the header
        """
        raise NotImplementedError
