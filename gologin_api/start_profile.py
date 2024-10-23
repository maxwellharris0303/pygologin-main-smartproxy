import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

def start(profile_id):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "profileId": profile_id,
        "sync": True
    }
    url = f'http://135.181.241.84:36912/browser/start-profile'

    response = requests.post(url, headers=headers, json=data)
    json_data = response.json()
            
    # Prettify the JSON
    prettified_json = json.dumps(json_data, indent=4)

    print(prettified_json)
