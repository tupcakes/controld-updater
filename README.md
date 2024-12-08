## Usage
```
podman run controld-updater \
    -a "api.abcd..." \
    -p "2342342kjhkj" \
    -g "Referral" \
    -b "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/controld/referral-allow-folder.json"
```

I personally use the json lists from https://github.com/hagezi/dns-blocklists/tree/main/controld. In particular the below lists.
- badware-hoster-folder.json
- referral-allow-folder.json
