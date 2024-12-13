import json
import requests
import argparse

# Helper functions
def paginate(items, page_size, page_number):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return items[start_index:end_index]

def api_request(method, url, headers, payload=None):
    """Generic API request handler."""
    response = requests.request(method, url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
    
def get_rule_folders(profile_id, api_key):
    url = f"https://api.controld.com/profiles/{profile_id}/groups"

    headers = {
        "accept": "application/json",
        "authorization": api_key
    }

    return api_request("GET", url, headers)

def get_domains(url):
    with requests.get(url) as response:
        response.raise_for_status()
        json_data = response.json()
    return [rule["PK"] for rule in json_data.get("rules", [])]



def delete_rule_folder(profile_id, folder_id, api_key):
    url = f"https://api.controld.com/profiles/{profile_id}/groups/{folder_id}"

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key
    }

    api_request("DELETE", url, headers)

def create_rule_folder(name, do, status, profile_id, api_key):
    url = f"https://api.controld.com/profiles/{profile_id}/groups"

    payload = {
        "name": name,
        "do": do,
        "status": status
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key
    }

    api_request("POST", url, headers, payload)


def create_folder_rules(profile_id, api_key, do, status, group, hostnames):
    url = f"https://api.controld.com/profiles/{profile_id}/rules"

    payload = {
        "do": do,
        "status": status,
        "group": group,
        "hostnames[]": hostnames
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key
    }

    api_request("POST", url, headers, payload)

    print(f"Successfully updated rule folder '{group_name}' with {len(hostnames)} domains.")


# Main script logic
# Initialize parser
parser = argparse.ArgumentParser()

# Adding arguments
parser.add_argument("-a", "--api_key", required=True, help="API Key for authorization")
parser.add_argument("-p", "--profile_id", required=True, help="Profile ID")
parser.add_argument("-g", "--group_name", required=True, help="Name of the rule group")
parser.add_argument("-b", "--blocklist_url", required=True, help="URL of the blocklist")

# Read arguments from command line
args = parser.parse_args()

# Assign arguments to variables
api_key = args.api_key
profile_id = args.profile_id
group_name = args.group_name
blocklist_url = args.blocklist_url

# Get data
domains = get_domains(blocklist_url)

# delete old folder
profiles = get_rule_folders(profile_id, api_key)
for group in profiles["body"]["groups"]: 
    if group["group"] == group_name:
        group_id = group["PK"]
        delete_rule_folder(profile_id, group_id, api_key)

# create new folder
create_rule_folder(group_name, 0, 1, profile_id, api_key)

# load domains
profiles = get_rule_folders(profile_id, api_key)
for group in profiles["body"]["groups"]: 
    if group["group"] == group_name:
        group_id = group["PK"]

# break into pages and create rules
page_size = 500 # page size
page_number = 1 # init page

while paginate(domains, page_size, page_number) != []:
    create_folder_rules(profile_id, api_key, 0, 1, group_id, paginate(domains, page_size, page_number))
    page_number += 1