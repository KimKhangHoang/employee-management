"""connect_data.py - The file that connects to the database
   Author: Kim Khang Hoang
   Date created: 26/07/2023"""

import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch connection details from environment variables
driver = os.getenv('DB_DRIVER')
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
trusted_connection = os.getenv('DB_TRUSTED_CONNECTION')

# Build the connection string
connection_string = f"Driver={driver};Server={server};Database={database};Trusted_Connection={trusted_connection};"

# Establish connection
try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")
