# progressively smaller databases as filter by each thing?

import sqlalchemy
import pymysql
#print(pymysql.__version__) #1.4.6
#print(sqlalchemy.__version__) # 2.0.23

## establishing connectivity - the engine 

from sqlalchemy import create_engine

from sqlalchemy import text

from sqlalchemy import exists
from sqlalchemy import select


def connect_cloud_db():
  import sqlalchemy
  import pymysql
  from sqlalchemy import create_engine

  engine = create_engine("mysql+pymysql://user:password@35.246.44.89/panelsearch")

        # this is the login to the cloud hosted SQL server
        # user = username
        #  password = password
        # 35.246.44.89 = host name
        # panelsearch = database name

  return engine 
  


def add_new_cloud_record(pid,panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file):
    
    engine = connect_cloud_db()
    
    with engine.connect() as conn:
        from sqlalchemy import text, select, Table, Column, Integer, String, MetaData, intersect_all
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
        
        #print("/////////// CHECK 1 /////////////////")

        meta.create_all(engine)

        stmt1 = select(searches_table).where(searches_table.c.panel_id == panel_id)
        stmt2 = select(searches_table).where(searches_table.c.panel_name == panel_name)
        stmt3 = select(searches_table).where(searches_table.c.panel_version == panel_version)
        stmt4 = select(searches_table).where(searches_table.c.GMS == GMS)
        stmt5 = select(searches_table).where(searches_table.c.gene_number == gene_number)
        stmt6 = select(searches_table).where(searches_table.c.r_code == r_code)
        stmt7 = select(searches_table).where(searches_table.c.transcript == transcript)
        stmt8 = select(searches_table).where(searches_table.c.genome_build == genome_build)
        stmt9 = select(searches_table).where(searches_table.c.bed_file == bed_file)

        #print("/////////// CHECK 2 /////////////////")

        int = intersect_all(stmt1,stmt2,stmt3,stmt4,stmt5,stmt6,stmt7,stmt8,stmt9)

        result = conn.execute(int).first()
        
        #print(result)
              

        #print("/////////// CHECK 3 /////////////////")


        # pulls out first row of intersection - should only be one if code has worked previously  
        print(result)
        print(result == None)
    
        if result == None: # i.e. if there is no row which matches the input given

            #print("/////////// CHECK 4 /////////////////")
        
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

        else: # i.e. if there is a row which matches the input given
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

            int = intersect_all(stmt1,stmt2)
            result = conn.execute(int)
            

            result = result.first()
            print(result)

            if result == None:
                conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                                [{"patient_id":pid, "search_id":searches_id}])
                conn.commit()
            else:
                print("this record already exists")

            conn.close()
            engine.dispose()  

        
        
add_new_cloud_record(pid = "Birb!",panel_id = 9,panel_name = "buddy is a lovely birb",panel_version = 1,GMS= "yes",gene_number= 2,r_code= "R38", transcript = "a really good one",genome_build = 37,bed_file= "placeholder")

engine = connect_cloud_db()

import pandas as pd

table = pd.read_sql_table(table_name = "searches", con = engine)

print(table)

table = pd.read_sql_table(table_name = "patients", con = engine)

print(table)