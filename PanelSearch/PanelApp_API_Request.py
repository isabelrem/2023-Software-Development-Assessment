# Import necessary modules:
import urllib.parse
import requests
import sys

# Import local modules:
import PanelApp_Request_Parse

class PanelAppRequest():
    # Class for searching PanelApp using different modules.

    def __init__(self):
        # Initiates a class for requesting data from the PanelApp API.
        self.base_url = 'https://panelapp.genomicsengland.co.uk/api/v1'
        self.url = ''
        self.input_type = None
        self.input = None

    def request_data(self,
                     prms = None):
        # Make a request to the PanelApp API using requests.get with the given parameters.
        return requests.get(self.url,
                            params = prms)
    
    def pk_search(self,
                  disease_desc):
        # Requests a gene list for a panel from the PanelApp API using the disease description (PK).
        
        # Cleans string - replaces characters not allowed in URL
        url_disease_desc = urllib.parse.quote(disease_desc) 
        
        # Combines base URL and user input to search API for specific panel
        self.url = f'{self.base_url}/panels/{url_disease_desc}/genes'
        
        return self.request_data()

    def R_search(self, R_code):
        # Requests a gene list for a panel from the PanelApp API using the test directory Rcode.
        
        # Combines base URL and user input to search API for specific panel
        self.url = f'{self.base_url}/panels/{R_code}/'
        
        response = self.request_data()

        if response.status_code == 404:
            print("A Panel could not be found under this R-code. Please check your R-code and try again.")

        return self.request_data()

    
if __name__ == '__main__':
    RQ = PanelAppRequest()



    ### For testing purposes ###
    PK = 'Fetal anomalies with a likely genetic cause'
    response = RQ.pk_search(PK)

    print(f"Status Code: {response.status_code}")

    # PanelApp_Request_Parse.pk_search_parse(response.json(), 'GRch37')

    ### For testing purposes ###
    R_code = 'R140'
    response_R = RQ.R_search(R_code)

    PanelApp_Request_Parse.search_parse(response_R.json(), 'GRch37')




