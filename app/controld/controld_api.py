from app.rest import api_request


def get_rule_folders(profile_id, api_key):
    url = f"https://api.controld.com/profiles/{profile_id}/groups"

    headers = {"accept": "application/json", "authorization": api_key}

    return api_request("GET", url, headers)


def delete_rule_folder(profile_id, folder_id, api_key):
    url = f"https://api.controld.com/profiles/{profile_id}/groups/{folder_id}"

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key,
    }

    api_request("DELETE", url, headers)


def create_rule_folder(name, do, status, profile_id, api_key):
    url = f"https://api.controld.com/profiles/{profile_id}/groups"

    payload = {"name": name, "do": do, "status": status}
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key,
    }

    api_request("POST", url, headers, payload)


def create_folder_rules(profile_id, api_key, do, status, group, hostnames) -> int:
    url = f"https://api.controld.com/profiles/{profile_id}/rules"

    payload = {"do": do, "status": status, "group": group, "hostnames[]": hostnames}
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key,
    }

    api_request("POST", url, headers, payload)
    return len(hostnames)
