from qaseio.pytest import qase


class TestClass:

    @qase.id(1)
    def test_authorization(self):
        assert 1 == 1, ""

    @qase.id(2)
    def test_sign_up(self):
        assert 1 != 1, "Assertion failed to to unexpected value"
