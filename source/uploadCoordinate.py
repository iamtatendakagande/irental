import os
from source.databaseConnection import Database
import csv


class UploadFile:
    def __init__(self, file): 
        self.file = file

    def filePath(filename):
        currentdirpath = os.getcwd()  
        # get current working directory path
        filepath = os.path.join(currentdirpath, filename)
        return filepath
                    
    def upload(filepath):
        
        # Database Connection
        connection = Database(host="localhost", user="root", password="edmore1", database="irental")
        connection.connect()

        #open the csv file
        with open(filepath, 'rb') as csvfile:
            #read csv using reader class
            csv_reader = csv.reader(csvfile)
            #skip header
            header = next(csv_reader)
            #Read csv row wise and insert into table
            for row in csv_reader:
                #address = row[0].strip()
                #lat  = row[1].strip()
                #long = row[2].strip()

                sql = "INSERT INTO coordinates (name, mobile, email) VALUES (%s,%s,%s)"
                users =  connection.execute_query(sql, tuple(row))
                print("Record inserted")
    