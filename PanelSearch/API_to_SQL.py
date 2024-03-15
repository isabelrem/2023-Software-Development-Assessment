from PanelApp_API_Request import *
from PanelApp_Request_Parse import *
from SQL_Functions import connect_db, add_new_record
import pandas as pd

# opens API connection
RQ = PanelAppRequest()

def PK_Parse_Data_to_SQL(pid, genome_build, PK, bed_filename, bed_file_config):

    response = RQ.pk_search(PK)
    result = panelapp_search_parse(response.json(), genome_build)
    
    transcript_list = []

    for gene in result['Genes']:
        for k, v in gene.items():
            transcript_list.append(v[3])

    transcripts=', '.join([str(item) for item in transcript_list])
    print(transcripts)


    panel_id = result["Panel ID"]
    panel_name = result["Panel Name"]
    GMS = result["GMS Signed-off"]
    gene_number = result["Gene Number"]
    r_code = result["R Codes"]
    panel_version = result["Version"] 
    bed_file = "No BED file generated"

    if bed_filename != "no BED file generated":
        bed_file = pd.read_csv(bed_filename, delimiter = '\t')
        bed_file = bed_file.to_string(index = False)
     
    connect_db()

    add_new_record(pid = pid,panel_id = panel_id,panel_name = panel_name, panel_version = panel_version,GMS= GMS,gene_number= gene_number,r_code= r_code , transcript = transcripts,genome_build = genome_build,bed_file_config = bed_file_config, bed_file=bed_file)

    return "Function run"

### TESTING ###

#PK_Parse_Data_to_SQL("Uno", "GRch37", "Cystic renal disease")
#RC_Parse_Data_to_SQL("Dos", "GRch37", "R195")

#engine = connect_db()
#table = pd.read_sql_table(table_name = "searches", con = engine)
#print(table)
#table = pd.read_sql_table(table_name = "patients", con = engine)
#print(table)
