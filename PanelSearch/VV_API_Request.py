"""
A class which contains functions to request data from the Variant
Validator API, using a gene symbol or HGNC ID, of which the
transcript information is the desired aspect. Functions also included
for converting genome build strings to the necessary format.
"""

# Imports:
import urllib.parse
import requests


class VVRequest():
    """ A class for requesting information from the VV API"""
    def __init__(self, genome_build):
        self.genome_build = genome_build
        self.genome_build_converted = self.genome_build_convert(self.genome_build)
        
        self.base_url = 'https://rest.variantvalidator.org/'
        self.url = ''

    def genome_build_convert(self, genome_build):
        """ VV API requires genome build in a different format"""
        gnc = ''
        if genome_build == 'GRch37':
            gnc = 'GRCh37'
        elif genome_build == 'GRch38':
            gnc = 'GRCh38'
            
        if gnc:
            return gnc
        else:
            raise ValueError('Invalid genome build passed to VV Request - exiting...')
 
    def request_data(self, prms = None):
        """ Make a request to the Ensembl API and return the response"""
        return requests.get(self.url, params = prms)
    
    def gene_to_transcripts(self, query, ref_type):
        """ Make a request to the VV API gene2transcript v2 endpoint to get back MANE select transcripts"""
        url_query = urllib.parse.quote(query)
        self.url = f"{self.base_url}VariantValidator/tools/gene2transcripts_v2/{url_query}/mane_select/{ref_type}/{self.genome_build_converted}?content-type=application%2Fjson"
        return self.request_data()
    

# Testing purposes
# RQ = VVRequest('GRch37')
# RESPONSE = RQ.gene_to_transcripts('HGNC:4982', 'refseq')

# print(RESPONSE.status_code)
# print(RESPONSE.json())


    
    

