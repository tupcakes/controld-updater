import requests
import json
import argparse

# API helper functions
def api_request(method, url, headers, payload=None):
    """Generic API request handler."""
    response = requests.request(method, url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()

def get_rule_folders(profile_id, api_key):
    """Fetch all rule folders for a given profile."""
    url = f"https://api.controld.com/profiles/{profile_id}/groups"
    headers = {"accept": "application/json", "authorization": api_key}
    return api_request("GET", url, headers)

def delete_rule_folder(profile_id, folder_id, api_key):
    """Delete a specific rule folder by ID."""
    url = f"https://api.controld.com/profiles/{profile_id}/groups/{folder_id}"
    headers = {"accept": "application/json", "authorization": api_key}
    api_request("DELETE", url, headers)

def create_rule_folder(name, do, status, profile_id, api_key):
    """Create a new rule folder."""
    url = f"https://api.controld.com/profiles/{profile_id}/groups"
    payload = {"name": name, "do": do, "status": status}
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key,
    }
    return api_request("POST", url, headers, payload)

def create_folder_rules(profile_id, api_key, do, status, group, hostnames):
    """Add rules to a rule folder."""
    url = f"https://api.controld.com/profiles/{profile_id}/rules"
    payload = {
        "do": do,
        "status": status,
        "group": group,
        "hostnames[]": hostnames,  # This assumes the API supports batch creation
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key,
    }
    api_request("POST", url, headers, payload)

def get_domains(url):
    """Retrieve domains from a given blocklist URL."""
    with requests.get(url) as response:
        response.raise_for_status()
        json_data = response.json()
    return [rule["PK"] for rule in json_data.get("rules", [])]

# Main script logic
if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding arguments
    parser.add_argument("-a", "--api_key", required=True, help="API Key for authorization")
    parser.add_argument("-p", "--profile_id", required=True, help="Profile ID")
    parser.add_argument("-g", "--group_name", required=True, help="Name of the rule group")
    parser.add_argument("-b", "--blocklist_url", required=True, help="URL of the blocklist")

    # Parse arguments
    args = parser.parse_args()

    api_key = args.api_key
    profile_id = args.profile_id
    group_name = args.group_name
    blocklist_url = args.blocklist_url

    # Fetch domains from the blocklist
    domains = get_domains(blocklist_url)

    # Fetch existing rule folders
    profiles = get_rule_folders(profile_id, api_key)

    # Delete existing folder with the same name
    group_id = None
    for group in profiles.get("body", {}).get("groups", []):
        if group.get("group") == group_name:
            group_id = group.get("PK")
            delete_rule_folder(profile_id, group_id, api_key)

    # Create a new folder
    folder_response = create_rule_folder(group_name, do=0, status=1, profile_id=profile_id, api_key=api_key)
    group_id = folder_response.get("PK")

    # Add rules to the folder in batches (if supported by API)
    create_folder_rules(profile_id, api_key, do=0, status=1, group=group_id, hostnames=domains)

    print(f"Successfully updated rule folder '{group_name}' with {len(domains)} domains.")
