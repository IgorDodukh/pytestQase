import copy
import math
import os
from datetime import datetime, timedelta
from typing import Union

import pytest
from _pytest.config import Config
from tabulate import tabulate

from tests.prometheus_worker import PrometheusReport, TestStatus
from tests.zephyr.models import TestCase
from tests.zephyr_utils import Zephyr

TEST_TYPES = ["ui", "api", "integration", "e2e"]
COMPONENTS = ["component1", "component2", "component3"]
automated_test_user_id = "62b58da39abb660ab14c8a0f"
TC_STATUS = {
    "DRAFT": 4855784,
    "DEPRECATED": 4855785,
    "APPROVED": 4855786,
}

zephyr = Zephyr()


class ZephyrStatus:
    IN_PROGRESS = "In Progress"
    FAIL = "Fail"
    PASS = "Pass"
    NOT_EXECUTED = "Not Executed"


class ExecutionStatus:
    FAIL = ZephyrStatus.FAIL
    PASS = ZephyrStatus.PASS
    NOT_EXECUTED = ZephyrStatus.NOT_EXECUTED
    WITH_ERRORS = "With Errors"
    ERRORS_AND_FAIL = "Errors and Fail"


class CycleStatus:
    IN_PROGRESS = ZephyrStatus.IN_PROGRESS
    NOT_EXECUTED = ZephyrStatus.NOT_EXECUTED
    DONE = "Done"

class MarkName:
    ID = "id"
    COMPONENT = "component"

# Test case executed
# get TC Zephyr id from tags
# if no TC id - create new test case in Zephyr
# if TC id exist - try to get TC with this ID from Zephyr
# if success - update this test case with existing
#


