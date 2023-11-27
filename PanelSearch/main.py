"""
The main script to take a disease description or R code,
and the genome build version in the form of inputted strings
and use these to search PanelApp, via the PanelApp API, for a
corresponding gene panel. Return the information associated with
this panel.
"""
import json
import subprocess
import datetime
import os
from Description_Select import get_clinical_indications, find_match
from PanelApp_API_Request import PanelAppRequest
from PanelApp_Request_Parse import panelapp_search_parse

class PanelSearch:
    """ A class for gathering the search information from the user on the commandline. """
    def __init__(self):
        self.input_type = self.get_input_string_type()
        self.input = self.get_input_string()
        self.genome_build = self.get_genome_build()

    def get_genome_build(self):
        """ Asks the user which genome build they would like genomic coordinates returned for. """
        genome_build_choice = input('Which genome build would you like to use? Enter 1 for GRCh37. Enter 2 for GRCh38.\n')
        if genome_build_choice == '1':
            return 'GRch37'
        elif genome_build_choice == '2':
            return 'GRch38'
        else:
            print('Invalid option selected - exiting... Please try again.')
            exit()

    def get_input_string_type(self):
        """ Asks the user whether they would like to input a R-code or disease description. """
        input_type = input('If you would like to search by R-code, enter 1. If you would like to enter a disease description, enter 2.\n')
        if input_type == '1':
            return 'R-code'
        elif input_type == '2':
            return 'disease_desc'
        else:
            print('Invalid input type - exiting... Please try again.')
            exit()
    
    def get_input_string(self):
        """ Asks the user for their search term and returns as a string. """
        input_string = input('Enter your search term: (e.g., R128 or pneumothorax)\n')
        return input_string

# Define the create_bed_filename function here
def create_bed_filename(panel_name, genome_build):
    """ Creates a filename for the BED file based on the panel name, genome build, and current date. """
    bed_files_dir = 'bed_files'
    if not os.path.exists(bed_files_dir):
        os.makedirs(bed_files_dir)  # Create the folder if it doesn't exist

    date_str = datetime.datetime.now().strftime("%Y%m%d")
    formatted_panel_name = panel_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    filename = f"{formatted_panel_name}_{genome_build}_{date_str}.bed"
    return os.path.join(bed_files_dir, filename)
    
if __name__ == '__main__':
    SEARCH = PanelSearch()
    REQUEST = PanelAppRequest()
    RESPONSE = None

    if SEARCH.input_type == 'R-code':
        RESPONSE = REQUEST.R_search(SEARCH.input)
    elif SEARCH.input_type == 'disease_desc':
        CLIN_INDS = get_clinical_indications()
        DISEASE_DESC = find_match(SEARCH.input, CLIN_INDS)
        RESPONSE = REQUEST.pk_search(DISEASE_DESC)

    # Error Handling for response:
    if str(RESPONSE.status_code).startswith('50'):
        print('A server-side issue occurred.\nPlease try again later.')
        exit()
    
    elif RESPONSE.status_code == 404:
        print('The requested panel could not be found.\nPlease review your search term and try again')
        exit()
    
    if RESPONSE.status_code == 200:
        panelapp_search_parse(RESPONSE.json(), SEARCH.genome_build)

    ### Bed File Creation ###
    if RESPONSE:
        # Parse the response
        panel_data = panelapp_search_parse(RESPONSE.json(), SEARCH.genome_build)
        
        # Print panel data
        print(panel_data)
        
        # Ask to generate BED
        generate_bed = input("Generate BED file? (y/n)")

        if generate_bed.lower() == 'y':
           panel_data_str = json.dumps(panel_data)
           panel_name = panel_data.get("Panel Name", "UnknownPanel")
           # Generate the filename for the BED file (also used for the corresponding JSON file)
           filename = create_bed_filename(panel_name, SEARCH.genome_build)
           # Call generate_bed.py to create BED and JSON files
           subprocess.call(["python", "generate_bed.py", panel_data_str, filename])
           print(f"BED and JSON files will be generated as {filename} and its JSON equivalent.")
