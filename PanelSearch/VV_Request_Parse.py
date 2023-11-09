def vv_request_parse(vv_output, panel_dict):
    """ Parses the response of a gene2transcripts request to VV API, adds transcript info to panel_dict"""
    for vv_gene_record in vv_output:
        ID = vv_gene_record['hgnc']
        print(ID)
        transcript = vv_gene_record['reference']

        for gene_record in panel_dict['Genes']:
            if list(gene_record.keys()[0]) == ID:
                gene_record[id].append(transcript)
    
    return panel_dict

