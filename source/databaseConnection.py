import psycopg2

class Database:
    def __init__(self, host, user, password, dbname): # Renamed to avoid confusion
        self.host = host
        self.user = user
        self.password = password
        self.database = dbname # Use the new parameter name here
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.database  # Note: psycopg2 uses 'dbname'
            )
            print("PostgreSQL Database connection established successfully.")
        except Exception as error:
            print("Failed to connect to PostgreSQL database:", error)

    def populate(self, query, params=None):
        """For queries that modify data (INSERT, UPDATE, DELETE)"""
        if not self.connection:
            print("Not connected to the database.")
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit() 
            cursor.close()
            print("Query executed and changes committed.")
        except Exception as error:
            print("Failed to execute query:", error)
            self.connection.rollback() # Roll back changes on error
            return None
        
    def populates(self, query, data_list):
        """For queries that modify data (INSERT, UPDATE, DELETE)"""
        if not self.connection:
            print("Not connected to the database.")
            return
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, data_list)
            self.connection.commit() 
            cursor.close()
            print("Query executed and changes committed.")
        except Exception as error:
            print("Failed to execute query:", error)
            self.connection.rollback() # Roll back changes on error
            return None
        
    def posts(self, query, params=None):
        """For queries that fetch multiple rows (SELECT all)"""
        if not self.connection:
            print("Not connected to the database.")
            return None
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            self.connection.commit()
            cursor.close()
            return results
        except Exception as error:
            print("Failed to execute query:", error)
            return None
        
    def post(self, query):
        """For queries that fetch a single row (SELECT one)"""
        if not self.connection:
            print("Not connected to the database.")
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as error:
            print("Failed to execute query:", error)
            return None
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("PostgreSQL database connection closed successfully.")