import json

import requests

from file_util import zip_file, get_path_dir
from helper import check_response_status, find_folder_id_by_name

BASE_URL = "https://api.zephyrscale.smartbear.com/v2"


def publish(zephyr_token, project_key, source_report_file, report_format, auto_create_test_cases="true"):
    if does_zephyr_token_exist(zephyr_token) is False:
        return

    url = BASE_URL + f"/automations/executions/{report_format}"
    source_path_dir = get_path_dir(source_report_file)
    output_zip = f"{source_path_dir}/testResults.zip"
    zip_file(source_report_file, output_zip)

    params = {
        "projectKey": project_key,
        "autoCreateTestCases": auto_create_test_cases
    }
    headers = {
        "Authorization": "Bearer " + zephyr_token
    }
    files = {
        "file": open(output_zip, 'rb')
    }

    print(f"Sending results to Zephyr Scale...")
    response = requests.post(url, files=files, params=params, headers=headers)
    check_response_status(response, 200)
    parsed_response = json.loads(response.text)
    print(f"Parsed response: {parsed_response}")
    return parsed_response


def publish_customized_test_cycle(zephyr_token,
                                  project_key,
                                  source_report_file,
                                  report_format,
                                  auto_create_test_cases="true",
                                  test_cycle_name="Automated Build",
                                  test_cycle_folder_name="All test cycles",
                                  test_cycle_description="",
                                  test_cycle_jira_project_version=1,
                                  test_cycle_custom_fields=None):
    if does_zephyr_token_exist(zephyr_token) is False:
        return
    if test_cycle_custom_fields is None \
            or test_cycle_custom_fields == "" \
            or test_cycle_custom_fields == "{}":
        test_cycle_custom_fields = {}

    url = BASE_URL + f"/automations/executions/{report_format}"
    source_path_dir = get_path_dir(source_report_file)
    output_zip = f"{source_path_dir}/testResults.zip"
    zip_file(source_report_file, output_zip)

    test_cycle = customize_test_cycle(zephyr_token,
                                      project_key,
                                      test_cycle_name,
                                      test_cycle_folder_name,
                                      test_cycle_description,
                                      test_cycle_jira_project_version,
                                      test_cycle_custom_fields)
    params = {
        "projectKey": project_key,
        "autoCreateTestCases": auto_create_test_cases
    }
    headers = {
        "Authorization": "Bearer " + zephyr_token
    }
    files = {
        "file": open(output_zip, 'rb'),
        "testCycle": ("test_cycle.json", test_cycle, "application/json")
    }

    print(f"Sending results to Zephyr Scale...")
    response = requests.post(url, files=files, params=params, headers=headers)
    check_response_status(response, 200)
    parsed_response = json.loads(response.text)
    print(f"Parsed response: {parsed_response}")
    return parsed_response


def does_zephyr_token_exist(zephyr_token):
    if zephyr_token is None:
        print("Zephyr Scale API Access Token is not provided. Results will not be published to Zephyr Scale.")
        return False
    return True


def customize_test_cycle(zephyr_token,
                         project_key,
                         test_cycle_name="Automation cycle",
                         folder_name="All test cycles",
                         description="",
                         jira_project_version=1,
                         custom_fields=None):
    if custom_fields is None:
        custom_fields = {}
    folder_id = get_folder_id_by_name(zephyr_token, folder_name, project_key, 20)
    test_cycle_json = {
        "name": test_cycle_name,
        "description": description,
        "jiraProjectVersion": jira_project_version,
        "folderId": folder_id,
        "customFields": custom_fields
    }
    print(f"Custom test cycle is generated: {test_cycle_json}")
    return json.dumps(test_cycle_json)


def get_folder_id_by_name(zephyr_token, name, project_key, max_results):
    url = BASE_URL + f"/folders"

    params = {
        "projectKey": project_key,
        "folderType": "TEST_CYCLE",
        "startAt": 0,
        "maxResults": max_results
    }
    headers = {
        "Authorization": "Bearer " + zephyr_token
    }

    response = requests.get(url, params=params, headers=headers)
    check_response_status(response, 200)
    parsed_response = json.loads(response.text)
    return find_folder_id_by_name(name, parsed_response)
