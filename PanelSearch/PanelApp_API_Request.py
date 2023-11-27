"""
A class containing functions for requesting data from the PanelApp
API on gene panels matching the given search terms - this can either
be an R code (e.g., R128) or a clinical description matching
a panel clinical indication.
"""

# Import necessary modules:
import urllib.parse
import requests

# Import local modules:
from PanelSearch.PanelApp_Request_Parse import *


class PanelAppRequest():
    """ Class for searching PanelApp using different modules."""

    def __init__(self):
        """Initiates a class for requesting data from the PanelApp API."""
        self.base_url = 'https://panelapp.genomicsengland.co.uk/api/v1'
        self.url = ''
        self.input_type = None
        self.input = None

    def request_data(self,
                     prms = None):
        """Make a request to the PanelApp API using requests.get with the given parameters."""
        return requests.get(self.url,
                            params = prms)
    
    def pk_search(self,
                  disease_desc):
        """Requests a gene list for a panel from the PanelApp API using the disease description (PK)."""
        
        # Cleans string - replaces characters not allowed in URL
        url_disease_desc = urllib.parse.quote(disease_desc) 
        
        # Combines base URL and user input to search API for specific panel
        self.url = f'{self.base_url}/panels/{url_disease_desc}/'
        
        return self.request_data()

    def r_search(self, r_code):
        """Requests a gene list for a panel from the PanelApp API using the test directory Rcode."""
        
        # Combines base URL and user input to search API for specific panel
        self.url = f'{self.base_url}/panels/{r_code}/'

        if self.request_data().status_code == 404:
            raise ValueError("A Panel could not be found under this R-code. Please check your R-code and try again.")

        return self.request_data()

    
if __name__ == '__main__':
    RQ = PanelAppRequest()



    ### For testing purposes ###
    PK = 'Fetal anomalies with a likely genetic cause'
    response = RQ.pk_search(PK)

    print(f"Status Code: {response.status_code}")

    #PanelApp_Request_Parse.pk_search_parse(response.json(), 'GRch37')