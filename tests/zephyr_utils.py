from __future__ import annotations

import json
import os
from time import sleep

import requests
from decohints import decohints
from dotenv import load_dotenv

from tests.test_base import logger


@decohints
def retry(times: int = 10, delay: float | int = 1, deco_type: str = "default", is_get_dag: bool = False,
          records_number: int | None = None, **retry_kwargs):
    """
    retry decorator
    :param times:
    :param delay:
    :param deco_type: default, airflow, no_records, has_response, df
    :param is_get_dag:
    :param records_number:
    :param retry_kwargs:
    :return:
    """

    # Retry Decorator
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    res = func(*args, **kwargs)
                    retry_kwargs.update(kwargs)
                    return handle_deco_args(res, deco_type, is_get_dag, records_number, **retry_kwargs)
                except Exception as e:
                    if not isinstance(e, WaitException):
                        logger.warning(e)
                    attempt += 1
                    sleep(delay)
            return False

        return newfn

    return decorator


class Zephyr:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('ZEPHYR_HOST')
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv('ZEPHYR_TOKEN')}"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def handle_get_request(self, endpoint: str, get_params: dict | None = None):
        """
        Handles get requests
        :param endpoint:
        :param get_params:
        :return:
        """
        try:
            return json.loads(
                self.session.get(
                    f"{self.host}/{endpoint}{dict_to_api_params(get_params)}").text)
        except json.JSONDecodeError:
            return {}

    def get_projects(self, _dict: dict | None = None) -> dict:
        """
        Returns zephyr projects
        :param _dict: keys -> maxResults, startAt
        :return:
        """
        return self.handle_get_request('projects', _dict)

    def get_test_cases(self, project_key: str, _dict: dict | None = None):
        obj = {"project_key": project_key, **(_dict if _dict else {})}
        return self.handle_get_request('testcases', obj)

    def get_test_cycles(self, project_key: str, _dict: dict | None = None):
        obj = {"project_key": project_key, **(_dict if _dict else {})}
        return self.handle_get_request('testcycles', obj)

    def get_environments(self, project_key: str, _dict: dict | None = None):
        obj = {"project_key": project_key, **(_dict if _dict else {})}
        return self.handle_get_request('environments', obj)

    def get_test_cycle_by_name_or_id(self, test_cycle_id: str | int):
        return self.handle_get_request(f'testcycles/{test_cycle_id}')

    @retry()
    def create_test_cycle(self, project_key: str, name: str, _dict: dict | None = None):
        params = {"projectKey": project_key,
                  "name": name,
                  **(_dict if _dict else {})}
        return json.loads(requests.post(f"{self.host}/testcycles", json=params, headers=self.headers).text)

    @retry()
    def create_test_execution(self, project_key: str, test_case_key, test_cycle_key: str, test_status,
                              _dict: dict | None = None):
        params = {"projectKey": project_key,
                  "testCaseKey": test_case_key,
                  "statusName": test_status,
                  "testCycleKey": test_cycle_key,
                  **(_dict if _dict else {})}
        return json.loads(self.session.post(f"{self.host}/testexecutions", json=params).text)

    def create_issue_link_to_test_run(self, test_execution_id: int, jira_issue_id: int) -> None:
        self.session.post(f"{self.host}/testexecutions/{test_execution_id}/links/issues",
                          json={"issueId": jira_issue_id})

    def get_single_test_case_by_id(self, test_case_id: str) -> dict:
        return self.handle_get_request(f'testcases/{test_case_id}')

    def get_test_case_steps(self, test_case_id: str) -> dict:
        return self.handle_get_request(f'testcases/{test_case_id}/teststeps')

    def post_test_case_steps(self, test_case_id: str, mode: str, steps: [object]):
        """
        :param test_case_id: [A-Z]+-T[0-9]+
        :param mode: "APPEND", "OVERWRITE"
        :param steps: list of test case steps with details
        """
        response = self.session.post(f'{self.host}/testcases/{test_case_id}/teststeps',
                                     json={
                                         "mode": mode,
                                         "items": steps
                                     })
        print(response)

    def get_statuses_for_entity(self, entity_name: str, project_key: str, _dict: dict | None = None):
        obj = {"statusType": entity_name,
               "projectKey": project_key,
               **(_dict if _dict else {})}
        return self.handle_get_request('statuses', obj)

    def update_test_cycle(self, test_cycle_id: int, status: str, project_name: str) -> None:
        current_test_cycle = self.get_test_cycle_by_name_or_id(test_cycle_id)
        # get statuses for test_execution
        test_cycle_statuses = self.get_statuses_for_entity('TEST_CYCLE', project_name, {"maxResults": 20})
        try:
            updated_status_id = [x['id'] for x in test_cycle_statuses['values'] if x['name'] == status][0]
            current_test_cycle['status'] = {"id": updated_status_id}
            self.session.put(f"{self.host}/testcycles/{test_cycle_id}", json=current_test_cycle)
        except (IndexError, AttributeError):
            logger.error(f"Test execution with id={test_cycle_id} was not updated")

    def get_test_executions(self, project_name: str, _dict: dict | None = None) -> dict:
        obj = {"projectKey": project_name,
               **(_dict if _dict else {})}
        return self.handle_get_request("testexecutions", obj)

    def get_single_test_execution(self, test_execution_id: int, _dict: dict | None = None) -> dict:
        return self.handle_get_request(f"testexecutions/{test_execution_id}", _dict)

    def update_test_case(self, test_case_key: str, _dict: dict) -> None:
        response = self.session.put(f"{self.host}/testcases/{test_case_key}", json=_dict)
        if response.status_code != 200:
            logger.error(f"Test case with key={test_case_key} was not updated. "
                         f"Status code: {response.status_code}"
                         f"Response: {response.text}")

    def __del__(self):
        # close http session in the end
        self.session.close()


def dict_to_api_params(_dict: dict | None) -> str:
    """
    Updates dict to str for get api call
    :param _dict:
    :return:
    """
    try:
        joined_params = "&".join([f"{k}={v}" for k, v in _dict.items()])
        return '?' + joined_params if joined_params else ''
    except AttributeError:
        return ''


def handle_deco_args(func_resp, deco_type, is_get_dag, records_number, **kwargs):
    if deco_type == 'airflow' and is_get_dag == True and func_resp['dag_runs']:
        return func_resp
    if deco_type == 'airflow' and (func_resp == 'success' or func_resp == 'failed'):
        return True if func_resp == 'success' else False
    elif ((records_number and len(func_resp) == deco_type)
          or deco_type == 'default'
          or (deco_type == 'has_response' and func_resp)):
        return func_resp
    elif deco_type == 'df' and not func_resp.empty:
        return func_resp
    elif deco_type == 'no_records' and (func_resp[0][0] or not func_resp) == 0:
        return True
    raise WaitException


class WaitException(Exception):
    pass
