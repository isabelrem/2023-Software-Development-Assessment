"""
A function which parses the json format object returned by the
VV API and extracts the mane_select transcript from it. Adds this
to the input dictionary.
"""

def vv_request_parse(vv_output, panel_dict):
    """ Parses the response of a gene2transcripts request to VV API, adds transcript info to panel_dict"""
    for vv_gene_record in vv_output:
        ID = vv_gene_record['hgnc']
        
        try:
            transcript = vv_gene_record['transcripts'][0]['reference'] # if the gene record has no transcript, this line can IndexError

            for gene_record in panel_dict['Genes']:
                if list(gene_record.keys())[0] == ID:
                    gene_record[ID].append(transcript)
        except:
            transcript = "No MANE SELECT transcript found"
            for gene_record in panel_dict['Genes']:
                if list(gene_record.keys())[0] == ID:
                    gene_record[ID].append(transcript)
            
           
    return panel_dict

