"""
Connect to SQL database and add new record
"""
# Import python packages
from sqlalchemy import *
# from pymysql import *  # for some reason this module is not needed in Jess's version? Try with/without it?
import pandas as pd

# print(pymysql.__version__) #1.4.6
# print(sqlalchemy.__version__) # 2.0.23

## establishing connectivity - the engine 

# from sqlalchemy import create_engine  # importing packages at start should mean that this line is not required

# this is my login to my local SQL server - works for local testing purposes but won't sync.
"""
root = username
birbtime = password
local host = host name
panelsearch = database name
"""
engine = create_engine("mysql+pymysql://root:birbtime@localhost/panelsearch")

# from sqlalchemy import text  # importing packages at start should mean that this line is not required
#
# from sqlalchemy import exists  # importing packages at start should mean that this line is not required
# from sqlalchemy import select  # importing packages at start should mean that this line is not required


def connect_db():
    # import sqlalchemy # importing packages at start should mean that this line is not required
    # import pymysql # importing packages at start should mean that this line is not required
    # from sqlalchemy import create_engine  # importing packages at start should mean that this line is not required

    # this is my login to my local SQL server - works for local testing purposes but won't sync.
    """
    root = username
    birbtime = password
    local host = host name
    panelsearch = database name
    """
    engine = create_engine("mysql+pymysql://root:birbtime@localhost/panelsearch")

    return engine  # is this line necessary? Yes ideally a function should return something - useful for pytest tests :)


def add_new_record(pid, panel_id, panel_name, panel_version, GMS, gene_number, r_code, genes, transcript, genome_build,
                   bed_file):
    """
    Need description here
    :param pid:
    :param panel_id:
    :param panel_name:
    :param panel_version:
    :param GMS:
    :param gene_number:
    :param r_code:
    :param genes:
    :param transcript:
    :param genome_build:
    :param bed_file:
    :return:
    """

    with engine.connect() as conn:
        from sqlalchemy import select, Table, Column, Integer, String, MetaData
        meta = MetaData()

        # initiate table object to allow use of certain functions in sqlalchemy
        searches_table = Table(
            "searches", meta,
            Column('id', Integer, primary_key=True),
            Column('panel_id', Integer),
            Column('panel_name', String),
            Column('panel_version', String),
            Column('GMS', String),
            Column('gene_number', Integer),
            Column('r_code', String),
            Column('genes', String),
            Column('transcript', String),
            Column('genome_build', String),
            Column('bed_file', String),
        )

        meta.create_all(engine)

        # from sqlalchemy import intersect_all # importing packages at start should mean that this line is not required

        stmt1 = select(searches_table).where(searches_table.c.panel_id == panel_id)
        stmt2 = select(searches_table).where(searches_table.c.panel_name == panel_name)
        stmt3 = select(searches_table).where(searches_table.c.panel_version == panel_version)
        stmt4 = select(searches_table).where(searches_table.c.GMS == GMS)
        stmt5 = select(searches_table).where(searches_table.c.gene_number == gene_number)
        stmt6 = select(searches_table).where(searches_table.c.r_code == r_code)
        stmt7 = select(searches_table).where(searches_table.c.genes == genes)
        stmt8 = select(searches_table).where(searches_table.c.transcript == transcript)
        stmt9 = select(searches_table).where(searches_table.c.genome_build == genome_build)
        stmt10 = select(searches_table).where(searches_table.c.bed_file == bed_file)

        # looking for rows where all column values match the column values of the input - this defines the
        # intersection we're looking for
        int1 = intersect_all(stmt1, stmt2, stmt3, stmt4, stmt5, stmt6, stmt7, stmt8, stmt9, stmt10)

        # = subselection where the intersection exists
        result = conn.execute(int1)

        # pulls out first row of intersection - should only be one if code has worked previously
        result = result.first()
        print(result)

        if result is None:  # i.e. if there is no row which matches the input given

            # insert input as new row into table
            result = conn.execute(text(
                "INSERT INTO searches (panel_id, panel_name, panel_version, GMS, gene_number, r_code, genes, "
                "transcript, genome_build,bed_file) "
                "VALUES (:panel_id, :panel_name, :panel_version, :GMS, :gene_number, :r_code, :genes, :transcript, "
                ":genome_build, :bed_file)"),
                                  [{"panel_id": panel_id, "panel_name": panel_name, "panel_version": panel_version,
                                    "GMS": GMS, "gene_number": gene_number, "r_code": r_code, "genes": genes,
                                    "transcript": transcript, "genome_build": genome_build, "bed_file": bed_file}],
                                  )
            # grab the auto-generated id from the newly inserted entry
            # so we can add the search id to the patients table
            searches_id = result.lastrowid
            print(searches_id)

            conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                         [{"patient_id": pid, "search_id": searches_id}])
            conn.commit()

        else:
            # grab the search id from the intersection result
            searches_id = result[0]

            # search for duplicate entries for patients table here too

            # initiate table object to allow use of certain functions in sqlalchemy
            patients_table = Table(
                "patients", meta,
                Column('id', Integer, primary_key=True),
                Column('patient_id', String),
                Column('search_id', String),
            )

            meta.create_all(engine)
            # is there already a row in the patients table with the same patient and searches id? if not,
            # add new entry. If not, warn of existing entry and exit.

            stmt1 = select(patients_table).where(patients_table.c.patient_id == pid)
            stmt2 = select(patients_table).where(patients_table.c.search_id == searches_id)

            int2 = intersect_all(stmt1, stmt2)

            result = conn.execute(int2)

            result = result.first()

            if result is None:
                conn.execute(text("INSERT INTO patients (patient_id,search_id) VALUES (:patient_id, :search_id)"),
                             [{"patient_id": pid, "search_id": searches_id}])
                conn.commit()
            else:
                print("this record already exists")


connect_db()

############
# TESTING #
############

# add one entry
add_new_record(pid="O107", panel_id=3, panel_name="A condition", panel_version=1, GMS="yes", gene_number=2,
               r_code="R35", genes=["BCR", "ABL1"], transcript="a really good one", genome_build=37,
               bed_file="placeholder")

# add another entry with a unique combination of column values
add_new_record(pid="O206", panel_id=3, panel_name="Another condition", panel_version=1, GMS="yes", gene_number=3,
               r_code="R140", genes=["BRCA1", "BRCA2"], transcript="a really good one", genome_build=37,
               bed_file="placeholder")

# add an entry where only the patient id is unique, the combination of the rest of the column values is not
add_new_record(pid="O333", panel_id=3, panel_name="Another condition", panel_version=1, GMS="yes", gene_number=3,
               r_code="R140", genes=["PCSK9", "LDLR"], transcript="a really good one", genome_build=37,
               bed_file="placeholder")

# Print searches table (testing purposes)
searches_table = pd.read_sql_table(table_name="searches", con=engine)
print(searches_table)

# Print patients table (testing purposes)
patients_table = pd.read_sql_table(table_name="patients", con=engine)
print(patients_table)
