import allure
from qaseio.pytest import qase


class TestSteps:

    @allure.step
    @qase.step("Go to sign up page https://qase.io/login")
    def step_one(self):
        print("complete step 1")

    @allure.step
    @qase.step('Fill the form with login "test" and password "test"')
    def step_two(self):
        print("complete step 2")

    @allure.step
    @qase.step('Check "remember me" checkbox')
    def step_three(self):
        print("complete step 3")

    @allure.step
    @qase.step('Click on the "Login" button')
    def step_four(self):
        assert 1 == 1, ""
