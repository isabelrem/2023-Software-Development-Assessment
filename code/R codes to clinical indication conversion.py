import pandas as pd
import xlrd
# pip install openpyxl --upgrade

def import_directory():
    url = "https://www.england.nhs.uk/wp-content/uploads/2018/08/Rare-and-inherited-disease-national-genomic-test-directory-version-5.1.xlsx"

    # import second sheet of genomics test directory - first contains version information, second contains info
    data = pd.read_excel(url, sheet_name = 1)
    
    # set first row as header
    data.columns = data.iloc[0]
    

    # get rid of the first row which contains the text which are now the headers
    data = data.iloc[1:]
    data.reset_index(drop=True, inplace = True)

    return data



def Rcode_to_Clin_Imp(Rcode):

    # import directory data
    data = import_directory()

    # cleaning the input:

    # remove any dashes
    Rcode = Rcode.replace('-','')

    # Add R prefix to code
    if not Rcode.startswith("R"):
        Rcode = "R" + Rcode
        
    
    CI = data.loc[data['Clinical indication ID'] == Rcode, 'Clinical Indication'].iloc[0]
    
    
    
    print(CI)


    # should add errors excepts here too

    return CI


Rcode_to_Clin_Imp(input("Please enter the Rcode"))    




