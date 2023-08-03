from qaseio.pytest import qase


class TestClass:

    @qase.id(1)
    @qase.title("Authorization")
    @qase.fields(
        ("severity", "critical"),
        ("priority", "hight"),
        ("layer", "e2e"),
        ("description", "Try to login in Qase TestOps using login and password"),
        ("description", "*Precondition 1*. Markdown is supported."),
    )
    def test_authorization(self):
        assert 1 == 1, ""

    @qase.id(2)
    @qase.title("Sign up")
    @qase.fields(
        ("severity", "critical"),
        ("priority", "hight"),
        ("layer", "e2e"),
        ("description", "Sign up user"),
        ("description", "*Precondition 1*. Markdown is supported."),
    )
    def test_sign_up(self):
        assert 1 != 1, "Assertion failed to to unexpected value"
