import argparse

from app.controld.controld_api import (
    get_rule_folders,
    delete_rule_folder,
    create_folder_rules,
    create_rule_folder,
)
from app.controld.controld_helpers import paginate
from app.hagezi.hagezi_api import get_do, get_domains

# Main script logic
if __name__ == '__main__':
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
    folder_do = get_do(blocklist_url)

    # delete old folder
    profiles = get_rule_folders(profile_id, api_key)
    for group in profiles["body"]["groups"]:
        if group["group"] == group_name:
            group_id = group["PK"]
            delete_rule_folder(profile_id, group_id, api_key)

    # create new folder
    create_rule_folder(group_name, folder_do, 1, profile_id, api_key)

    # load domains
    profiles = get_rule_folders(profile_id, api_key)
    for group in profiles["body"]["groups"]:
        if group["group"] == group_name:
            group_id = group["PK"]

    # break into pages and create rules
    page_size = 500  # page size
    page_number = 1  # init page

    while paginate(domains, page_size, page_number) != []:
        count = create_folder_rules(
            profile_id, api_key, 0, 1, group_id, paginate(domains, page_size, page_number)
        )
        page_number += 1

    print(f"Successfully updated rule folder '{group_name}' with {count} domains.")
