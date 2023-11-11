"""
From the API output get a list of gene names to put into the SQL database
"""


# Parse API output and retrieve gene names
def gene_names(input_list):
    """
    Loops through API output and returns list of gene names
    :param input_list: API output
    :return: list of gene names
    """
    try:
        # Create empty list
        list_of_genes = []

        # Loop through API output
        for i in range(len(input_list)):
            new = list(input_list['Genes'][i].values())[0][0]
            list_of_genes.append(new)

        # Check list is not empty
        if len(list_of_genes) == 0:
            raise KeyError
        else:
            return list_of_genes

    except KeyError:
        print("No genes found in panel. Please contact authors.")
