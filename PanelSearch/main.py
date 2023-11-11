"""
The main script to take a disease description or R code,
and the genome build version in the form of inputted strings
and use these to search PanelApp, via the PanelApp API, for a
corresponding gene panel. Return the information associated with
this panel.
"""
import json
import subprocess
from Description_Select import get_clinical_indications, find_match

from PanelApp_API_Request import PanelAppRequest
from PanelApp_Request_Parse import search_parse
from utils.get_gene_names import gene_names


class PanelSearch:
    """ A class for gathering the search information from the user on the commandline. """
    def __init__(self):
        self.input_type = self.get_input_string_type()
        self.input = self.get_input_string()
        self.genome_build = self.get_genome_build()

    def get_genome_build(self):
        """ Asks the user which genome build they would like genomic coordinates returned for. """
        genome_build_choice = input('Which genome build would you like to use? Enter 1 for GRch37. Enter 2 for GRch38.\n')
        if genome_build_choice == '1':
            return 'GRch37'
        elif genome_build_choice == '2':
            return 'GRch38'
        else:
            print('Invalid option selected - exiting... Please try again.')
            exit()

    def get_input_string_type(self):
        """ Asks the user whether the would like to input a R-code or disease description. """
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
        input_string = input('Enter your search term:\n')
        return input_string
    
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
 
    if RESPONSE:
        # Parse the response
        panel_data = search_parse(RESPONSE.json(), SEARCH.genome_build)
        
        # Print panel data
        print(panel_data)
        
        # Ask to generate BED
        generate_bed = input("Generate BED file? (y/n): ")
        
        if generate_bed.lower() == 'y':
            # Convert panel data to string format for command line argument
            panel_data_str = json.dumps(panel_data)
            # Call script
            subprocess.call(["python", "generate_bed.py", panel_data_str])

        # Get gene names for SQL database storage
        genes = gene_names(panel_data)
        print(genes)
