from qaseio.pytest import qase


@qase.suite("Authorization")
class TestClass:

    @qase.id(1)
    @qase.title("Authorization")
    def test_authorization(self):
        with qase.step("Go to sign up page https://qase.io/login"):
            print("complete step 1")
        with qase.step('Fill the form with login "test" and password "test"'):
            print("complete step 2")
        with qase.step('Check "remember me" checkbox'):
            print("complete step 3")
        with qase.step('Click on the "Login" button'):
            assert 1 == 1, ""

    @qase.id(2)
    @qase.title("Sign up")
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
            assert 1 != 1, "Assertion failed to to unexpected value"
