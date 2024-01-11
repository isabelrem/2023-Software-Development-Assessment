"""
Connect to local MySQL server stored in a separate docker container 'panelsearch-database' 
and save API searches to database
"""
# Install packages
from sqlalchemy import *
from pymysql import *
import pandas as pd

#check to see whether docker SQL database container is running
def docker_or_cloud():
    # docker database details
    username = 'root'
    password = 'password'
    database_name = 'panelsearch'
    database_host = 'panelsearch-database'
    connection_string = f'mysql+pymysql://{username}:{password}@{database_host}:3306/{database_name}'
    attempt = 0
    engine = None

    for i in range(1,10,1):
        try:
            engine = create_engine(connection_string)
            conn = engine.connect()
            conn.close()
            engine.dispose()
            print("successful connection to docker database")
            return connection_string
        except:
            pass
        
    # google cloud database details
    username = 'panelsearch_user'
    password = 'panelsearch_password'
    database_name = 'panelsearch'
    database_host = '35.197.209.133'
    connection_string = f'mysql+pymysql://{username}:{password}@{database_host}:3306/{database_name}'
    engine = create_engine(connection_string)
    conn = engine.connect()
    conn.close()
    engine.dispose()
    print("successful connection to sql database")

    return connection_string

connection_string = docker_or_cloud()

## Establishing connectivity - the engine
def connect_cloud_db():
    """
    Connect to the MySQL database on the cloud-hosted SQL server
    """
    # TODO try connecting to the sql database multiple times
    # bc sometimes mysql needs a few tries
    # TODO set a limit on this bc might not be possile to everr resolve
    engine = None
    attempt = 0
    while (engine is None) and (attempt <= 10):
        try:
            engine = create_engine(connection_string)
        except:
            attempt +=1
            print(attempt)
            pass
    return engine
    
connect_cloud_db()

# Add record to the database
def add_new_cloud_record(pid,panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file):
    """
    Add a new record to the searches and patients tables in the database
    """
    engine = connect_cloud_db()
    
    with engine.connect() as conn:
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
        #print(result)
        #print(result == None)
    
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
            #print(result)

            if result == None:
                conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                                [{"patient_id":pid, "search_id":searches_id}])
                conn.commit()
            else:
                print("this record already exists")

            conn.close()
            engine.dispose()

    return result

        
### TESTING ###
# add_new_cloud_record(pid = "Tres",panel_id = 9,panel_name = "heart stuff",panel_version = 1,GMS= "yes",gene_number= 2,r_code= "R38", transcript = "a really good one",genome_build = 37,bed_file= "placeholder")
#
# engine = connect_cloud_db()
# searches_table = pd.read_sql_table(table_name = "searches", con = engine)
# print(table)
# patients_table = pd.read_sql_table(table_name = "patients", con = engine)
# print(table)
