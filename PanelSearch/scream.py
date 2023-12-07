import sqlalchemy
import pymysql
from pymysql import *

from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine("mysql+pymysql://user:password@35.246.44.89/panelsearch")

with engine.connect() as conn:
    from sqlalchemy import text
    conn.execute(text("INSERT INTO searches (panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file) VALUES (:panel_id, :panel_name, :panel_version, :GMS, :gene_number, :r_code, :transcript, :genome_build, :bed_file)"),
                  [{"panel_id": 2, "panel_name": "MAKE", "panel_version":1, "GMS":"SOME SENSE", "gene_number":55, "r_code":"fdg", "transcript":"1","genome_build":"37","bed_file":"placeholder"}],
                  )
    conn.commit()






import pandas as pd

table = pd.read_sql_table(table_name = "searches", con = engine)

print(table)

table = pd.read_sql_table(table_name = "patients", con = engine)

print(table)

conn.close()
engine.dispose() 