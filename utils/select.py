"""
This script allows the user to search for
genetic diseases in the National Test Directory
and returns the disease in a format that is suitable
for the /panels/{panel_pk}/genes API endpoint.
"""

# Import python modules
import pandas as pd

# URL for National Genomic Test Directory
url = "https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test\
-directory-version-5.1.xlsx"

# Read National Test Directory as dataframe
data = pd.read_excel(url, sheet_name="R&ID indications", header=1)
dataFrame = pd.DataFrame(data)

# Create dictionary of diseases from National Test Directory v5.1
clinical_indications = set(dataFrame["Clinical Indication"])  # set so no duplicates
clinical_indications = list(clinical_indications)  # convert set to list

# Ask user for disease
disease = input("Please enter disease name: ")


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

        for i in range(len(lst)):
            if element in lst[i]:
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


# Run function to search for disease in clinical indications list
find_match(disease, clinical_indications)
