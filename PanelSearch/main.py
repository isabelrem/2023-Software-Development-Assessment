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
from SQL_Cloud_Functions import browse_cloud_records, download_records

# Set up logging to include both file and console logging
log_file = 'panel_search.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10000, backupCount=1),
        logging.StreamHandler()
    ]
)

class PanelSearch:
    """ A class for gathering the search information from the user on the commandline. """
    def __init__(self):
        self.search_type = self.existing_or_new()
        if self.search_type == 'search_new':
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

    def existing_or_new(self):
        """ Asks the user whether they would like to get new panel information, or browse through existing records. """
        existing_or_new_choice = input('Enter 1 to search for new panel information. Enter 2 to browse existing PanelSearch records.')
        if existing_or_new_choice == '1':
            return 'search_new'
        elif existing_or_new_choice == '2':
            return 'search_existing'
        else:
            raise ValueError('Invalid input type - exiting... Please try again,.')

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


def create_sql_record(panel_name,genome_build,pid):
    """ Allows the user to save their PanelApp search in a SQL database """
    print(panel_name)
    print(genome_build)
    PK_Parse_Data_to_SQL_cloud(pid,genome_build,PK = panel_name)




# Run the app
def main():
    """
    Use functions create above and in the other files to run PanelSearch
    :return: PanelApp API information and BED file and allow user to store data
    """
    SEARCH = PanelSearch()
    REQUEST = PanelAppRequest()
    RESPONSE = None  

    if SEARCH.existing_or_new == 'search_new':

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
                print(panel_data)
                logging.info("Panel data processed successfully")

                generate_bed = input("Generate BED file? (y/n)")
                if generate_bed.lower() == 'y':
                    panel_data_str = json.dumps(panel_data)
                    panel_name = panel_data.get("Panel Name", "UnknownPanel")
                    filename = create_bed_filename(panel_name, SEARCH.genome_build)
                    subprocess.call(["python", "generate_bed.py", panel_data_str, filename])
                    logging.info("BED file generation initiated")

                # Ask to save search into SQL DB
                save_search = input("Would you like to save this search against a patient ID? (y/n) \n")
                if save_search.lower() == 'y':
                    #json_filename = filename.replace("bed","json") # implement with json later

                    panel_data_str = json.dumps(panel_data)
                    panel_name = panel_data.get("Panel Name", "UnknownPanel")
                    pid = input("What patient ID would you like to save this search against? \n")
                    create_sql_record(panel_name,SEARCH.genome_build, pid)
                    print("Your search was saved")
                else:
                    print("Your search was not saved")



                    # also, logging?            

    else:
        # the user has selected to browse existing records saved in the SQL database
        pid = input("Please enter the patient ID here. If you wish to see all saved records, press Return : ")
        result = browse_cloud_records(patient_id=pid)

        if result != "This patient ID does not exist in the SQL database":
            try:
                patients_df = result[0]
                searches_df = result[1]
            except:
                patients_df = result
                searches_df = ''
                         
            save_choice = input("Would you like to save these tables locally? (y/n)")
            if save_choice.lower() == "y":
                file_name_choice = input("Please enter your desired filename: ")
                download_records(patients_df,searches_df,file_name_choice)
                # download_records(patients_dataframe,searches_dataframe,file_name = '') # these are the parameters - what if no searches table?
    
    # Thank user and say goodbye
    print("Thank you for using PanelSearch. Goodbye.")

if __name__ == '__main__':
    main()

