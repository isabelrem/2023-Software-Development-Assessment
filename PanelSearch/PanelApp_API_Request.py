# Import necessary modules:
import urllib.parse
import requests

# Create a class for requesting from the PanelApp API:
class PanelAppRequest:
    # 

    def __init__(self):
        # Initiates a class for requesting data from the PanelApp API.
        self.base_url = 'https://panelapp.genomicsengland.co.uk/api/v1'

    def request_data(self, prms = None):
        # Make a request to the PanelApp API using requests.get with the given parameters.
        return requests.get(self.url, params = prms)
    
    def PK_search(self, disease_desc):
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
    rq = PanelAppRequest()

    ### For testing purposes ###
    pk = 'Fetal anomalies with a likely genetic cause'
    response = rq.PK_search(pk)
    print(response.status_code)
    print(response.json())

    ### For testing purposes ###
    R_code = 'R140'
    response_R = rq.R_search(R_code)
    print(response_R.status_code)
    print(response_R.json())

    rq.R_search("140")




