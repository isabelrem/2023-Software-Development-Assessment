"""
This script allows the user to search for
genetic diseases in the GMS approved group of PanelApp panels
and returns the disease for the /panels/{panel_pk}/genes API endpoint.
"""
# Import python libraries
import requests

panel_url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/"


# Function to get all signed off panels
def get_clinical_indications(url):
    """
    Gets GMS approved panels as a JSON file from the API link
    :return: list of panels and associated metadata
    """
    panels = []  # Create empty list for panel details
    next_url = url  # PanelApp base API URL for getting all panels
    print("Please wait. Fetching data.")  # Takes a while to get panel data so notify user

    try:
        while next_url:
            response = requests.get(next_url)
            response.raise_for_status()  # This will raise an error if the request fails
            data = response.json()
            next_url = data['next']  # URL for the next page of results

            for panel in data['results']:
                # Check if the panel has "GMS signed-off" type
                if any(t['slug'] == 'gms-signed-off' for t in panel['types']):
                    panels.append(panel)

        if len(panels) == 0:
            raise KeyError
        else:
            # Create empty list of disease names
            clinical_indications = []

            # Get list of disease names
            for j in range(len(panels)):
                add_disease = panels[j]['name']  # Get disease name from JSON of panel data
                clinical_indications.append(add_disease.lower())  # Add disease name to list in lowercase

            return clinical_indications

    except (KeyError, requests.exceptions.MissingSchema, ConnectionError):
        print("Sorry list of diseases could not be generated from the API. Please contact the authors.")
        return False


# Search for disease in list
def find_match(element, lst):
    """
    Searches for disease in clinical indications list and returns
    matches. User is asked to pick genetic disease for API.
    :param element: disease that user has inputted
    :param lst: list of clinical indications from Test Directory
    :return: matches in clinical indications list
    """
    try:
        tracker = []  # List of matching clinical indications
        element_search = element.lower()

        for i in range(len(lst)):
            if element_search in lst[i]:
                print(lst[i])
                tracker.append(lst[i])

        if len(tracker) == 0:
            raise ValueError

        option = input("Please choose an option from above: ")
        if option in tracker:
            print("You have chosen {}".format(option))
            return option
        else:
            raise ValueError

    except ValueError:
        print("Sorry no matches found. Please try again.")
        return False


if __name__ == '__main__':
    disease = input("Please enter keyword(s) for your genetic disease: ")  # Ask user for disease
    list_clinical_indications = get_clinical_indications(panel_url)
    find_match(disease, list_clinical_indications)  # Run function to search for disease in clinical indications list
