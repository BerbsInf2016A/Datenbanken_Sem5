import psycopg2
import os
import zipfile
import shutil
import json


databaseServer = os.environ['DATABASE_SERVER']
databaseServerPort = os.environ['DATABASE_SERVER_PORT']
databaseUser = os.environ['DATABASE_USER']
databaseUserPassword = os.environ['DATABASE_USER_PASSWORD']
targetDatabaseName = os.environ['TARGET_DATABASE_NAME']
rawDataTableName = os.environ['RAW_DATATABLE_NAME']
companyNameTableName = os.environ['COMPANYNAME_TABLE_NAME']
pickupLatitudeTableName = os.environ['PICKUP_LATITUDE_TABLE_NAME']
pickupLongitudeTableName = os.environ['PICKUP_LONGITUDE_TABLE_NAME']
dropoffLatitudeTableName = os.environ['DROPOFF_LATITUDE_TABLE_NAME']
dropoffLongitudeTableName = os.environ['DROPOFF_LONGITUDE_TABLE_NAME']

zipSourceFile = 'chicago-taxi-rides-2016.zip'
extractFolder = 'data'

def GetTargetConnection():
    try:
        connection = psycopg2.connect(database=targetDatabaseName, user=databaseUser, password=databaseUserPassword, host=databaseServer, port=databaseServerPort)
        return connection
    except:
        print("I am unable to connect to the database")
        return

def ImportRawDataCsvFile(connection, file):
    cur = connection.cursor()
    with open(file, 'r') as f:
        # Notice that we don't need the `csv` module.
        next(f)  # Skip the header row.
        cur.copy_from(f, rawDataTableName, sep=',', null='')
    connection.commit()

def ImportRawData(targetDirectory):
    for file in os.listdir( os.fsencode(str(targetDirectory))):
        filename = os.fsdecode(file)
        if filename.endswith(".csv") and filename.startswith("chicago_taxi_trips"): 
            print("Importing file " +  os.path.join(targetDirectory, filename))
            ImportRawDataCsvFile(connection, os.path.join(targetDirectory, filename))
            continue
        else:
            print("Import raw data: Skipping file " +  os.path.join(targetDirectory, filename))
            continue

def ReadJsonFile(targetDirectory):
    for file in os.listdir( os.fsencode(str(targetDirectory))):
        filename = os.fsdecode(file)
        if filename.endswith(".json") and filename.startswith("column_remapping"): 
            with open(os.path.join(targetDirectory,filename)) as f:
              return json.load(f)
        else:
            print("Import json: skipping file " +  os.path.join(targetDirectory, filename))
            continue

def ImportStringTupleData(tupleData, targetTableName, connection):
    cursor = connection.cursor()
    for dataEntry in tupleData:
        statement = "INSERT INTO " + targetTableName +" VALUES(" + dataEntry + ", '" + tupleData[dataEntry].translate(str.maketrans({"'":  r"''"}))  + "') " 
        cursor.execute(statement)
    connection.commit()

def ImportLocationTupleData(tupleData, targetTableName, connection):
    cursor = connection.cursor()
    for dataEntry in tupleData:
        statement = "INSERT INTO " + targetTableName +" VALUES(" + dataEntry + "," + tupleData[dataEntry] + ") " 
        cursor.execute(statement)
    connection.commit()

print("Starting import")

connection = GetTargetConnection()

dir_path = os.path.dirname(os.path.realpath(__file__))
directory = os.fsencode(str(dir_path))
print("Current directory: " + dir_path)
sourceFile = os.path.join(dir_path,zipSourceFile)
print("Zip source file: " + sourceFile)
zip_ref = zipfile.ZipFile(sourceFile, 'r')
targetDirectory = os.path.join(dir_path,extractFolder)
print("Extracting to target directory: " + targetDirectory)
zip_ref.extractall(targetDirectory)
zip_ref.close()

ImportRawData(targetDirectory)
jsonData = ReadJsonFile(targetDirectory)

ImportStringTupleData(jsonData['company'], companyNameTableName, connection)
ImportLocationTupleData(jsonData['dropoff_latitude'], dropoffLatitudeTableName, connection)
ImportLocationTupleData(jsonData['dropoff_longitude'], dropoffLongitudeTableName, connection)
ImportLocationTupleData(jsonData['pickup_latitude'], pickupLatitudeTableName, connection)
ImportLocationTupleData(jsonData['pickup_longitude'], pickupLongitudeTableName, connection)


print("Removing temporary folder: " + targetDirectory)
shutil.rmtree(targetDirectory)

print("Import finished")