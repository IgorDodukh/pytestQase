import json
import os

import requests
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    host = os.getenv('ZEPHYR_HOST')
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('ZEPHYR_TOKEN')}"
    }
    session = requests.session()
    session.headers.update(headers)

    response = session.get(f"{host}/testcases/QT-T3")
    formatted_response = json.loads(response.text)
