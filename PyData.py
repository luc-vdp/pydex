# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Data

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import libraries
import tkinter as tk
import tkinter.ttk as ttk
import pyodbc 
import pandas as pd
from PyTree import PyTree

#%% Main class
class PyData(ttk.Frame):
    def __init__(self, master = None, connectionString = None):
        # Define connection
        if connectionString is None:
            self.connectionString = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        else:
            self.connectionString = connectionString
            
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    #%% Actions to do when a treeview item is selected in the Query Tree
    def selectQuery(self, event):
        # Get selected tree item
        Id = self.treeviewQueries.Id
        
        # Get corresponding info from database
        self.connection = pyodbc.connect(self.connectionString)
        data = pd.io.sql.read_sql("Select A.*, B.ConnectionName, B.DatabaseId From Queries A, Connections B " +
                                  "Where A.ConnectionId = B.Id " + 
                                  "  And A.Id = " + Id, self.connection)
                    
        # Clear entries
        self.entryQueryName.delete(0, tk.END)

        if len(data.index) > 0:
            # Fill in Database
            if data.ConnectionName[0] is not None:
                self.DatabaseName.set(data.ConnectionName[0].strip())
            
            # Fill in Name
            if data.QueryName[0] is not None:
                self.entryQueryName.insert(0, data.QueryName[0].strip())
            
            # Fill in Query
            if data.SQL_Data[0] is not None:
                self.textQuery.insert(tk.END, data.SQL_Data[0].strip())
        
    #%% Actions to do when a treeview item is selected in the Query Tree
    def selectTable(self, event):
        # Get selected tree item
        Id = self.treeviewTablesAndViews.Id
        
        # Get corresponding info from database
        self.connection = pyodbc.connect(self.connectionString)
        data = pd.io.sql.read_sql("Select * From Tables Where Id = " + Id, self.connection)
        
        # Clear entries
        #self.entryQueryName.delete(0, tk.END)

        # Fill in Name
        #if data.QueryName[0] is not None:
        #    self.entryQueryName.insert(0, data.QueryName[0])

    #%% Create widgets
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make row 10 stretchable         
        self.rowconfigure(10, weight=1)

        # Make certain columns stretchable
        self.columnconfigure(1, weight=1)        
        self.columnconfigure(5, weight=4)        

        #%% LEFT
        # Tab control (notebook)
        self.notebookLeft = ttk.Notebook(self)
        self.notebookLeft.grid(row = 0, column = 0, rowspan=11, columnspan=2, sticky = tk.NE + tk.SW)
        
        # Queries tab page
        self.frameQueries = ttk.Frame(self.notebookLeft) 
        self.notebookLeft.add(self.frameQueries, text=' Queries ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameQueries.rowconfigure(0, weight=1)
        self.frameQueries.columnconfigure(0, weight=1)        
        # Queries Tree
        self.treeviewQueries = PyTree(self.frameQueries, connectionString=self.connectionString, table='Queries')
        self.treeviewQueries.grid(row = 0, column = 0, rowspan=11, sticky = tk.NE + tk.SW, padx =1, pady=1)
        # Define events
        self.frameQueries.bind('<<TreeviewSelect>>', self.selectQuery)

        # TablesAndViews tab page
        self.frameTablesAndViews = ttk.Frame(self.notebookLeft) 
        self.notebookLeft.add(self.frameTablesAndViews, text=' Tables & Views ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameTablesAndViews.rowconfigure(0, weight=1)
        self.frameTablesAndViews.columnconfigure(0, weight=1)        
        # TablesAndViews Tree
        self.treeviewTablesAndViews =PyTree(self.frameTablesAndViews, 
                                            connectionString=self.connectionString,
                                            table='Tables',
                                            filterColumn='DatabaseId',
                                            filterId='20')
        self.treeviewTablesAndViews.grid(row = 0, column = 0, rowspan=11, sticky = tk.NE + tk.SW, padx =1, pady=1)
        # Define events
        self.frameTablesAndViews.bind('<<TreeviewSelect>>', self.selectTable)

        # Show Settings ?
        self.showSettings = tk.IntVar() 
        self.showSettings.set(1)
        ttk.Checkbutton(self, text = "Settings", variable=self.showSettings).grid(row = 12, column = 0, sticky = tk.W, padx =5, pady=5)
        
        # Show Data ?
        self.showData = tk.IntVar() 
        self.showData.set(0)
        ttk.Checkbutton(self, text = "Data", variable=self.showData).grid(row = 12, column = 1, sticky = tk.W, padx =5, pady=5)

        #%% MIDDLE
        # Database
        self.DatabaseName = tk.StringVar()
        ttk.Label(self, text = "Database:").grid(row = 0, column = 2, sticky = tk.NE, padx =5, pady=5)
        self.buttonDatabase = ttk.Button(self, text = "Select database", textvariable=self.DatabaseName)
        self.buttonDatabase.grid(row = 0, column = 3, columnspan=4, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Query name
        ttk.Label(self, text = "Query:").grid(row=1, column=2, sticky=tk.E, padx=5, pady=0)
        self.entryQueryName = ttk.Entry(self)
        self.entryQueryName.grid(row=1, column=3, columnspan=4, sticky=tk.W + tk.E, padx=5, pady=0)
        ttk.Button(self, text = "Find...").grid(row=1, column=7, sticky=tk.W, padx=0, pady=0)
        
        # Last changed
        ttk.Label(self, text = "Last changed:").grid(row = 2, column = 2, sticky = tk.E, padx =5, pady=5)

        # Tab control (notebook)
        self.notebookMiddle = ttk.Notebook(self)
        self.notebookMiddle.grid(row = 3, column = 2, rowspan=8, columnspan=6, sticky = tk.NE + tk.SW)      

        #  Query tab page
        self.frameQuery = ttk.Frame(self.notebookMiddle) 
        self.notebookMiddle.add(self.frameQuery, text=' Query ', sticky=tk.NW + tk.SE)
        
        #  Make row and column stretchable         
        self.frameQuery.rowconfigure(1, weight=1)
        self.frameQuery.columnconfigure(0, weight=1)        
        
        #  Query Text
        self.textParameterQuery = tk.Text(self.frameQuery, height=4)
        self.textParameterQuery.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)

        #  Query Text
        self.textQuery = tk.Text(self.frameQuery)
        self.textQuery.grid(row = 1, column = 0, rowspan=12, sticky = tk.NE + tk.SW, padx =1, pady=1)

        #  Columns tab page
        self.frameColumns = ttk.Frame(self.notebookMiddle) 
        self.notebookMiddle.add(self.frameColumns, text=' Columns ', sticky=tk.NW + tk.SE)
        #  Make row and column stretchable         
        self.frameColumns.rowconfigure(0, weight=1)
        self.frameColumns.columnconfigure(0, weight=1)        
        #  Columns table
        #...

        #  Tables tab page
        self.frameTables = ttk.Frame(self.notebookMiddle) 
        self.notebookMiddle.add(self.frameTables, text=' Tables ', sticky=tk.NW + tk.SE)
        #  Make row and column stretchable         
        self.frameTables.rowconfigure(0, weight=1)
        self.frameTables.columnconfigure(0, weight=1)        
        #  Tables list
        #...

        #  Views tab page
        self.frameViews = ttk.Frame(self.notebookMiddle) 
        self.notebookMiddle.add(self.frameViews, text=' Views ', sticky=tk.NW + tk.SE)
        #  Make row and column stretchable         
        self.frameViews.rowconfigure(0, weight=1)
        self.frameViews.columnconfigure(0, weight=1)        
        #  Views list
        #...
        
        #%% RIGHT
        # Auto fetch parameters checkbox
        self.autoFetchParameters = tk.IntVar() 
        self.autoFetchParameters.set(1)       
        ttk.Checkbutton(self, text='Auto fetch parameters', variable=self.autoFetchParameters).grid(row = 0, column = 10, columnspan=2, sticky = tk.W, padx =5, pady=5)
        
        ttk.Button(self, text='Guess').grid(row = 0, column = 12, sticky = tk.W, padx =5, pady=5)
        
        # Show Parameters
        self.showParameters = tk.IntVar() 
        self.showParameters.set(0)
        ttk.checkboxShowParameters = ttk.Checkbutton(self, text='Show parameters', variable=self.showParameters).grid(row = 1, column = 10, columnspan=2, sticky = tk.W, padx =5, pady=0)
        
        # Parameters
        ttk.Label(self, text = "Parameters come here").grid(row = 3, column = 8, columnspan=3, sticky = tk.NW+tk.SE, padx =5, pady=5)
        
        #%% BOTTOM
        ttk.Button(self, text = "Run").grid(row = 12, column = 2, sticky = tk.W, padx =5, pady=5)
        ttk.Button(self, text = "Save").grid(row = 12, column = 3, sticky = tk.W, padx =5, pady=5)
        ttk.Button(self, text = "Save as...").grid(row = 12, column = 4, sticky = tk.W, padx =5, pady=5)

        ttk.Label(self, text = "Variable").grid(row = 12, column = 6, sticky = tk.W, padx =5, pady=5)
        ttk.Entry(self, text = "d").grid(row = 12, column = 7, sticky = tk.W, padx =5, pady=5)
        ttk.Button(self, text = "Excel").grid(row = 12, column = 11, sticky = tk.E, padx =5, pady=5)
        ttk.Button(self, text = "Python").grid(row = 12, column = 12, sticky = tk.W, padx =5, pady=5)

#%% Allow the class to run stand-alone.
if __name__ == "__main__":
    PyData().mainloop()

