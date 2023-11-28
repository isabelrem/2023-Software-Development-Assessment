"""
A script which takes the output of a request for a gene panel from
the PanelApp API as a large, complex dictionary and parses this
to extract the panel ID, name, GMS sign-off status, gene number,
associated R-codes, gene names, and genomic coordinates and stores
these within a new dictionary which is return.

This information is also printed to the screen.
"""

from VV_API_Request import VVRequest
from VV_Request_Parse import vv_request_parse

def panelapp_search_parse(input, genome_build):
    """Takes the OUTPUT of the pk_search method for the
    PanelAppRequest class in PanelApp_API_Request.py and parses it
    to extract the desired information."""
    
    OUTPUT = {} 
    # Create an empty dictionary - we will store the information
    # from the API output dictionary we wish to use in here.

    # Check genome build is valid:
    if genome_build == 'GRch37':
        print('GRch37 build selected.')
    elif genome_build == 'GRch38':
        print('GRch38 build selected.')
    else:
        raise ValueError('Invalid genome build')

    OUTPUT['Panel ID'] = input['id']
    OUTPUT['Panel Name'] = input['name']
    OUTPUT['Version'] = input['version']

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
    OUTPUT['R Codes'] = [x for x in input['relevant_disorders'] if
                         x.startswith('R') \
                         and x[1:].isdigit()]
    # Add all items in the input['relevant disorders] list which
    # start with R and are otherwise numbers to the dict in a list.


    # Extract the gene symbols, HGNC IDs, Ensembl IDs, and genomic coordinates:
    OUTPUT['Genes'] = []
    
    for gene_record in input['genes']:
        SYMBOL = gene_record['gene_data']['gene_symbol']
        HGNC_ID = gene_record['gene_data']['hgnc_id']
        LOC_INFO = list(gene_record['gene_data']['ensembl_genes'][genome_build].values())
        # Must extract like this as build version number is a dict key
        # and I want to get the information without having to specify
        # this.
                                                                   
        CHROM = LOC_INFO[0]['location'].split(':')[0]                                   
        COORDS = LOC_INFO[0]['location'].split(':')[-1]

        ENSEMBL_ID = LOC_INFO[0]['ensembl_id']
    
        OUTPUT['Genes'].append({HGNC_ID :  [SYMBOL, [CHROM, COORDS], ENSEMBL_ID]})
        
    # Get Mane_Select Transcripts for each gene:
    # Get the gene id's in a list:
    gene_list = []
    for gene_dict in OUTPUT['Genes']:
        gene_list += list(gene_dict.keys())
        
    # Put id's in query from for VV API:
    vv_genes_query = ''
    vv_genes_query += gene_list[0]
    if len(gene_list) > 1:
        for gene_id in gene_list[1:]:
            vv_genes_query += f'|{gene_id}'
    
    vv_genes_query = vv_genes_query.strip()
        
    print(f'HGNC list: {vv_genes_query}')

    # Perform a query to the VV API for that list:
    VV_REQ = VVRequest(genome_build)
    VV_RESP = VV_REQ.gene_to_transcripts(vv_genes_query, 'refseq')

    if VV_RESP.status_code == 200:
        OUTPUT = vv_request_parse(VV_RESP.json(), OUTPUT)


    ### Print the summary of the panel ###
    print(f"Panel ID: {OUTPUT['Panel ID']}")
    print(f"Panel Name: {OUTPUT['Panel Name']}")
    print(f"GMS Sign-off Status: {OUTPUT['GMS Signed-off']}")
    print(f"Associated NGTD R-codes: {', '.join(OUTPUT['R Codes'])}")
    print(f"Gene Number: {OUTPUT['Gene Number']}")

    print('Gene List:')
    print('HGNC_ID  Symbol  Coords  Ensembl_ID Mane_Select_Transcript')
    for gene in OUTPUT['Genes']:
        for k, v in gene.items():
            print(f"{k} {v[0]}  {v[1][0]}:{v[1][1]} {v[2]} {v[3]}")

    return OUTPUT