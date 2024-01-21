import mysql.connector as mysql
import csv

class Database:
    def __init__(self): 
        conn = None

    def connect(conn):
        conn = mysql.connect(user='root', password='edmore1', host='localhost', database='irental')
        cursor = conn.cursor()
    
        try:
            conn = mysql.connect()
            cursor = conn.cursor(mysql.cursors.DictCursor)
            print("Connected")
        except Exception as e:
		    print(e)
        finally:
            cursor.close() 
            conn.close()