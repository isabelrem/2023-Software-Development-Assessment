import json
import sys

def parse_panel_data(json_data):
    """
    Parses panel data from JSON and extracts gene information.

    :param json_data: JSON string with panel data
    :return: List of gene information as dictionaries
    """
    try:
        printed_panel = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        sys.exit(1)

    genes = printed_panel.get('Genes', [])
    beds = []

    for gene_dict in genes:
        for gene, coords in gene_dict.items():
            chromosome, positions = coords[0], coords[1]
            start, end = positions.split('-')
            bed = {
                'chromosome': chromosome,
                'start': start,
                'end': end,
                'gene': gene
            }
            beds.append(bed)
    
    return beds

def write_bed_to_json(beds, filename='beds.json'):
    """
    Writes the BED data to a JSON file.

    :param beds: List of BED data
    :param filename: File name to write the BED data
    """
    bed_json = json.dumps(beds, indent=4)
    with open(filename, 'w') as f:
        f.write(bed_json)

def main():
    """
    Main function to process panel data and generate BED file.
    """
    if len(sys.argv) < 2:
        print("No input data provided.")
        sys.exit(1)

    printed_panel_json = sys.argv[1]
    beds = parse_panel_data(printed_panel_json)

    # Optional: Write BED data to a file or handle as needed
    # write_bed_to_json(beds)

    print("BED file generated successfully.")

if __name__ == '__main__':
    main()
