import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get_all_cloudflare_zones(api_key):
    endpoint = "https://api.cloudflare.com/client/v4/zones"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    zones = []
    page = 1

    while True:
        params = {"page": page, "per_page": 50}  # Adjust per_page as needed
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            result_info = data.get("result_info", {})
            zones.extend(data.get("result", []))

            if "page" in result_info and result_info["page"] >= result_info.get("total_pages", 1):
                break  # Reached the last page, exit the loop
            else:
                page += 1
        else:
            print(f"Error fetching zones: {response.status_code}")
            print(response.text)
            return None

    return zones

def get_cloudflare_a_records(api_key, zone_id):
    endpoint = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
        a_records = set(record["name"] for record in data["result"] if record["type"] == "A" and "*" not in record["name"])
        return list(a_records)
    else:
        print(f"Error fetching A records for zone {zone_id}: {response.status_code}")
        print(response.text)
        return None

def send_to_splunk(zone_name, a_records):
    splunk_url = "https://172.18.0.2:8088/services/collector/event"   
    headers = {"Authorization": "Splunk <hec>"}
    data = {"zone": zone_name, "subdomains": a_records if a_records else []}
    payload = {"event": json.dumps(data), "index": "cloudflare_domains"}  # Specify the index
    response = requests.post(splunk_url, headers=headers, json=payload, verify=False)

# Replace this with your actual Cloudflare API key
api_key = ""

# Get all zones
zones = get_all_cloudflare_zones(api_key)

#TODO CLEAN UP
if zones:
    total_subdomains = 0

    print("Fetching A Records for each zone:")
    for zone in zones:
        zone_id = zone["id"]
        zone_name = zone["name"]
        print(f"\nZone: {zone_name} (ID: {zone_id})")
        
        # Get A records for the current zone
        a_records = get_cloudflare_a_records(api_key, zone_id)
        send_to_splunk(zone_name, a_records)

        if a_records:
            total_subdomains += len(a_records)
            print("A Records (IPv4 addresses):")
            for a_record in a_records:
                print(a_record)


    print(f"\nTotal Subdomains Found: {total_subdomains}")
