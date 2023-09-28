import allure
from qaseio.pytest import qase

from steps import TestSteps


@allure.suite("Authorization")
@qase.suite("Authorization")
class TestClass:

    @qase.id(1)
    @allure.title("Authorization test")
    @qase.title("Authorization")
    def test_authorization(self):
        steps = TestSteps()
        steps.step_one()
        steps.step_two()
        steps.step_three()
        steps.step_four()

    @qase.id(2)
    @allure.title("Sign up")
    @qase.title("Sign up")
    @qase.fields(("automation status", "automated"))
    def test_sign_up(self):
        with qase.step('Open "Sign Up" page: https://qase.io/signup'):
            print('Open "Sign Up" page: https://qase.io/signup')
        with qase.step('Fill form with the following credentials:'):
            print('Fill form with the following credentials:')
        with qase.step('Click Submit button'):
            print('Click Submit button')
        with qase.step('Open email application'):
            print('Open email application')
        with qase.step('Confirm account registration by clicking on the confirm button from the email'):
            assert 1 == 1, "Assertion failed to to unexpected value"

    @qase.id(3)
    @allure.title("Pwd rst")
    @qase.title("Pwd rst")
    def test_pwd_rst(self):
        with qase.step("do this"):
            print("complete step 1")
        with qase.step('do that'):
            print("complete step 2")
        with qase.step('check it'):
            print("complete step 3")
        with qase.step('got this'):
            assert 1 != 1, "failed assertion validation"

    @allure.title("New created scranrio")
    @qase.title("New created scranrio")
    def test_new_scenario(self):
        with qase.step("do this"):
            print("complete step 1")
        with qase.step('do that'):
            print("complete step 2")
        with qase.step('check it'):
            print("complete step 3")
        with qase.step('got this'):
            assert 1 != 1, "failed assertion validation"
