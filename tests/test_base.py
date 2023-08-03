from qaseio.pytest import qase


class TestClass:

    @qase.suite("Authorization")
    @qase.id(1)
    @qase.title("Authorization")
    def test_authorization(self):
        assert 1 == 1, ""

    @qase.suite("Authorization")
    @qase.id(2)
    @qase.title("Sign up")
    def test_sign_up(self):
        assert 1 != 1, "Assertion failed to to unexpected value"
