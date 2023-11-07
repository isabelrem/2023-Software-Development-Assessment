# Import necessary modules:
import urllib.parse
import requests
import sys

# Import local modules:
import PanelApp_Request_Parse

class PanelAppRequest:
    # Class for searching PanelApp using different modules.

    def __init__(self):
        # Initiates a class for requesting data from the PanelApp API.
        self.base_url = 'https://panelapp.genomicsengland.co.uk/api/v1'
        self.url = ''

    def request_data(self,
                     prms = None):
        # Make a request to the PanelApp API using requests.get with the given parameters.
        return requests.get(self.url,
                            params = prms)
    
    def pk_search(self,
                  disease_desc):
        # Requests a gene list for a panel from the PanelApp API using the disease description (PK).
        url_disease_desc = urllib.parse.quote(disease_desc)
        self.url = f'{self.base_url}/panels/{url_disease_desc}/?format=json'
        return self.request_data()
    
if __name__ == '__main__':
    RQ = PanelAppRequest()

    ### For testing purposes ###
    PK = 'Fetal anomalies with a likely genetic cause'
    response = RQ.pk_search(PK)

    print(f"Status Code: {response.status_code}")

    PanelApp_Request_Parse.pk_search_parse(response.json(), 'GRch37')
    




