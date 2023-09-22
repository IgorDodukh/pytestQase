from typing import Union

from decorators import singleton


@singleton
class TestCase:

    def __init__(self):
        self.name = None
        self.original_name = None
        self.id = None
        self.description = None
        self.labels = []
        self.steps = []
        self.errors = []
        self.component = None

    def parse_item(self, item):
        self.id = self.get_pytest_marker_args(item, marker_name="id")
        self.component = self.get_pytest_marker_args(item, marker_name="component")
        self.name = self.get_test_case_name(item)
        self.original_name = item.originalname
        self.description = self.get_test_case_docstring(item)

    def clear(self):
        self.__init__()

    @staticmethod
    def get_test_case_name(item) -> str:
        """
        Converts test function name into a string name with spaces and capitalized first letter.
        """
        return " ".join(item.originalname.split("_")[1:]).capitalize()

    @staticmethod
    def get_test_case_docstring(item):
        """
        Get test case description from the docstring. Return empty string if no description.
        """
        return item.obj.__doc__ if item.obj.__doc__ else ""

    @staticmethod
    def get_pytest_marker_args(item, marker_name) -> Union[str, None]:
        """
        Find pytest marks related to the current test case by name and get its argument.
        Pytest marks are collected from function level and class level.
        :param marker_name: pytest.mark marker name ("id", "component")
        :param item: test case information
        :return: string value of test case id
        """
        markers = item.own_markers + item.parent.own_markers
        for own_marker in markers:
            if own_marker.name == marker_name:
                return own_marker.args[0]
        return None
