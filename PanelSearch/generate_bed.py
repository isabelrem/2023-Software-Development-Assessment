import sys
import json
 
# Check if the input argument is provided
if len(sys.argv) < 2:
    print("No input data provided.")
    sys.exit(1)
 
# The first argument is the script name, the second argument is the panel data in JSON format
printed_panel_json = sys.argv[1]
 
# Deserialize the JSON string back into a Python object (dictionary)
try:
    printed_panel = json.loads(printed_panel_json)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
    sys.exit(1)
 
# Extract genes from the panel data
genes = printed_panel.get('Genes', [])
 
# Generate BED file
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
 
# Serialize BED data to JSON
bed_json = json.dumps(beds, indent=4)
 
# Write the BED data to a JSON file
with open('beds.json', 'w') as f:
    f.write(bed_json)
 
print("BED file generated successfully.")