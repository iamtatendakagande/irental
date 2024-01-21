import mysql.connector as mysql
import csv

class UploadFile:
    def __init__(self, file): 
        self.file = file

    def upload(file):
        #open the csv file
        with open('users.csv', mode='r') as csv_file:
            #read csv using reader class
            csv_reader = csv.reader(csv_file)
            #skip header
            header = next(csv_reader)
            #Read csv row wise and insert into table
            for row in csv_reader:
                sql = "INSERT INTO users (name, mobile, email) VALUES (%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
    