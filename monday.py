import sys
import json
import requests

def send_to_monday_com(data):
    apiKey = ""  # Replace with your Monday.com API key
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}

    # Extract relevant information
    zone = data.get("result", {}).get("zone", "")
    subdomains = data.get("result", {}).get("subdomains{}", "").split(',')

    # Format the data as a string
    monday_data = f'New Domain Detected'

    # Escape double quotes within subdomains
    subdomains_escaped = [sub.replace('"', '\\"') for sub in subdomains]

    # Send data to Monday.com
    query = f'mutation ($myItemName: String!) {{ create_item (board_id:<>, item_name:$myItemName, column_values: "{{\\"long_text\\":\\"{zone}\\", \\"long_text8\\":\\"{", ".join(subdomains_escaped)}\\"}}") {{ id }} }}'
    variables = {'myItemName': monday_data}
    monday_request_data = {'query': query, 'variables': variables}

    try:
        response = requests.post(url=apiUrl, json=monday_request_data, headers=headers)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Monday.com: {e}")
        sys.exit(1)

#TODO CLEAN UP CODE AND REMOVE IF STATEMENT
if __name__ == "__main__":
    # Check for --execute argument
    if 1 == 1:
        # Read data from stdin
        try:
            alert_data = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from stdin: {e}")
            sys.exit(1)

        # Log both command-line arguments and data to file
        # Assuming you have a log_to_file function defined somewhere
        # log_to_file(alert_data)

        # Send data to Monday.com
        send_to_monday_com(alert_data)
    else:
        print("This script should be executed as part of a Splunk alert.")
        sys.exit(1)
