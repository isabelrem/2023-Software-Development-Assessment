"""
A script which takes the output of a request for a gene panel from
the PanelApp API has a large, complex dictionary and parses this
to extract the panel ID, name, GMS sign-off status, gene number,
associated R-codes, gene names, and genomic coordinates and stores
these within a new dictionary which is return.

This information is also printed to the screen.
"""

def pk_search_parse(input, genome_build):
    # Takes the OUTPUT of the pk_search method for the PanelAppRequest class in PanelApp_API_Request.py and parses it to extract the desired information.
    
    OUTPUT = {} # Create an empty dictionary - we will store the information from the API output dictionary we wish to use in here.

    # Check genome build is valid:
    if genome_build == 'GRch37':
        print('GRch37 build selected.')
    elif genome_build == 'GRch38':
        print('GRch38 build selected.')
    else:
        print('Invalid genome build given - must be GRch37 or GRch38')
        exit()

    # Extract panel ID and name:
    OUTPUT['Panel ID'] = input['id']
    OUTPUT['Panel Name'] = input['name']

    # Extract whether the panel is GMS signed-off:
    SIGNED_OFF = ''

    for TYPE_DICT in input['types']:
        if TYPE_DICT['name'] == 'GMS signed-off':
            SIGNED_OFF = 'Y'

    if SIGNED_OFF:
        OUTPUT['GMS Signed-off'] = 'Signed Off'
    else:
        OUTPUT['GMS Signed-off'] = 'Not Signed Off'

    # Extract the number of genes on the panel:
    OUTPUT['Gene Number'] = input['stats']['number_of_genes']

    # Extract the associated NGTD R Codes:
    OUTPUT['R Codes'] = [x for x in input['relevant_disorders'] if # Add all items in the input['relevant disorders] list which start with R and are otherwise numbers to the dict in a list.
                         x.startswith('R') \
                         and x[1:].isdigit()]
    
    # Extract the gene symbols and their genomic coordinates:
    OUTPUT['Genes'] = []
    
    for gene_record in input['genes']:
        SYMBOL = gene_record['gene_data']['gene_symbol']
        LOC_INFO = list(gene_record['gene_data']['ensembl_genes'][genome_build].values()) # Must extract like this as build version number is a dict key
                                                                                          # and I want to get the information without having to specify
        CHROM = LOC_INFO[0]['location'].split(':')[0]                                     # this.
        COORDS = LOC_INFO[0]['location'].split(':')[-1]
    
        OUTPUT['Genes'].append({SYMBOL : [CHROM, COORDS]})

    ### Print the summary of the panel ###
    print(f"Panel ID: {OUTPUT['Panel ID']}")
    print(f"Panel Name: {OUTPUT['Panel Name']}")
    print(f"GMS Sign-off Status: {OUTPUT['GMS Signed-off']}")
    print(f"Associated NGTD R-codes: {', '.join(OUTPUT['R Codes'])}")
    print(f"Gene Number: {OUTPUT['Gene Number']}")

    print('Gene List:')
    for gene in OUTPUT['Genes']:
        for k, v in gene.items():
            print(f"{k} - {v[0]}:{v[1]}")
    
    return OUTPUT