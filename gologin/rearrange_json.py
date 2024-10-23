import json
from collections import OrderedDict

def change_headers_order(file_path, new_order):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file, object_pairs_hook=OrderedDict)

    # Rearrange the order of the keys
    rearranged_data = OrderedDict((key, data[key]) for key in new_order if key in data)

    # Write the data back to the file with the new order
    with open(file_path, 'w') as file:
        json.dump(rearranged_data, file, indent=4)

    print("Headers order has been changed successfully.")

# Example usage
# file_path = 'data.json'  # Path to your JSON file
# new_order = ['authority', 'Accept', 'accept-language', 'Cookie', 'DNT', 'Origin', 'Referer', 'sec-ch-ua', 'sec-ch-ua-mobile',
#              'sec-ch-ua-platform', 'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'User-Agent', 'x-hermes-locale', 'x-xsrf-token']  # Desired order of keys

# change_headers_order(file_path, new_order)