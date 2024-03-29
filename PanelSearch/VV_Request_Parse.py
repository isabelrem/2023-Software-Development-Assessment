"""
A function which parses the json format object returned by the
VV API and extracts the mane_select transcript from it. Adds this
to the input dictionary.
"""

def vv_request_parse(vv_output, panel_dict):
    """ Parses the response of a gene2transcripts request to VV, 
        API adds transcript info to panel_dict"""
    
    for vv_gene_record in vv_output:
        ID = vv_gene_record['hgnc']
        
        genome_direction = list(vv_gene_record['transcripts'][0]['genomic_spans'].values())[0]['orientation']
        if genome_direction == 1:
            genome_direction = '+'
        elif genome_direction == -1:
            genome_direction = '-'

        try:
            transcript = vv_gene_record['transcripts'][0]['reference'] # if the gene record has no transcript, this line can IndexError
        except IndexError:
            transcript = "No MANE SELECT transcript found"

        try:
            exon_coords = []
            exons_record = list(vv_gene_record['transcripts'][0]['genomic_spans'].values())[0]['exon_structure']
            for exon_record in exons_record:
                exon_no = exon_record['exon_number']
                gen_start = exon_record['genomic_start']
                gen_end = exon_record['genomic_end']
                trans_start = exon_record['transcript_start']
                trans_end = exon_record['transcript_end']

                exon_coords.append({exon_no : [trans_start, trans_end, gen_start, gen_end]})
        except:
            exon_coords.append("No exon coordinates found")

        for gene_record in panel_dict['Genes']:
            if list(gene_record.keys())[0] == ID:
                gene_record[ID].append(transcript)
                gene_record[ID].append(exon_coords)
                gene_record[ID].append(genome_direction)
    
    return panel_dict

