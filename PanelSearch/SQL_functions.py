"""
Connect to MySQL database and add new records
"""
# Import functions and packages
from sqlalchemy import *
from pymysql import *
import pandas as pd
#print(pymysql.__version__) #1.4.6
#print(sqlalchemy.__version__) # 2.0.23

## establishing connectivity - the engine 
# this is my login to my local SQL server - works for local testing purposes but won't sync.
engine = create_engine("mysql+pymysql://root:birbtime@localhost/panelsearch")


def connect_db():
  import sqlalchemy
  import pymysql
  from sqlalchemy import create_engine

  engine = create_engine("mysql+pymysql://root:birbtime@localhost/panelsearch")
        # this is my login to my local SQL server - works for local testing purposes but won't sync.
        # root = username
        # birbtime = password
        # local host = host name
        # panelsearch = database name

  return engine # is this line necessary?
  


def add_new_record(pid,panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file):
  
 
  with engine.connect() as conn:
    from sqlalchemy import select, Table, Column, Integer, String, MetaData
    meta = MetaData()
          
    # initiate table object to allow use of certain functions in sqlalchemy    
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
    stmt7 = select(searches_table).where(searches_table.c.transcript == transcript)
    stmt8 = select(searches_table).where(searches_table.c.genome_build == genome_build)
    stmt9 = select(searches_table).where(searches_table.c.bed_file == bed_file)
      
    # looking for rows where all column values match the column values of the input - this defines the intersection we're looking for
    int = intersect_all(stmt1,stmt2,stmt3,stmt4,stmt5,stmt6,stmt7,stmt8,stmt9)

    # = subselection where the intersection exists
    result = conn.execute(int)

    # pulls out first row of intersection - should only be one if code has worked previously  
    result = result.first()
    print(result) 

    
    if result == None: # i.e. if there is no row which matches the input given
        
      # insert input as new row into table
      result = conn.execute(text("INSERT INTO searches (panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file) VALUES (:panel_id, :panel_name, :panel_version, :GMS, :gene_number, :r_code, :transcript, :genome_build, :bed_file)"),
                  [{"panel_id": panel_id, "panel_name": panel_name, "panel_version":panel_version, "GMS":GMS, "gene_number":gene_number, "r_code":r_code, "transcript":transcript,"genome_build":genome_build,"bed_file":bed_file}],
                  )
        # grab the auto-generated id from the newly inserted entry
        # so we can add the search id to the patients table
      searches_id = result.lastrowid 
      print(searches_id)

      conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                       [{"patient_id":pid, "search_id":searches_id}])
      conn.commit()

    else:
      # grab the search id from the intersection result
      searches_id = result[0]

      # search for duplicate entries for patients table here too
        
      # initiate table object to allow use of certain functions in sqlalchemy    
      patients_table = Table(
        "patients",meta,
        Column('id',Integer,primary_key = True),
        Column('patient_id',String),
        Column('search_id',String),
      )
        
      meta.create_all(engine)
       # is there already a row in the patients table with the same patient and searches id? if not, add new entry. If not, 
      # warn of existing entry and exit.

      stmt1 = select(patients_table).where(patients_table.c.patient_id == pid)
      stmt2 = select(patients_table).where(patients_table.c.search_id == searches_id)

      int2 = intersect_all(stmt1,stmt2)

      result = conn.execute(int2)

      result = result.first()

      if result == None:
        conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                        [{"patient_id":pid, "search_id":searches_id}])
        conn.commit()
      else:
        print("this record already exists")


####################
# Testing and checks
####################
connect_db()

# one entry
add_new_record(pid = "O107",panel_id = 3,panel_name = "A condition",panel_version = 1,GMS= "yes",gene_number= 2,r_code= "R35", transcript = "a really good one",genome_build = 37,bed_file= "placeholder")
# another entry with a unique combination of column values
add_new_record(pid = "O206",panel_id = 3,panel_name = "Another condition",panel_version = 1,GMS= "yes",gene_number= 3,r_code= "R140",  transcript = "a really good one",genome_build = 37,bed_file= "placeholder")
# an entry where only the patient id is unique, the combination of the rest of the column values is not
add_new_record(pid = "O333",panel_id = 3,panel_name = "Another condition",panel_version = 1,GMS= "yes",gene_number= 3,r_code= "R140", transcript = "a really good one",genome_build = 37,bed_file= "placeholder")

# Print searches table
table = pd.read_sql_table(table_name = "searches", con = engine)
print(table)

# Print patients table
table = pd.read_sql_table(table_name = "patients", con = engine)
print(table)