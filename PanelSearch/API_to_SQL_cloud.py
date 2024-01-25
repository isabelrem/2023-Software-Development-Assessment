from PanelApp_API_Request import *
from PanelApp_Request_Parse import *
from SQL_Cloud_Functions import connect_cloud_db, add_new_cloud_record
import pandas as pd

# opens API connection
RQ = PanelAppRequest()

def PK_Parse_Data_to_SQL_cloud(pid, genome_build, PK):
    """
    Parses API JSON output and stores values as record in SQL database
    """
    try:
        response = RQ.pk_search(PK)
        result = panelapp_search_parse(response.json(), genome_build)

        #print(result)
        panel_id = result["Panel ID"]
        panel_name = result["Panel Name"]
        GMS = result["GMS Signed-off"]
        gene_number = result["Gene Number"]
        r_code = result["R Codes"]
        panel_version = result["Version"] 

        connect_cloud_db()

        add_new_cloud_record(pid = pid,panel_id = panel_id,panel_name = panel_name, panel_version = panel_version,GMS= GMS,gene_number= gene_number,r_code= r_code , transcript = "a really good one",genome_build = genome_build,bed_file="placeholder")

        return panel_id

    except:
        raise ValueError("Please enter correct panel ID, genome build, and panel name.")

### TESTING ###

#PK_Parse_Data_to_SQL_cloud("Uno", "GRch37", "Cystic renal disease")
#RC_Parse_Data_to_SQL_cloud("Dos", "GRch37", "R195")

#engine = connect_cloud_db()
#table = pd.read_sql_table(table_name = "searches", con = engine)
#print(table)
#table = pd.read_sql_table(table_name = "patients", con = engine)
#print(table)
