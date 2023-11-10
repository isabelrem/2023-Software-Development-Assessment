import requests
import json
import argparse
from deepdiff import DeepDiff  # You will need to install this package

# PanelApp base API URL for getting all panels
PANEL_APP_URL = "https://panelapp.genomicsengland.co.uk/api/v1/panels/"

# Function to get all signed off panels
def get_signed_off_panels():
    panels = []
    next_url = PANEL_APP_URL

    while next_url:
        response = requests.get(next_url)
        response.raise_for_status()  # This will raise an error if the request fails
        data = response.json()
        next_url = data['next']  # URL for the next page of results

        for panel in data['results']:
            # Check if the panel has "GMS signed-off" type
            if any(t['slug'] == 'gms-signed-off' for t in panel['types']):
                panels.append(panel)

    return panels

# Save the signed off panels to a JSON file
def save_panels_to_json(panels, filename='signed_off_panels.json'):
    with open(filename, 'w') as file:
        json.dump(panels, file, indent=4)

def compare_panels_with_local_file(panels, filename):
    try:
        with open(filename, 'r') as file:
            local_panels = json.load(file)
    except FileNotFoundError:
        print(f"The file {filename} does not exist. Please run the script without the -c option to fetch and save the data first.")
        return

    # Convert both lists (local and fetched) to dictionaries keyed by panel ID
    local_panels_dict = {panel['id']: panel for panel in local_panels}
    fetched_panels_dict = {panel['id']: panel for panel in panels}

    # Compare the two dictionaries
    differences = []
    for panel_id, fetched_panel in fetched_panels_dict.items():
        local_panel = local_panels_dict.get(panel_id)
        if not local_panel:
            differences.append(f"Panel with ID {panel_id} is new.")
            continue

        # Compare significant fields
        for key in fetched_panel:
            if key not in ['version', 'version_created']:  # Skip non-significant fields
                if fetched_panel[key] != local_panel.get(key):
                    differences.append(f"Value of panel ID {panel_id}['{key}'] changed from {local_panel.get(key)} to {fetched_panel[key]}.")

    if differences:
        print("The local JSON file is not up-to-date with the API. Differences found:")
        for difference in differences:
            print(difference)
    else:
        print("The local JSON file is up-to-date with the API.")


def main():
    parser = argparse.ArgumentParser(description="Fetch and compare signed-off panels from PanelApp API.")
    parser.add_argument("-c", "--compare", help="Compare fetched data with the local JSON file.", action="store_true")
    args = parser.parse_args()

    filename = 'signed_off_panels.json'
    signed_off_panels = get_signed_off_panels()

    if args.compare:
        compare_panels_with_local_file(signed_off_panels, filename)
    else:
        save_panels_to_json(signed_off_panels, filename)
        print(f"Saved {len(signed_off_panels)} signed-off panels to JSON file.")

if __name__ == "__main__":
    main()