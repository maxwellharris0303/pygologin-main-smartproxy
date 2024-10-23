import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

def update_fingerprint(profile_id):
  headers = {
      'Authorization': f'Bearer {TOKEN}',
      'Content-Type': 'application/json'
  }
  data = {
    "instanceIds": [
      profile_id
    ]
  }

  url = f'{BASE_URL}browser/fingerprint/multi'

  response = requests.post(url, headers=headers, json=data)

  # json_data = response.json()
          
  # # Prettify the JSON
  # prettified_json = json.dumps(json_data, indent=4)
  if response.status_code == 201:
    return "Successfully generate new fingerprint"
  else:
    return "Failed generate new fingerprint"