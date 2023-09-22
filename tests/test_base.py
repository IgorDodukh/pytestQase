import time
from pathlib import Path

import pytest
import logging

# from zephyr import ZephyrScale

from tests.decorators import step
from tests.logger_util import get_logger

logger = get_logger(__name__)

@pytest.mark.skip
@pytest.mark.id("QT-T2")
def test_authorization_outside():
    """
    Test case to execute positive authorisation scenario
    """
    steps = TestSteps()
    steps.step_two()
    steps.step_two()


@pytest.mark.component("Authorization feature")
class TestClass:

    @pytest.mark.skip
    @pytest.mark.api
    @pytest.mark.id("QT-T3")
    def test_authorization(self):
        """
        Test case to execute positive authorisation scenario
        """
        steps = TestSteps()
        steps.step_one(1111, 2222)
        steps.step_three()
        steps.step_two()

    @pytest.mark.api
    def test_authorization_invalid(self, request):
        time.sleep(5)
        print(request)
        assert 1 != 1, ""
#
    @pytest.mark.api
    def test_authorization_negative(self):
        time.sleep(5)
        assert 1 == 1, ""
    @pytest.mark.integration
    def test_authorization_corner_case(self):
        time.sleep(2)
        assert 1 == 1, ""
#
#     @pytest.mark.api
#     @pytest.mark.skip
#     def test_authorization_renew_access(self):
#         # time.sleep(5)
#         assert 1 != 1, ""
#
#     @pytest.mark.api
#     @pytest.mark.id("QT-T4")
#     def test_sign_up(self):
#         # time.sleep(1)
#         steps = TestSteps()
#         steps.step_one()
#
#         assert 1 == 1, "Assertion failed to to unexpected value"
#
#     @pytest.mark.api
#     # @pytest.mark.skip
#     def test_restore_password(self):
#         time.sleep(2)
#         assert 1 == 1, "Failed to restore password"
#
#     @pytest.mark.integration
#     @pytest.mark.skip
#     def test_invalid_credentials(self):
#         time.sleep(2)
#         assert 1 == 1, "Assertion failed to to unexpected value"
#
#     @pytest.mark.integration
#     @pytest.mark.skip
#     def test_sign_up_existing_user(self):
#         # time.sleep(3)
#         assert 1 != 1, "Failed to restore password"
#
#
class TestSteps:

    @step
    def step_one(self, param1=1, param2=33):
        """
        Execute step 1 docstring
        :return:
        """
        time.sleep(5)
        print(f"step1: {self.__class__.__name__}")
        print(f"step1: {param1, param2}")

    @step
    def step_two(self):
        """
        Execute step 2 docstring
        :return:
        """
        print(f"step2: {self.__class__.__name__}")
        assert 1 != 1, ""

    @step
    def step_three(self):
        """
        Execute step 3 docstring
        :return:
        """
        logging.warning('Watch out!')  # will print a message to the console
        logging.info('I told you so')  # will not print anything
        print(f"step3: {self.__class__.__name__}")


# def zephyr_publisher():
#     # Zephyr Scale API Access Token. Suggestion: should be provided as environment variable to avoid security issues.
#     zephyr_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL2lob3Jkb2R1a2guYXRsYXNzaWFuLm5ldCIsInVzZXIiOnsiYWNjb3VudElkIjoiNTU3MDU4OmMyYTU0OWM2LWI0ZDMtNDQ5MS05OTI1LTE1NTA0MmQyZTdiOCJ9fSwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJzdWIiOiIxMTExNjA4Yy0yYmQ2LTM0MjMtYjI0MC0wNDU3NjljOGE4ZDYiLCJleHAiOjE3MjI2OTM4NjIsImlhdCI6MTY5MTE1Nzg2Mn0.Y6z9gFbGdtPp91YwgqCRFLSWakfOlK27DgAFcU7wBx0"
#
#     # Key name of the Jira project
#     project_key = "QT"
#
#     # Absolute path to the report file. E.g. "/Users/user/Project/report/cucumber.json"
#     source_report_file = Path(__file__).parent.parent.joinpath("reports").joinpath("out_report.xml")
#
#     # Report format. Possible values: "cucumber", "junit", "behave", "custom"
#     report_format = "junit"
#
#     # Automatically create test cases if they are absent in Zephyr Scale. Possible values: true, false
#     auto_create_test_cases = "true"
#
#     # # Execute
#     # publisher.publish(zephyr_token, project_key, source_report_file, report_format, auto_create_test_cases)
#
#     ########
#     # Customized test cycle name. Default: "Automated Build"
#     test_cycle_name = "Automated Build"
#
#     # Set test cycle folder to publish the results. Default: "All test cycles"
#     # IMPORTANT: the folder should be already created manually in Zephyr Scale "Test Cycles"
#     test_cycle_folder_name = "All test cycles"
#
#     # Customized test cycle description. Default: ""
#     test_cycle_description = "Test Cycle description"
#
#     # Set project version. Default: 1
#     test_cycle_jira_project_version = 1
#
#     # Set test cycle custom fields. E.g {"Sprint": 23}. Default: {}
#     test_cycle_custom_fields = {}
#
#     publisher.publish_customized_test_cycle(zephyr_token,
#                                             project_key,
#                                             source_report_file,
#                                             report_format,
#                                             auto_create_test_cases,
#                                             test_cycle_name,
#                                             test_cycle_folder_name,
#                                             test_cycle_description,
#                                             test_cycle_jira_project_version,
#                                             test_cycle_custom_fields)
#
#
# class ZephyrHelper:
#
#     def helper(self):
#         zephyr_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL2lob3Jkb2R1a2guYXRsYXNzaWFuLm5ldCIsInVzZXIiOnsiYWNjb3VudElkIjoiNTU3MDU4OmMyYTU0OWM2LWI0ZDMtNDQ5MS05OTI1LTE1NTA0MmQyZTdiOCJ9fSwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJzdWIiOiIxMTExNjA4Yy0yYmQ2LTM0MjMtYjI0MC0wNDU3NjljOGE4ZDYiLCJleHAiOjE3MjI2OTM4NjIsImlhdCI6MTY5MTE1Nzg2Mn0.Y6z9gFbGdtPp91YwgqCRFLSWakfOlK27DgAFcU7wBx0"
#
#         zscale = ZephyrScale(token=zephyr_token)
#         zapi = zscale.api
#         zapi.test_cases.create_test_case()
#
#
