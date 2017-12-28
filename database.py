# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Tree

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import libraries
import pyodbc
import pandas as pd

def getData(connectionString, query):
    # Connect to the database
    connection = pyodbc.connect(connectionString)
    
    # Run the select query
    data = pd.io.sql.read_sql(query, connection)
    return data

    # Close the connection to the database
    connection.close()
        
def setData(connectionString, query):
    # Connect to the database
    connection = pyodbc.connect(connectionString)

    # Execute the query
    pd.io.sql.execute(query, connection)

    # Commit changes
    connection.commit()

    # Close the connection to the database
    connection.close()

