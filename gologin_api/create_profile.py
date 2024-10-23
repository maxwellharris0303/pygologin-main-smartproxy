import os
from dotenv import load_dotenv
import json
import requests
from datetime import datetime

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")


def create():
    current_time = datetime.now()
    # Format the current time as string
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # Print the formatted time
    # print("Formatted time:", formatted_time)

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "name": f"profile-{formatted_time}",
        "notes": "string",
        "browserType": "chrome",
        "os": "lin",
        "startUrl": "string",
        "googleServicesEnabled": False,
        "lockEnabled": False,
        "debugMode": False,
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
        "geoProxyInfo": {},
        "storage": {
            "local": True,
            "extensions": True,
            "bookmarks": True,
            "history": True,
            "passwords": True,
            "session": True
        },
        "proxyEnabled": True,
        "proxy": {
            "mode": "http",
            "host": "string",
            "port": 0,
            "username": "string",
            "password": "string"
        },
        "dns": "string",
        "plugins": {
            "enableVulnerable": True,
            "enableFlash": True
        },
        "timezone": {
            "enabled": True,
            "fillBasedOnIp": True,
            "timezone": "string"
        },
        "audioContext": {
            "mode": "off",
            "noise": 0
        },
        "canvas": {
            "mode": "off",
            "noise": 0
        },
        "fonts": {
            "families": [
                "string"
            ],
            "enableMasking": True,
            "enableDomRect": True
        },
        "mediaDevices": {
            "videoInputs": 0,
            "audioInputs": 0,
            "audioOutputs": 0,
            "enableMasking": False
        },
        "webRTC": {
            "mode": "alerted",
            "enabled": True,
            "customize": True,
            "localIpMasking": False,
            "fillBasedOnIp": True,
            "publicIp": "string",
            "localIps": [
                "string"
            ]
        },
        "webGL": {
            "mode": "noise",
            "getClientRectsNoise": 0,
            "noise": 0
        },
        "clientRects": {
            "mode": "noise",
            "noise": 0
        },
        "webGLMetadata": {
            "mode": "mask",
            "vendor": "string",
            "renderer": "string"
        },
        "webglParams": [],
        "profile": "string",
        "googleClientId": "string",
        "updateExtensions": True,
        "chromeExtensions": [
            "string"
        ]
    }

    url = f'{BASE_URL}browser'

    response = requests.post(url, headers=headers, json=data)

    json_data = response.json()
            
    # Prettify the JSON
    # prettified_json = json.dumps(json_data, indent=4)
    profile_id = json_data['id']
    print(f"Profile ID: {profile_id}")
    return profile_id