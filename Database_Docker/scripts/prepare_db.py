import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os


databaseServer = os.environ['DATABASE_SERVER']
databaseServerPort = os.environ['DATABASE_SERVER_PORT']
entrypointDatabaseName = os.environ['ENTRYPOINT_DATABASE_NAME']
databaseUser = os.environ['DATABASE_USER']
databaseUserPassword = os.environ['DATABASE_USER_PASSWORD']
targetDatabaseName = os.environ['TARGET_DATABASE_NAME']
rawDataTableName = os.environ['RAW_DATATABLE_NAME']
companyNameTableName = os.environ['COMPANYNAME_TABLE_NAME']
pickupLatitudeTableName = os.environ['PICKUP_LATITUDE_TABLE_NAME']
pickupLongitudeTableName = os.environ['PICKUP_LONGITUDE_TABLE_NAME']
dropoffLatitudeTableName = os.environ['DROPOFF_LATITUDE_TABLE_NAME']
dropoffLongitudeTableName = os.environ['DROPOFF_LONGITUDE_TABLE_NAME']

def GetBaseConnection():
    try:
        connection = psycopg2.connect(database=entrypointDatabaseName, user=databaseUser, password=databaseUserPassword, host=databaseServer, port=databaseServerPort)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        return connection
    except:
        print("I am unable to connect to the database")
        return

def GetTargetConnection():
    try:
        connection = psycopg2.connect(database=targetDatabaseName, user=databaseUser, password=databaseUserPassword, host=databaseServer, port=databaseServerPort)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        return connection
    except:
        print("I am unable to connect to the database")
        return

def CreateRawDataTable(cursor):
    print("Creating new table: " + rawDataTableName)
    cursor.execute("""CREATE TABLE """ + rawDataTableName + """(
        taxi_id integer,
    	trip_start_timestamp timestamp,
    	trip_end_timestamp timestamp,
    	trip_seconds integer,
    	trip_miles real,
    	pickup_census_tract integer,
    	dropoff_census_tract integer,
    	pickup_community_area integer,
    	dropoff_community_area integer,
    	fare real,
    	tips real,
    	tolls real,
    	extras real,
    	trip_total real,
    	payment_type varchar,
    	company integer,
    	pickup_latitude integer,
    	pickup_longitude integer,
    	dropoff_latitude integer,
    	dropoff_longitude integer
    )""")

def CreateCompanyNameTable(cursor):
    print("Creating new table: " + companyNameTableName)
    cursor.execute("""CREATE TABLE """ + companyNameTableName + """(
        company_id integer PRIMARY KEY,    	
    	company_name varchar    	
    )""")

def CreatePickupLatitudeTable(cursor):
    print("Creating new table: " + pickupLatitudeTableName)
    cursor.execute("""CREATE TABLE """ + pickupLatitudeTableName + """(
        id integer PRIMARY KEY,    	
    	latitude float8    	
    )""")

def CreatePickupLongituedTable(cursor):
    print("Creating new table: " + pickupLongitudeTableName)
    cursor.execute("""CREATE TABLE """ + pickupLongitudeTableName + """(
        id integer PRIMARY KEY,    	
    	longitude float8    	
    )""")

def CreateDropoffLatitudeTable(cursor):
    print("Creating new table: " + dropoffLatitudeTableName)
    cursor.execute("""CREATE TABLE """ + dropoffLatitudeTableName + """(
        id integer PRIMARY KEY,    	
    	latitude float8    	
    )""")

def CreateDropoffLongituedTable(cursor):
    print("Creating new table: " + dropoffLongitudeTableName)
    cursor.execute("""CREATE TABLE """ + dropoffLongitudeTableName + """(
        id integer PRIMARY KEY,    	
    	longitude float8    	
    )""")


print("Starting database preperation")

currentConnection = GetBaseConnection()
cur = currentConnection.cursor()

print("Dropping existing database: " + targetDatabaseName)
cur.execute('DROP DATABASE IF EXISTS ' + targetDatabaseName)

print("Creating new database: " + targetDatabaseName)
cur.execute('CREATE DATABASE ' + targetDatabaseName)
cur.close()
# Switch connection to new database
currentConnection = GetTargetConnection()
cur = currentConnection.cursor()

CreateRawDataTable(cur)
CreateCompanyNameTable(cur)
CreatePickupLatitudeTable(cur)
CreatePickupLongituedTable(cur)
CreateDropoffLongituedTable(cur)
CreateDropoffLatitudeTable(cur)

print("Finished database preperation")
