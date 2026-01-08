import mysql.connector

def getConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="Learn"
    )