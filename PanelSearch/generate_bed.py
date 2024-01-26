"""
This script processes gene panel data provided in JSON format to generate output in two formats: 
a BED file suitable for genomic analysis and a JSON file for database integration. It efficiently reads 
command-line arguments for input data and desired output filenames. This dual-format output ensures compatibility 
with genomic analysis tools and facilitates easy integration with SQL databases.
"""
import json
import sys
import logging
from logging.handlers import RotatingFileHandler

# Set up logging to include both file and console logging
log_file = 'generate_bed.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
    ]
)

def parse_panel_data(json_data, coord_type, padding):
    """
    Parses panel data from JSON and extracts gene information.

    Args:
        json_data (str): JSON string containing panel data.

        coord_type (str): string specifying whether the user wants
                          genomic or transcript coordiantes in the
                          produced bed file.
        
        padding (int): the number of base pairs added either side
                       of exon boundaries extracted from the VV
                       API.
    Returns:
        list: List of dictionaries representing BED data.
    """
    try:
        printed_panel = json.loads(json_data)
        logging.debug("JSON data parsed successfully.")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        sys.exit(1)

    genes = printed_panel.get('Genes', [])
    beds = []
    for gene_dict in genes:
        for hgnc_id, info in gene_dict.items():
            
            # Basic information:
            
            bed = {}

            symbol = info[0]
            chr = info[1][0]
            transcript = info[3]
            strand = info[5]

            bed['chromosome'] = chr
            bed['gene'] = symbol
            bed['transcript'] = transcript
            bed['strand'] = strand

            if coord_type == 'trans':
                bed['coordinates'] = 'transcript'
            elif coord_type == 'gen':
                bed['coordinates'] = 'genomic'

            bed['exons'] = []

            for exon in info[4]:

                exon_bed = {}

                for k, v in exon.items():
                    exon_bed['exon_no'] = k
                    
                    if coord_type == 'trans':
                        exon_bed['start'] = int(v[0]) - padding
                        if int(exon_bed['start']) < 0:
                            exon_bed['start'] = 0
                        
                        exon_bed['end'] = v[1] + padding
                    
                    elif coord_type == 'gen':
                        exon_bed['start'] = (int(v[2]) - 1) - padding
                        if int(exon_bed['start']) < 0:
                            exon_bed['start'] = 0
                        
                        exon_bed['end'] = (int(v[3]) - 1) + padding
                
                bed['exons'].append(exon_bed)
            
            beds.append(bed)
                
    return beds

def write_bed_file(beds, filename, coord_type, genome_build):
    """
    Writes BED data to a file in both BED and JSON formats.

    Args:
        beds (list): List of BED data.
        filename (str): Filename for the output BED file.

        coord_type (str): The type of coordinates, genomic or
                         transcript, used to generate the bed
                         file. 
    Returns:
        tuple: (bool, str) Indicates success status and message.
    """
    try:
        # Write to BED file
        with open(filename, 'w') as file:
            if coord_type == 'trans':
                headline = 'transcript\tstart\tend\tlabel\tscore\tstrand'
            elif coord_type == 'gen':
                headline = 'chromosome\tstart\tend\tlabel\tgene\tscore\tstrand'
            file.write(headline)
            
            for bed in beds:
                for exon in bed['exons']:
                    if coord_type == 'trans':
                        line = f"\n{bed['transcript']}\t{exon['start']}\t{exon['end']}\t{genome_build}_{bed['gene']}_ex{exon['exon_no']}\t---\t{bed['strand']}"
                    elif coord_type == 'gen':
                        line = f"\n{bed['chromosome']}\t{exon['start']}\t{exon['end']}\t{bed['transcript']}_{bed['gene']}_ex{exon['exon_no']}\t---\t{bed['strand']}"
                    file.write(line)

        # Write to JSON file
        json_filename = filename.replace('.bed', '.json')
        with open(json_filename, 'w') as json_file:
            json.dump({'bed_regions': beds}, json_file, indent=4)
        logging.info(f"BED and JSON files written successfully.")
        return True, "Success"

    except Exception as e:
        error_message = f"Error writing files: {e}"
        logging.error(error_message)
        return False, error_message

def main():
    """
    Main function to process panel data and generate BED and JSON files.
    """
    if len(sys.argv) < 4:
        logging.warning("Insufficient arguments provided. Exiting.")
        sys.exit(1)

    try:
        printed_panel_json = sys.argv[1]
        filename = sys.argv[2]
        genome_build = sys.argv[3]
        coord_type = sys.argv[4]
        padding_value = sys.argv[5]
        
        
        
        logging.info(f"Using a padding value of +/- {padding_value} bp.")


        beds = parse_panel_data(printed_panel_json, coord_type, padding_value)
        write_bed_file(beds, filename, coord_type, genome_build)

        bed_file_config = coord_type + "-" + str(padding_value)
        return bed_file_config
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

