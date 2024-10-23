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

profile_id_array = []
print(len(json_data['profiles']))
for profile in json_data['profiles']:
    profile_id_array.append(profile['id'])

print(profile_id_array)


headers = {
    'Authorization': f'Bearer {TOKEN}'
}
for profile_id in profile_id_array:
    url = f'{BASE_URL}browser/{profile_id}'

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Success")
    else:
        print("Failed")