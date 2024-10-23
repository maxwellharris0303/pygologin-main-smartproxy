import os
from dotenv import load_dotenv
import json
import requests
import random

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
PROXY_DOMAIN = os.getenv("PROXY_DOMAIN")

def add_proxy(profile_id):
    

    with open('proxy_port_index.txt', "r") as file:
        proxy_port = file.read()

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        # "autoProxyRegion": "us",
        "mode": "http",
        "host": PROXY_DOMAIN,
        "port": proxy_port,
        "username": PROXY_USERNAME,
        "password": PROXY_PASSWORD
        # "torProxyRegion": "us",
        
    }
    # proxy_port = int(proxy_port)
    url = f'{BASE_URL}browser/{profile_id}/proxy'
    with open('proxy_port_index.txt', "w") as file:
        file.write(str(int(proxy_port) + 1))

    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 204:
        return proxy_port
    else:
        return "Failed"