def get_test_markers(item):
    markers = [x.name for x in item.own_markers]
    test_type = [i for i in markers if i in TEST_TYPES]
    # add component, and other test specific categories
    return test_type


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(call, item):
    """
    4 -> executed in fixtures
    Creates test cycle after first test that is registered in zephyr
    """
    pytest.step_results = []
    # execute all other hooks to obtain the report object
    outcome = yield
    res = outcome.get_result()
    # check if we would like to grab test execution results
    if call.when == 'call':
        # add errors for failure in errors:
        # if res.outcome == 'failed':
        #     pytest.errors.append(res.longreprtext)
        # try:
        # get all currently selected tests
        test_case = TestCase()
        test_case.parse_item(item)

        # get markers
        markers = [x.name for x in item.own_markers]
        test_case.labels = [i for i in markers if i in TEST_TYPES]

        if not test_case.id:
            print(f"Test case [{test_case.name}] is not marked with @pytest.mark.id")
        else:
            zephyr_test_case_data = zephyr.get_single_test_case_by_id(test_case_id=test_case.id)

            test_contains_steps = zephyr_test_case_data['testScript']['self'].endswith('teststeps')
            zephyr_test_steps = zephyr.get_test_case_steps(test_case_id=test_case.id) if test_contains_steps else 0

            # Update test case data
            zephyr_test_case_data["name"] = test_case.name
            zephyr_test_case_data["objective"] = test_case.description
            zephyr_test_case_data["labels"] = test_case.labels
            zephyr_test_case_data["customFields"] = {
                "Jenkins link": "https://jenkins.com/jobs/123123",
            }

            # Publish updated test case to Zephyr
            zephyr.update_test_case(test_case.id, zephyr_test_case_data)

            # Update test case steps
            steps = []
            for step in test_case.steps:
                steps.append({
                    "inline": {
                        "description": step["step"],
                        "testData": step["args"] if step["args"] else "",
                        "expectedResult": "",
                    }
                })
            zephyr.post_test_case_steps(test_case.id, mode="OVERWRITE", steps=steps)

            # Collect test data for test run
            # Publish test run to Zephyr

        pytest.zephyr_project_name, case_number = item.originalname.split("_")[-2:]
        this_test_case_zephyr_data = zephyr.get_single_test_case_by_id(
            f"{pytest.zephyr_project_name}-{case_number}")
        # check if current test is testscript or teststeps
        try:
            this_tc_script_steps = (zephyr.get_test_case_steps(this_test_case_zephyr_data['key'])['total']
                                    if this_test_case_zephyr_data['testScript']['self'].endswith(
                'teststeps') else 0)
        except KeyError:
            this_tc_script_steps = 0
        is_in_zephyr = False
        # try to create a test cycle in case we are missing it (after first test case execution)

        if is_in_zephyr:
            if not pytest.test_cycle:
                # check jenkins job
                # try:
                # if os.getenv('JOB_URL'):
                #     soap = BeautifulSoup(this_test_case_zephyr_data['customFields']['Jenkins links'])
                #     # find all links:
                #     all_current_jlinks = [x['href'] for x in soap.find_all(['a'])]
                #     if os.getenv('JOB_URL') not in all_current_jlinks or not all_current_jlinks:
                #         all_current_jlinks.append(os.getenv('JOB_URL'))
                #         this_test_case_zephyr_data['customFields']['Jenkins links'] = '<br/>'.join([
                #             f"""<a href="{x}" rel="noopener noreferrer" target="_blank">{x.strip("/").split('/')[-1]}</a>"""
                #             for x in
                #             all_current_jlinks])
                #         zephyr.update_test_case(this_test_case_zephyr_data['key'], this_test_case_zephyr_data)
                # except AttributeError:
                #     pass
                description = os.getenv('JOB_NAME').split("/")[-1] if os.getenv(
                    'JOB_NAME') else item.session.name + " local"
                test_cycle_params = {"statusName": CycleStatus.IN_PROGRESS,
                                     "plannedStartDate": datetime.utcnow().strftime(
                                         '%Y-%m-%dT%H:%M:%SZ'),
                                     "plannedEndDate": (
                                             datetime.utcnow() + timedelta(
                                         hours=1)).strftime(
                                         '%Y-%m-%dT%H:%M:%SZ')}
                if os.getenv('ZEPHYR_FOLDER_ID'):
                    test_cycle_params['folderId'] = int(os.getenv('ZEPHYR_FOLDER_ID'))
                pytest.test_cycle = zephyr.create_test_cycle(pytest.zephyr_project_name, description,
                                                             test_cycle_params)
            env = os.getenv('ZEPHYR_ENV')
            test_execution_env = env if env in [x['name'] for x in
                                                zephyr.get_environments(pytest.zephyr_project_name)[
                                                    'values']] else None
            # called params:
            params_arr = []
            params = None
            try:
                params = item.callspec.params
            except AttributeError:
                pass
            current_test_run_status = ExecutionStatus.PASS
            if pytest.errors and res.outcome == 'failed':
                current_test_run_status = ExecutionStatus.ERRORS_AND_FAIL
            elif res.outcome == 'failed':
                current_test_run_status = ExecutionStatus.FAIL
            elif pytest.errors:
                current_test_run_status = ExecutionStatus.FAIL
            total_time = math.floor(res.duration * 1000)
            # merge step results
            merged_results = []
            for step in list(dict.fromkeys([x['step'] for x in pytest.step_results])):
                step_results = [x for x in pytest.step_results if x['step'] == step]
                shared_status = ('Fail'
                                 if any([x for x in step_results if x['statusName'] == 'Fail'])
                                 else 'With Errors'
                if any([x for x in step_results if x['statusName'] == 'With Errors'])
                else 'Pass')
                [x.pop('step', None) for x in copy.deepcopy(step_results)]
                merged_results.append({"statusName": shared_status,
                                       "actualResult": tabulate(step_results,
                                                                headers='keys',
                                                                tablefmt='html', colalign=("center", "center"))})
            # check if test steps results != that are in spec -> cut or add results
            if len(merged_results) < this_tc_script_steps:
                # logger.warning(f"Number of steps in file less than expected. "
                #                f"Got {len(merged_results)} instead of {this_tc_script_steps}")
                other_steps_results = [{"statusName": ExecutionStatus.NOT_EXECUTED} for _ in
                                       range(this_tc_script_steps - len(merged_results))]
                merged_results.extend(other_steps_results)
            elif len(merged_results) > this_tc_script_steps:
                # logger.warning(f"Number of steps in file greater than expected. "
                #                f"Got {len(merged_results)} instead of {this_tc_script_steps}")
                merged_results = merged_results[:this_tc_script_steps]
            test_execution_dict = {"executionTime": total_time,
                                   "executedById": automated_test_user_id,
                                   "testScriptResults": merged_results if merged_results else [
                                       {"statusName": current_test_run_status}]}
            # add environment to test execution
            if test_execution_env:
                test_execution_dict["environmentName"] = test_execution_env
            if params:
                params_arr.append(
                    "<h2>Input parameters</h2><br/>" + tabulate([(k, v) for k, v in params.items()],
                                                                ['parameter', 'value'],
                                                                tablefmt='html', colalign=("center", "center")))
            # add called params as comment:
            # add called params as comment:
            called_args = ([x.replace('--', '').split('=') for x in item.config.invocation_params.args if
                            x.startswith('--') and "=" in x])
            if called_args:
                params_arr.append(
                    "<h2>Called with parameters</h2><br/>" + tabulate(called_args, ['parameter', 'value'],
                                                                      tablefmt='html',
                                                                      colalign=("center", "center")))
            # check test blocks and add them to params :
            if pytest.tc_comment:
                params_arr.append("<h2>Outputs</h2><br/>" + pytest.tc_comment)
            # put all params in the comments as separate tables:
            if params_arr:
                test_execution_dict["comment"] = '<br/><br/>'.join(params_arr)
            # get test run statuses from current test cycle:
            current_test_cycle_executions = zephyr.get_test_executions(pytest.zephyr_project_name,
                                                                       {"testCycle": pytest.test_cycle['key'],
                                                                        "maxResults": 500})
            # assume that by default current test run is the common test run result
            # get all previous runs for current test case. If there was any failure then status is Fail, if any with errors-> the sattus =With Errors
            if current_test_cycle_executions['values']:
                executions_status_ids = [x['testExecutionStatus']['id'] for x in
                                         current_test_cycle_executions['values']
                                         if
                                         x['testCase']['id'] == this_test_case_zephyr_data['id']]
                test_execution_statuses = \
                    zephyr.get_statuses_for_entity('TEST_EXECUTION', pytest.zephyr_project_name)[
                        'values']
                current_test_case_execution_statuses = [x['name'] for x in test_execution_statuses if
                                                        x['id'] in executions_status_ids]
                if [x for x in current_test_case_execution_statuses if x == 'Fail']:
                    current_test_run_status = 'Fail'
                elif [x for x in current_test_case_execution_statuses if x == 'With Errors']:
                    current_test_run_status = 'With Errors'
            test_execution = zephyr.create_test_execution(pytest.zephyr_project_name,
                                                          f"{pytest.zephyr_project_name}-{case_number}",
                                                          pytest.test_cycle['key'], current_test_run_status,
                                                          test_execution_dict)
            # todo: until fixed zephyr get test execution info
            pytest.execution = zephyr.get_single_test_execution(test_execution['id'])
            # create jira links:
            if pytest.jira_tickets:
                for ticket in pytest.jira_tickets:
                    zephyr.create_issue_link_to_test_run(test_execution['id'], ticket.id)
        # except ValueError:
        #     pass
        # test_case.clear()


