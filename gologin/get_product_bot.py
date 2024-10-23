import json
import requests
from collections import OrderedDict
import os
import glob

def get_product(location, sku):
    

    def get_json_files(folder_path):
        json_files = glob.glob(os.path.join(folder_path, '*.json'))
        return json_files

    folder_path = 'headers'  # Replace with the actual folder path
    header_files = get_json_files(folder_path)
    print(header_files)

    headers_array = []
    proxy_hosts = []
    proxy_ports = []
    proxy_usernames = []
    proxy_passwords = []
    for header_file in header_files:
        # Load headers from the JSON file
        with open(header_file, 'r') as json_file:
            headers_data = json.load(json_file)
        # print(headers_data['x-hermes-locale'])
        temp_headers = {}
        if location in headers_data['x-hermes-locale']:
            for header_name, header_value in headers_data.items():
                if header_name != "proxy_username" and header_name != "proxy_password" and header_name != "proxy_host" and header_name != "proxy_port":
                    temp_headers[header_name] = header_value
                elif header_name == "proxy_username":
                    proxy_usernames.append(header_value)
                elif header_name == "proxy_password":
                    proxy_passwords.append(header_value)
                elif header_name == "proxy_host":
                    proxy_hosts.append(header_value)
                elif header_name == "proxy_port":
                    proxy_ports.append(header_value)

            headers_array.append(temp_headers)

    if len(headers_array) == 0:
        print(f"No header for '{location}'")
        return f"No header for '{location}'"
    
    index = 0
    for _ in range(len(headers_array)):
        proxies = {
            'http': f'http://{proxy_usernames[index]}:{proxy_passwords[index]}@{proxy_hosts[index]}:{proxy_ports[index]}',
            'https': f'http://{proxy_usernames[index]}:{proxy_passwords[index]}@{proxy_hosts[index]}:{proxy_ports[index]}',
        }


        # url = f"https://bck.hermes.com/product?locale={headers_array[index]['x-hermes-locale']}&productsku={sku}"
        url = f"https://httpbin.org/ip"
        print(url)
        response = requests.get(url, proxies=proxies)

        # Check if the response is in JSON format
        if response.headers.get('content-type') == 'application/json':
            # Parse the JSON response
            json_data = response.json()
            
            # Prettify the JSON
            prettified_json = json.dumps(json_data, indent=4)
            
            print(prettified_json)
            return prettified_json
        else:
            print("Response is not in JSON format.")
            json_data = response.json()
            
            # Prettify the JSON
            prettified_json = json.dumps(json_data, indent=4)
            
            print(prettified_json)
            # continue
            # continue
        index += 1

    return "Not found product"
    
