import pytest
from decohints import decohints

from tests.zephyr.models import TestCase


@decohints
def step(func):
    def inner(*args, **kwargs):
        # check kwargs started with group
        test_case = TestCase()

        step_name = " ".join(func.__name__.split("_")).capitalize()
        k_dict = {k: v for k, v in kwargs.items() if k.startswith('group_')}
        test_case.steps.append({"statusName": 'Fail',
                                    "step": step_name,
                                    "args": k_dict})

        pytest.step_results.append({"statusName": 'Fail',
                                    "step": step_name,
                                    "args": k_dict})
        # check pytest errors before and after
        before_exec = test_case.errors[:]
        print(f"Started execution for {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished execution for {func.__name__}")
        test_case.steps[-1] = {"statusName": 'With Errors' if len(test_case.errors) > len(before_exec) else 'Pass',
                                   "actualResult": '<br/><br/>'.join(
                                       [str(x) for x in test_case.errors if x not in before_exec]),
                                   "step": step_name,
                                   "args": k_dict}
        return result
    return inner
