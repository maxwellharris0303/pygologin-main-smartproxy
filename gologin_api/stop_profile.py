import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

def stop(profile_id):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "profileId": profile_id
    }
    url = f'http://135.181.241.84:36912/browser/stop-profile'

    response = requests.post(url, headers=headers, json=data)

    print(response)
