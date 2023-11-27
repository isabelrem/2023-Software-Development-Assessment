"""
The main function of this script processes gene panel data provided in JSON format, generating a BED file 
suitable for genomic analysis. It reads command-line arguments for input data and output file name, ensuring 
efficient and accurate conversion of panel data into the BED file format.
"""
import json
import sys
import logging
from logging.handlers import RotatingFileHandler

# Set up logging
log_file = 'generate_bed.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10000, backupCount=1),
        logging.StreamHandler(sys.stdout)
    ]
)

def parse_panel_data(json_data):
    """
    Parses panel data from JSON and extracts gene information.
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
        for gene, coords in gene_dict.items():
            chromosome, positions = coords[0], coords[1]
            start, end = positions.split('-')
            bed = {
                'chromosome': chromosome,
                'start': str(int(start) - 1),  # Adjust start position for zero-based indexing
                'end': end,
                'gene': gene
            }
            beds.append(bed)
    
    return beds

def write_bed_file(beds, filename):
    """
    Writes the BED data to a file in BED format.
    """
    try:
        with open(filename, 'w') as file:
            for bed in beds:
                line = f"{bed['chromosome']}\t{bed['start']}\t{bed['end']}\t{bed['gene']}\n"
                file.write(line)
        logging.info(f"BED file written successfully to {filename}")
    except Exception as e:
        logging.error(f"Error writing BED file: {e}")

def main():
    """
    Main function to process panel data and generate a BED file.
    """
    if len(sys.argv) < 3:
        logging.warning("Insufficient arguments provided. Exiting.")
        sys.exit(1)

    try:
        printed_panel_json = sys.argv[1]
        filename = sys.argv[2]
        beds = parse_panel_data(printed_panel_json)
        write_bed_file(beds, filename)
        logging.info(f"BED file generated successfully as {filename}.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
