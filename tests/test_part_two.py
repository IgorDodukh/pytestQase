import time

import pytest

@pytest.mark.component1
class TestNavigationSuite:

    @pytest.mark.ui
    def test_navigate_page_a(self):
        time.sleep(5)
        assert 1 != 1, ""

    @pytest.mark.integration
    def test_navigate_page_b(self):
        time.sleep(3)
        assert 1 != 1, ""
    @pytest.mark.ui
    def test_navigate_page_c(self):
        time.sleep(5)
        assert 1 == 1, ""

    @pytest.mark.integration
    def test_navigate_page_d(self):
        time.sleep(1)
        assert 1 != 1, ""
    @pytest.mark.ui
    def test_navigate_page_e(self):
        time.sleep(5)
        assert 1 == 1, ""

    @pytest.mark.integration
    def test_navigate_page_f(self):
        time.sleep(1)
        assert 1 == 1, ""

    @pytest.mark.ui
    def test_navigate_between_pages(self):
        time.sleep(1)
        assert 1 != 1, ""

    @pytest.mark.integration
    def test_negative_navigation(self):
        time.sleep(1)
        assert 1 == 1, "Assertion failed to to unexpected value"

    @pytest.mark.api
    def test_navigate_unauthorised_user(self):
        time.sleep(2)
        assert 1 == 1, "Failed to restore password"

    @pytest.mark.integration
    @pytest.mark.skip
    def test_navigate_to_invalid_pages(self):
        time.sleep(2)
        assert 1 == 1, "Assertion failed to to unexpected value"

    @pytest.mark.integration
    @pytest.mark.skip
    def test_navigate_without_cookies(self):
        time.sleep(1)
        assert 1 != 1, "Failed to restore password"
