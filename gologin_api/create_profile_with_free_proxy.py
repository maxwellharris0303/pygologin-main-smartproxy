import os
from dotenv import load_dotenv
import json
import requests
import get_new_fingerprint

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

data = {
  "name": "345",
  "browserType": "chrome",
  "os": "lin",
  "navigator": {
    "userAgent": "string",
    "resolution": "string",
    "language": "string",
    "platform": "string",
    "doNotTrack": False,
    "hardwareConcurrency": 0,
    "deviceMemory": 1,
    "maxTouchPoints": 0
  },
  "proxyEnabled": True,
  "proxy": {
      "mode": "gologin",
      "autoProxyRegion": "us"
  }
}


url = f'{BASE_URL}browser'

response = requests.post(url, headers=headers, json=data)

json_data = response.json()
        
# Prettify the JSON
prettified_json = json.dumps(json_data, indent=4)

print(prettified_json)