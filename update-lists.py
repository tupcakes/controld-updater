import urllib.request, json, requests, argparse


def get_rule_folders(profile_id, api_key):
    url = "https://api.controld.com/profiles/" + profile_id + "/groups"

    headers = {
        "accept": "application/json",
        "authorization": api_key
    }

    response = requests.get(url, headers=headers)

    json_object = json.loads(response.text)
    return json_object

def get_domains(url):
    with urllib.request.urlopen(url) as url:
        json_data = json.load(url)

    domains = []
    for i in range(len(json_data["rules"])):
        domains.append(json_data["rules"][i]["PK"])
    return domains

def delete_rule_folder(profile_id, folder_id, api_key):
    import requests

    url = "https://api.controld.com/profiles/" + profile_id + "/groups/" + str(folder_id)

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": api_key
    }

    response = requests.delete(url, headers=headers)

    print(response.text)

def create_rule_folder(name, do, status, profile_id, api_key):
    url = "https://api.controld.com/profiles/" + profile_id + "/groups"

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

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)

def create_folder_rules(profile_id, api_key, do, status, group, hostnames):
    url = "https://api.controld.com/profiles/" + profile_id + "/rules"

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

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument('-a', '--api_key')
parser.add_argument('-p', '--profile_id')
parser.add_argument('-g', '--group_name')
parser.add_argument('-b', '--blocklist_url')

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

for domain in domains:
    create_folder_rules(profile_id, api_key, 0, 1, group_id, domain)
