from PanelApp_API_Request import *
from PanelApp_Request_Parse import *
from SQL_functions import *

RQ = PanelAppRequest()

def PK_Parse_Data_to_SQL(pid, genome_build, PK):
    response = RQ.pk_search(PK)
    result = PanelApp_Request_Parse.search_parse(response.json(), genome_build)

    #print(result)
    panel_id = result["Panel ID"]
    panel_name = result["Panel Name"]
    GMS = result["GMS Signed-off"]
    gene_number = result["Gene Number"]
    r_code = result["R Codes"]
    panel_version = 1 # PLACEHOLDER - not in the API yet

    connect_db()

    add_new_record(pid = pid,panel_id = panel_id,panel_name = panel_name, panel_version = panel_version,GMS= GMS,gene_number= gene_number,r_code= r_code , transcript = "a really good one",genome_build = genome_build,bed_file= "placeholder")


def RC_Parse_Data_to_SQL(pid, genome_build, R_code):
    response_R = RQ.R_search(R_code)
    result = PanelApp_Request_Parse.search_parse(response_R.json(), genome_build)

    #print(result)
    panel_id = result["Panel ID"]
    panel_name = result["Panel Name"]
    GMS = result["GMS Signed-off"]
    gene_number = result["Gene Number"]
    r_code = result["R Codes"]
    panel_version = 1 # PLACEHOLDER - not in the API yet

    connect_db()

    add_new_record(pid = pid,panel_id = panel_id,panel_name = panel_name, panel_version = panel_version,GMS= GMS,gene_number= gene_number,r_code= r_code , transcript = "a really good one",genome_build = genome_build,bed_file= "placeholder")


PK_Parse_Data_to_SQL("Patient A", "GRch37", "Long QT syndrome")
RC_Parse_Data_to_SQL("Patient B", "GRch37", "R140")



import pandas as pd

table = pd.read_sql_table(table_name = "searches", con = engine)

print(table)

table = pd.read_sql_table(table_name = "patients", con = engine)

print(table)