"""
Connect to local MySQL server stored in a separate docker container 'panelsearch-database' 
and save API searches to database
"""
# Install packages
from sqlalchemy import *
from pymysql import *
import pandas as pd

#check to see whether docker SQL database container is running
# this logic works - put it in its own function? or into connect()

def docker_or_cloud():
    # docker database details
    username = 'root'
    password = 'password'
    database_name = 'panelsearch'
    database_host = 'panelsearch-database'
    connection_string = f'mysql+pymysql://{username}:{password}@{database_host}:3306/{database_name}'
    attempt = 0
    engine = None
    while (engine == None) and (attempt <= 10):
        try:
            engine = create_engine(connection_string)
            engine.close()
            print("yay!¬")
            return connection_string
        except:
            attempt += 1
            print("aa!")
            pass
    # google cloud database details
    username = 'panelsearch_user'
    password = 'panelsearch_password'
    database_name = 'panelsearch'
    database_host = '35.197.209.133'
    connection_string = f'mysql+pymysql://{username}:{password}@{database_host}:3306/{database_name}'
    
    return connection_string

print(docker_or_cloud())
"""
The main script to take a disease description or R code,
and the genome build version in the form of inputted strings
and use these to search PanelApp, via the PanelApp API, for a
corresponding gene panel. Return the information associated with
this panel.
"""

# Import packages
import json
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os
from select_disease import get_clinical_indications, find_match
from PanelApp_API_Request import PanelAppRequest
from PanelApp_Request_Parse import panelapp_search_parse
from API_to_SQL_cloud import PK_Parse_Data_to_SQL_cloud

# Set up logging to include file logging only
log_file = 'panel_search.log'
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=50000, backupCount=1)
    ]
)

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
            raise ValueError('Invalid option selected - exiting... Please try again.')

    def get_input_string_type(self):
        """ Asks the user whether they would like to input a R-code or disease description. """
        input_type = input('If you would like to search by R-code, enter 1. If you would like to enter a disease description, enter 2.\n')
        if input_type == '1':
            return 'R-code'
        elif input_type == '2':
            return 'disease_desc'
        else:
            raise ValueError('Invalid input type - exiting... Please try again.')

    def get_input_string(self):
        """ Asks the user for their search term and returns as a string. """
        input_string = input('Enter your search term: (e.g., R128 or pneumothorax)\n')
        return input_string

def create_bed_filename(panel_name, genome_build):
    """ Creates a filename for the BED file based on the panel name, genome build, and current date. """
    bed_files_dir = 'bed_files'
    if not os.path.exists(bed_files_dir):
        os.makedirs(bed_files_dir)  # Create the folder if it doesn't exist

    date_str = datetime.datetime.now().strftime("%Y%m%d")
    formatted_panel_name = panel_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    filename = f"{formatted_panel_name}_{genome_build}_{date_str}.bed"
    return os.path.join(bed_files_dir, filename)

def create_sql_record(panel_name, genome_build, pid):
    """ Creates a SQL record. """
    print(panel_name)
    print(genome_build)
    PK_Parse_Data_to_SQL_cloud(pid, genome_build, PK = panel_name)

def main():
    """
    Use functions create above and in the other files to run PanelSearch
    :return: PanelApp API information and BED file and allow user to store data
    """
    SEARCH = PanelSearch()
    REQUEST = PanelAppRequest()
    RESPONSE = None

    logging.info("Starting PanelSearch with input type: %s", SEARCH.input_type)

    if SEARCH.input_type == 'R-code':
        RESPONSE = REQUEST.r_search(SEARCH.input)
    elif SEARCH.input_type == 'disease_desc':
        clinical_indications = get_clinical_indications()
        disease_desc = find_match(SEARCH.input, clinical_indications)
        RESPONSE = REQUEST.pk_search(disease_desc)

    if RESPONSE:
        if str(RESPONSE.status_code).startswith('50'):
            logging.error('Server-side issue occurred with status code: %s', RESPONSE.status_code)
            print('A server-side issue occurred.\nPlease try again later.')
            exit()

        elif RESPONSE.status_code == 404:
            logging.warning('Requested panel not found with status code: %s', RESPONSE.status_code)
            print('The requested panel could not be found.\nPlease review your search term and try again')
            exit()

        if RESPONSE.status_code == 200:
            panel_data = panelapp_search_parse(RESPONSE.json(), SEARCH.genome_build)
            logging.info("Panel data processed successfully")

            generate_bed = input("Generate BED file? (Y/N) \n")
            if generate_bed.lower() == 'y':
                panel_data_str = json.dumps(panel_data)
                panel_name = panel_data.get("Panel Name", "UnknownPanel")
                
                filename = create_bed_filename(panel_name,SEARCH.genome_build)
                subprocess.call(["python", "PanelSearch/generate_bed.py", panel_data_str, filename, SEARCH.genome_build])

                logging.info("BED file generation initiated")

            save_search = input("Would you like to save this search against a patient ID? (Y/N) \n")
            if save_search.lower() == 'y':
                panel_data_str = json.dumps(panel_data)
                panel_name = panel_data.get("Panel Name", "UnknownPanel")
                pid = input("What patient ID would you like to save this search against? \n")
                create_sql_record(panel_name, SEARCH.genome_build, pid)
                print("Your search was saved")
            else:
                print("Your search was not saved")

    print("Thank you for using PanelSearch. Goodbye.")

if __name__ == '__main__':
    main()
