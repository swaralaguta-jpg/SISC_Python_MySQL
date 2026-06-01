import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Kosongkan jika XAMPP default
        database="dbsisc"
    )