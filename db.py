import pyodbc
from config import settings

def get_db():
    conn = pyodbc.connect(settings.SQL_CONNECTION_STRING)
    return conn
