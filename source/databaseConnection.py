import mysql
import mysql.connector
import csv

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Database connection established successfully.")
        except Exception as error:
            print("Failed to connect to database:", error)

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as error:
            print("Failed to execute query:", error)
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed successfully.")


