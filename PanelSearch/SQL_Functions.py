"""
Connect to local MySQL server stored in a separate docker container 'panelsearch-database' 
and save API searches to database
"""
# Install packages
from sqlalchemy import *
from pymysql import *
import pandas as pd
import os
import datetime

## Establishing connectivity - the engine
def connect_db():
    """
    Connect to the MySQL database in the docker container
    """
    # docker database details
    username = 'root'
    password = 'password'
    database_name = 'panelsearch'
    database_host = 'panelsearch-database'
    connection_string = f'mysql+pymysql://{username}:{password}@{database_host}:3306/{database_name}'
    
    # attempt to create database engine using docker db details
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
    
# Add record to the database
def add_new_record(pid,panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file_config,bed_file):
    """
    Add a new record to the searches and patients tables in the database
    """
    engine = connect_db()
    
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
            Column('bed_file_config',String),
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
        stmt9 = select(searches_table).where(searches_table.c.bed_file_config == bed_file_config)

        #print("/////////// CHECK 2 /////////////////")

        int = intersect_all(stmt1,stmt2,stmt3,stmt4,stmt5,stmt6,stmt7,stmt8,stmt9)

        result = conn.execute(int).first()

        #print("/////////// CHECK 3 /////////////////")


        # pulls out first row of intersection - should only be one if code has worked previously  
        #print(result)
        #print(result == None)
    
        if result == None: # i.e. if there is no row which matches the input given

            #print("/////////// CHECK 4 /////////////////")
        
            # insert input as new row into table
            result = conn.execute(text("INSERT INTO searches (panel_id,panel_name,panel_version,GMS,gene_number,r_code,transcript,genome_build,bed_file_config, bed_file) VALUES (:panel_id, :panel_name, :panel_version, :GMS, :gene_number, :r_code, :transcript, :genome_build, :bed_file_config, :bed_file)"),
                  [{"panel_id": panel_id, "panel_name": panel_name, "panel_version":panel_version, "GMS":GMS, "gene_number":gene_number, "r_code":r_code, "transcript":transcript,"genome_build":genome_build,"bed_file":bed_file,"bed_file_config":bed_file_config}],
                  )
            # grab the auto-generated id from the newly inserted entry
            # so we can add the search id to the patients table
            
            #print("/////////// CHECK 5 /////////////////")
            searches_id = result.lastrowid 
            print(searches_id)

            conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                       [{"patient_id":pid, "search_id":searches_id}])
            conn.commit()

            #print("/////////// CHECK 6 /////////////////")

        elif result != None:
             # i.e. if there is a row which matches the input given
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

    return result

def browse_records(patient_id=''):
        # connect to database
        engine = connect_db()
        # search patient id table and searches id table separately
        # if no patient id supplied, show all of both tables
        # if patient id supplied, show patient entry and then ask user if they want to look at the related searches entries and if so which
        if patient_id == '':
             patients_table = pd.read_sql_table(table_name = "patients", con = engine)
             searches_table = pd.read_sql_table(table_name = "searches", con = engine)
             print("### Patients table ###")
             print(patients_table)
             print("### Searches table ###")
             print(searches_table)
             return(patients_table,searches_table)
        else:
             with engine.connect() as conn:
                meta = MetaData()

                patients_table = Table(
                    "patients",meta,
                    Column('id',Integer,primary_key = True),
                    Column('patient_id',String),
                    Column('search_id',String),
                    )
            
                meta.create_all(engine)

                stmt1 = select(patients_table).where(patients_table.c.patient_id == patient_id)
                patients_query = pd.read_sql(stmt1, con = engine)

                if patients_query.empty:
                    print("This patient ID does not exist in the SQL database")
                    return "This patient ID does not exist in the SQL database"
                else:
                    print("### Patients table for: "+ patient_id + " ###")
                    print(patients_query)
                    
                    searches_request = input("Would you like to see the searches information for this patient? (Y/N) \n")
                    if searches_request.lower() == "y":
                        search_ids = patients_query['search_id'].tolist()
                        
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
                            Column('bed_file_config'),
                            Column('bed_file',String)
                                    )
                        meta.create_all(engine)

                        stmt2 = select(searches_table).where(searches_table.c.id.in_(search_ids))
                        searches_query = pd.read_sql(stmt2, con = engine)
                        print(searches_query)
                        return patients_query,searches_query
                    else:
                        return patients_query
                

# def create_record_filenames(file_name):
#     """ Creates a filename for a downloaded SQL record based on the current date. """
#     panelsearch_downloads = 'panelsearch_downloads'
#     if not os.path.exists(panelsearch_downloads_dir):
#         os.makedirs(panelsearch_downloads_dir)  # Create the folder if it doesn't exist

#     date_str = datetime.datetime.now().strftime("%Y%m%d")
    
#     patients_filename = f"{date_str}_{file_name}_patients.csv"
#     searches_filename = f"{date_str}_{file_name}_searches.csv"
    
#     return os.path.join(panelsearch_downloads_dir, patients_filename), os.path.join(panelsearch_downloads_dir, searches_filename)


def download_records(patients_dataframe,searches_dataframe,file_name = ''):
    """ Allows the user to download their SQL search as a CSV file. """
    print(os.getcwd())
    print(os.listdir())
    # os.chdir('PanelSearch')
    # print(os.getcwd())
    # print(os.listdir())
    file_name = file_name.replace(' ','_')
    try:
        panelsearch_downloads_dir = '/app/panelsearch_downloads/' # change to just panelsearch_downloads - like how the bedfile is made in the main.py?
        if not os.path.exists('/app/panelsearch_downloads/'):
            os.makedirs('/app/panelsearch_downloads/')
    except:
        panelsearch_downloads_dir = '../panelsearch_downloads/'
        if not os.path.exists('../panelsearch_downloads/'):
            os.makedirs('../panelsearch_downloads/')
    #print(os.getcwd())
    #print(os.listdir()) # Create the folder if it doesn't exist
    
    date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    
    
    patients_filename = f"{date_str}_{file_name}_patients.csv"
    searches_filename = f"{date_str}_{file_name}_searches.csv"
    
    
    if type(searches_dataframe) == str:
        patients_dataframe.to_csv(os.path.join(panelsearch_downloads_dir, patients_filename),index = False,)
    else: 
        patients_dataframe.to_csv(os.path.join(panelsearch_downloads_dir, patients_filename),index = False)
        searches_dataframe.to_csv(os.path.join(panelsearch_downloads_dir, searches_filename),index = False)
    
    return patients_filename

    # print(os.listdir())
    # os.chdir('panelsearch_downloads')
    # print(os.listdir())


                    
### TESTING ###
#add_new_record(pid = "ronald",panel_id = 9,panel_name = "heart stuff",panel_version = 1,GMS= "yes",gene_number= 2,r_code= "R38", transcript = "a really good one",genome_build = 37,bed_file= "placeholder")
# engine = connect_db()
# searches_table = pd.read_sql_table(table_name = "searches", con = engine)
# print(table)
# patients_table = pd.read_sql_table(table_name = "patients", con = engine)
# print(table)
#browse_records()
#browse_records('ronald')

