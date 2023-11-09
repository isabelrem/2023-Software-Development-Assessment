import sqlalchemy
import pymysql
print(sqlalchemy.__version__) # 2.0.23

## establishing connectivity - the engine 

from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:birbtime@localhost/panelsearch")

import pandas as pd

table = pd.read_sql_table(table_name = "patients", con = engine)

print(table)

from sqlalchemy import text

from sqlalchemy import exists
from sqlalchemy import select

class Database_Add:
  def connect_db():
        import sqlalchemy
        import pymysql
        from sqlalchemy import create_engine

        engine = create_engine("mysql+pymysql://root:birbtime@localhost/panelsearch")
        # root = username
        # birbtime = password
        # local host = host name
        # panelsearch = database name

        return engine # is this line necessary?
  


  def add_new_record(pid,panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file):
    
    # exclude bedfile from check

    # check if searches row already exists in searches table
    # if yes, assign patient the same search id
    # if no, create new row in searches, grab the searches id and 
    # assign to patient
  

  # THIS IS IF ROW DOES NOT YET EXIST IN SEARCHES TABLE

    with engine.connect() as conn:
      from sqlalchemy import select, Table, Column, Integer, String, MetaData
      meta = MetaData()
          
      searches_table = Table(
        "searches",meta,
         Column('id',Integer,primary_key = True),
         Column('panel_id',Integer),
         Column('panel_name',String),
         Column('panel_version',String),
         Column('GMS',String),
         Column('gene_number',Integer),
         Column('r_code',String),
         Column('transcript',String),
         Column('genome_build',String),
         Column('bed_file',String),
         )

      meta.create_all(engine)

      from sqlalchemy import intersect_all
      stmt1 = select(searches_table).where(searches_table.c.panel_id == panel_id)
      stmt2 = select(searches_table).where(searches_table.c.panel_name == panel_name)
      stmt3 = select(searches_table).where(searches_table.c.panel_version == panel_version)
      stmt4 = select(searches_table).where(searches_table.c.GMS == GMS)
      stmt5 = select(searches_table).where(searches_table.c.gene_number == gene_number)
      stmt6 = select(searches_table).where(searches_table.c.r_code == r_code)
      stmt8 = select(searches_table).where(searches_table.c.transcript == transcript)
      stmt9 = select(searches_table).where(searches_table.c.genome_build == genome_build)
      stmt10 = select(searches_table).where(searches_table.c.bed_file == bed_file)
      
      int = intersect_all(stmt1,stmt2,stmt3,stmt4,stmt5,stmt6,stmt7,stmt8,stmt9,stmt10)

      result = conn.execute(int)
        
      result = result.first()
      print(result)

      
     

      if result == None:
        result = conn.execute(text("INSERT INTO searches (panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file) VALUES (:panel_id, :panel_name, :panel_version, :GMS, :gene_number, :r_code, :transcript, :genome_build, :bed_file)"),
                  [{"panel_id": panel_id, "panel_name": panel_name, "panel_version":panel_version, "GMS":GMS, "gene_number":gene_number, "r_code":r_code, "transcript":transcript,"genome_build":genome_build,"bed_file":bed_file}],
                  )
        searches_id = result.lastrowid 
        print(searches_id)
        conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                       [{"patient_id":pid, "search_id":searches_id}])
        conn.commit()

      else:
        searches_id = result[0]
        conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                       [{"patient_id":pid, "search_id":searches_id}])
        conn.commit()

        

    




Database_Add.connect_db()
Database_Add.add_new_record(pid = "gdsdfasdfsdfsfg",panel_id = 3,panel_name = "eatshit",panel_version = 1,GMS= "yes",gene_number= 4,r_code= "R35",transcript = "safdf",genome_build = 37.5,bed_file= "sgs")

Database_Add.add_new_record(pid = "FUCK",panel_id = 3,panel_name = "3253",panel_version = 1,GMS= "yes",gene_number= 4,r_code= "R35",transcript = "safdf",genome_build = 37.5,bed_file= "sgs")


import pandas as pd

table = pd.read_sql_table(table_name = "searches", con = engine)

print(table)

table = pd.read_sql_table(table_name = "patients", con = engine)

print(table)