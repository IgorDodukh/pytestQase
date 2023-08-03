from qaseio.pytest import qase


class TestClass:

    @qase.suite("Authorization")
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

    @qase.suite("Authorization")
    @qase.id(2)
    @qase.title("Sign up")
    def test_sign_up(self):
        with qase.step(1):
            print()
        with qase.step(2):
            print()
        with qase.step(3):
            print()
        with qase.step(4):
            print()
        with qase.step(5):
            assert 1 != 1, "Assertion failed to to unexpected value"
