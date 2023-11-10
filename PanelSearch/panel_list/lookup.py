#!/usr/bin/env python3
import argparse
import subprocess
import json

# Assuming the JSON data file is named 'panels.json' in the current directory
# Replace 'panels.json' with the path to your actual JSON data file
JSON_FILE = 'signed_off_panels.json'

def lookup_panel(panel_id=None, condition_name=None):
    try:
        jq_filter = '['  # Start the filter to create a JSON array
        jq_filter += '.[]'
        if panel_id:
            jq_filter += f' | select(.relevant_disorders[] == "{panel_id}")'
        elif condition_name:
            jq_filter += f' | select(.name | ascii_downcase | contains("{condition_name.lower()}"))'
        jq_filter += ']'  # End the filter to close the JSON array
        
        # Use jq to filter the JSON data
        result = subprocess.run(
            ['jq', jq_filter, JSON_FILE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # Use this for compatibility with Python < 3.7
        )
        
        # Check if the command was successful
        if result.returncode == 0 and result.stdout:
            # Parse JSON output from jq and print
            panel_data = json.loads(result.stdout)
            print(json.dumps(panel_data, indent=2))
        else:
            print(f"No panel found with identifier: {panel_id or condition_name}")
    
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON output from jq")
    except FileNotFoundError:
        print(f"Error: JSON file {JSON_FILE} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Lookup a panel by its identifier or name using jq.')
    parser.add_argument('-p', '--panel', help='The panel identifier to lookup.')
    parser.add_argument('-c', '--condition', help='The condition name to search for in panel names.')
    args = parser.parse_args()

    if args.panel:
        lookup_panel(panel_id=args.panel)
    elif args.condition:
        lookup_panel(condition_name=args.condition)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