@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(report, config: Config):
    if config.getoption('prometheus_pushgateway_url'):
        prom_rep = PrometheusReport(config)
        test_type = next((keyword for keyword in set(TEST_TYPES) if keyword in report.keywords), None)
        prom_rep.start_date = prom_rep.start_date or round(report.start * 1000)

        if report.when == 'call' or report.outcome == TestStatus.SKIPPED:
            test_case = TestCase()
            execution_time = round(report.duration)
            prom_rep.build_report(test_name=test_case.original_name, execution_time=execution_time, status=report.outcome,
                                  test_type=test_type, component_name=test_case.component)
            test_case.clear()

def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption(
        '--prometheus-pushgateway-url',
        default="http://localhost:9091",
        help='Push Gateway URL to send metrics to'
    )
    group.addoption(
        '--prometheus-prefix-name',
        default="qa_",
        help='Project name test cases are related to'
    )
    group.addoption(
        '--prometheus-extra-label',
        action='append',
        default=['environment=staging', 'project=Project1'],
        help='Extra labels to attach to reported metrics'
    )
    group.addoption(
        '--prometheus-job-name',
        default="qa_metrics",
        help='Value for the "job" key in exported metrics'
    )


def pytest_configure(config):
    if config.getoption('prometheus_pushgateway_url'):
        config._prometheus = PrometheusReport(config)
        config.pluginmanager.register(config._prometheus)


def pytest_unconfigure(config):
    prometheus = getattr(config, '_prometheus', None)

    if prometheus:
        del config._prometheus
        config.pluginmanager.unregister(prometheus)
