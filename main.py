import requests
import xml.etree.ElementTree as ET

# Qase.io API token
API_TOKEN = "94e3522eadbeff229978669e21f77f8a2b9f31b8263f4d2f7807bcc2f80cbaaf"

# Zephyr Scale XML file with test cases
XML_FILE_PATH = "test_cases.xml"

# Mapping from Zephyr Scale field names to Qase.io field names
FIELD_MAPPING = {
    "details": "description",
    "attachments": "attachments",
    "createdOn": "created_at",
    "labels": "tags",
    "name": "title",
    "priority": "priority",
    "parameters": "params",
}


def parse_xml_file(xml_file_path):
    """Parses the XML file with test cases and returns a list of test cases."""

    test_cases = []
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for test_case in root.find("testCases").findall("testCase"):
        test_case_data = {}
        for field in FIELD_MAPPING.keys():
            if field == "details":
                test_case_data[FIELD_MAPPING[field]] = test_case.find("testScript").find(field).text
            else:
                test_case_data[FIELD_MAPPING[field]] = test_case.find(field).text

        test_cases.append(test_case_data)

    return test_cases


def upload_test_cases_to_qase(test_cases, api_token):
    """Uploads the test cases to Qase.io using the API."""

    for test_case in test_cases:
        # Create a Qase.io test case object
        test_case_object = {
            "title": test_case["title"],
            "description": test_case["description"],
            # "priority": test_case["priority"],
            "tags": test_case["tags"],
        }
        print(test_case_object)

        # Upload the Qase.io test case object
        response = requests.post(
            "https://api.qase.io/v1/case/DEMMO",
            headers={"Token": f"{api_token}"},
            json=test_case_object,
        )

        # Check the response status code
        if response.status_code != 200:
            raise Exception(f"Failed to upload test case: {response.status_code} {response.text}")
        else:
            print(f"Imported successfully: {response.status_code} {response.text}")


if __name__ == "__main__":
    # Parse the XML file with test cases
    test_cases = parse_xml_file(XML_FILE_PATH)

    # Upload the test cases to Qase.io
    upload_test_cases_to_qase(test_cases, API_TOKEN)
