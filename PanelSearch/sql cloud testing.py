# pip install "cloud-sql-python-connector[pymysql]"
# Google Cloud SDK CLI
from google.cloud.sql.connector import *


from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
from pymysql import *

from sqlalchemy import create_engine

def connect_db():
  import sqlalchemy
  import pymysql
  from sqlalchemy import create_engine

  # this is my login to my local SQL server - works for local testing purposes but won't sync.
  engine = create_engine("mysql+pymysql://user:password@35.246.44.89/panelsearch")

        # this is my login to my local SQL server - works for local testing purposes but won't sync.
        # = username
        #  = password
        # = host name
        #  = database name

  return engine # is this line necessary?



'''
# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "stp-software-engineering:europe-west2:panel-search",
        "pymysql",
        user="user",
        password="password",
        db="panelsearch"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

with pool.connect() as conn:
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



connector.close()
'''