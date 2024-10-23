import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}
url = f'{BASE_URL}browser/v2'

response = requests.get(url, headers=headers)

json_data = response.json()
        
# Prettify the JSON
prettified_json = json.dumps(json_data, indent=4)

print(prettified_json)