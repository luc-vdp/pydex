# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Data

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import libraries
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import simpledialog
import pyodbc 
import pandas as pd
from PyTree import PyTree
from PyParameters import PyParameters
from PyTable import PyTable
from tkinter.scrolledtext import ScrolledText
import database
import sys

#%% Main class
class PyData(ttk.Frame):
    def __init__(self, master = None, connectionString = None):
        # Define connection to the meta data
        if connectionString is None:
            self.connectionStringMeta = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        else:
            self.connectionStringMeta = connectionString
            
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    #%% Actions to do when a treeview item is selected in the Query Tree
    def selectQuery(self, event):
        # Get selected tree item
        Id = self.treeviewQueries.Id
        
        # Get corresponding info from database
        self.connectionMeta = pyodbc.connect(self.connectionStringMeta)
        data = pd.io.sql.read_sql("Select A.*, B.ConnectionName, B.DatabaseId, " +
                                  "       CASE WHEN B.[User] = '' THEN 'DRIVER={' + Rtrim(B.Driver) + '};Server=' + Rtrim(B.Server) + ';Database=' + Rtrim(B.[Database]) + ';Trusted_Connection=yes;' "
                                  "             ELSE 'DRIVER={' + Rtrim(B.Driver) + '};Server=' + Rtrim(B.Server) + ';Database=' + Rtrim(B.[Database]) + ';UID=' + Rtrim(B.[User]) + ';PWD=' + Rtrim(B.[Password]) END As ConnectionString "           
                                  "From Queries A, Connections B " +
                                  "Where A.ConnectionId = B.Id " + 
                                  "  And A.Id = " + Id, self.connectionMeta)
                    
        # Clear entries
        self.entryQueryName.delete(0, tk.END)
        self.textParameterQuery.delete(1.0, tk.END)
        self.textQuery.delete(1.0, tk.END)

        if len(data.index) > 0:
            # Fill in Database
            if data.ConnectionName[0] is not None:
                self.DatabaseName.set(data.ConnectionName[0].strip())
            
            # Fill in Name
            if data.QueryName[0] is not None:
                self.entryQueryName.insert(0, data.QueryName[0].strip())
            
            # Fill in ParameterQuery
            if data.SQL_Parameters[0] is not None:
                self.textParameterQuery.insert(tk.END, data.SQL_Parameters[0].strip())
        
            # Fill in Query
            if data.SQL_Data[0] is not None:
                self.textQuery.insert(tk.END, data.SQL_Data[0].strip())

            self.connectionStringData = data.ConnectionString[0]
            #print(self.connectionStringData)
            
    def findQuery(self):         
         # Ask new text
        queryName = simpledialog.askstring("Find query", "Query name?", initialvalue=self.entryQueryName.get(), parent=self)
        
        
    #%% Actions to do when a treeview item is selected in the Query Tree
#    def editQuery(self, event):
#        # Get selected tree item
#        Id = self.treeviewQueries.Id
        
    #%% Run the query
    def runQuery(self, event=None):
        # Get query
        self.query = self.textQuery.get(1.0,tk.END)
        # Define global variable
        global data 
        # Try to get the data       
        try:
            data = database.getData(self.connectionStringData,self.query)
            # Fill the table
            self.pyTable.addDataframe(dataframe = data)
            # Show the table
            self.checkData.set(1)
            self.showData()
        except:  
            messagebox.showerror("getData failed", sys.exc_info()[1])
        
    #%% Actions to do when a treeview item is selected in the Query Tree
    def selectTable(self, event):
        # Get selected tree item
        Id = self.treeviewTablesAndViews.Id
        
        # Get corresponding info from database
        self.connectionMeta = pyodbc.connect(self.connectionStringMeta)
        data = pd.io.sql.read_sql("Select * From Tables Where Id = " + Id, self.connectionMeta)
        
        # Clear entries
        #self.entryQueryName.delete(0, tk.END)

        # Fill in Name
        #if data.QueryName[0] is not None:
        #    self.entryQueryName.insert(0, data.QueryName[0])

    # Show or hide the table
    def showParameters(self):
        if self.checkboxParameters.get() == 1:
            self.Parameters.grid(row=2, column=0, sticky=tk.NW + tk.SE)
        else:
            self.Parameters.grid_forget()
        
    # Show or hide the settings (query, ...)
    def showSettings(self):
        if self.checkSettings.get() == 1:
            if self.checkData.get() == 1:
                self.notebookMiddle.grid(row = 3, column = 2, rowspan=2, columnspan=11, sticky = tk.NE + tk.SW)
                self.pyTable.grid(row=5, column=2, columnspan=11, sticky=tk.NW + tk.SE)
            else:
                self.notebookMiddle.grid(row = 3, column = 2, rowspan=2, columnspan=11, sticky = tk.NE + tk.SW)
                self.pyTable.grid_forget()
        else:
            self.notebookMiddle.grid_forget()
            if self.checkData.get() == 1:
                self.pyTable.grid(row=3, column=2, rowspan=2, columnspan=11, sticky=tk.NW + tk.SE)
            else:
                self.pyTable.grid_forget()
        
    # Show or hide the data table
    def showData(self):
        self.showSettings()
        
    def createPythonData(self):
#        eval("global " + self.pythonVar.get())
#        eval(self.pythonVar.get() + " = self.pyTable.data")
#        messagebox.showinfo("Info","pandas dataframe saved as " + self.pythonVar.get())
        global df 
        df = self.pyTable.data
        messagebox.showinfo("Info","pandas dataframe saved as " + self.pythonVar.get())
        
        
    #%% Create widgets
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make row 4 stretchable         
        self.rowconfigure(4, weight=1)

        # Make certain columns stretchable
        #self.columnconfigure(1, weight=1)        
        self.columnconfigure(5, weight=4)        

        #%% LEFT
        # Tab control (notebook)
        self.notebookLeft = ttk.Notebook(self)
        self.notebookLeft.grid(row = 0, column = 0, rowspan=7, columnspan=2, sticky = tk.NE + tk.SW)
        
        # Queries tab page
        self.frameQueries = ttk.Frame(self.notebookLeft) 
        self.notebookLeft.add(self.frameQueries, text=' Queries ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameQueries.rowconfigure(0, weight=1)
        self.frameQueries.columnconfigure(0, weight=1)               
        # Queries Tree
        self.treeviewQueries = PyTree(self.frameQueries, 
                                      connectionString=self.connectionStringMeta, 
                                      table='Queries')
        self.treeviewQueries.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        # Define events
        self.frameQueries.bind('<<TreeviewSelect>>', self.selectQuery)
        self.frameQueries.bind('<<Double-Button-1>>', self.runQuery)
        #self.frameQueries.bind('<<TreeviewEdit>>', self.editQuery)
        #self.frameQueries.bind('<<TreeviewRename>>', self.renameQuery)

        # TablesAndViews tab page
        self.frameTablesAndViews = ttk.Frame(self.notebookLeft) 
        self.notebookLeft.add(self.frameTablesAndViews, text=' Tables & Views ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameTablesAndViews.rowconfigure(0, weight=1)
        self.frameTablesAndViews.columnconfigure(0, weight=1)        
        # TablesAndViews Tree
        self.treeviewTablesAndViews =PyTree(self.frameTablesAndViews, 
                                            connectionString=self.connectionStringMeta,
                                            table='Tables',
                                            filterColumn='DatabaseId',
                                            filterId='20')
        self.treeviewTablesAndViews.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        # Define events
        self.frameTablesAndViews.bind('<<TreeviewSelect>>', self.selectTable) # TO be corrected ?

        # Show Parameters
        self.checkboxParameters = tk.IntVar() 
        self.checkboxParameters.set(0)
        self.checkboxShowParameters = ttk.Checkbutton(self.frameQueries, text='Show parameters', variable=self.checkboxParameters, command=self.showParameters)
        self.checkboxShowParameters.grid(row = 1, column = 0, columnspan=4, sticky = tk.W, padx =2, pady=2)
        
        # Parameters table
        self.Parameters = PyParameters(self.frameQueries, connectionString=self.connectionStringMeta)
        self.Parameters.grid(row = 2, column = 0, columnspan=4, sticky = tk.NE + tk.SW)
        self.Parameters.grid_forget()
        
        # Show Settings ?
        self.checkSettings = tk.IntVar() 
        self.checkSettings.set(1)
        ttk.Checkbutton(self, text = "Settings", variable=self.checkSettings, command=self.showSettings).grid(row = 12, column = 0, sticky = tk.W, padx =5, pady=5)
        
        # Show Data ?
        self.checkData = tk.IntVar() 
        self.checkData.set(0)
        ttk.Checkbutton(self, text = "Data", variable=self.checkData, command=self.showData).grid(row = 12, column = 1, sticky = tk.W, padx =5, pady=5)

        #%% MIDDLE
        # Database
        self.DatabaseName = tk.StringVar()
        styleLeftAligned = ttk.Style()
        styleLeftAligned.configure('LeftAligned.TButton', foreground='maroon', justify=tk.LEFT)
        ttk.Label(self, text = "Database:").grid(row = 0, column = 2, sticky = tk.NE, padx =5, pady=5)
        self.buttonDatabase = ttk.Button(self, text = "Select database", textvariable=self.DatabaseName, style='LeftAligned.TButton')
        self.buttonDatabase.grid(row = 0, column = 3, columnspan=4, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Query name
        ttk.Label(self, text = "Query:").grid(row=1, column=2, sticky=tk.E, padx=5, pady=0)
        self.entryQueryName = ttk.Entry(self)
        self.entryQueryName.grid(row=1, column=3, columnspan=4, sticky=tk.W + tk.E, padx=5, pady=0)
        ttk.Button(self, text = "Find...", command=self.findQuery).grid(row=1, column=7, sticky=tk.W, padx=0, pady=0)
        
        # Last changed
        ttk.Label(self, text = "Last changed:").grid(row = 2, column = 2, sticky = tk.E, padx =5, pady=5)

        # Tab control (notebook)
        self.notebookMiddle = ttk.Notebook(self)
        self.notebookMiddle.grid(row = 3, column = 2, rowspan=2, columnspan=11, sticky = tk.NE + tk.SW)      

        #  Query tab page
        self.frameQuery = ttk.Frame(self.notebookMiddle) 
        self.notebookMiddle.add(self.frameQuery, text=' Query ', sticky=tk.NW + tk.SE)
        
        #  Make row and column stretchable         
        self.frameQuery.rowconfigure(1, weight=1)
        self.frameQuery.columnconfigure(0, weight=1)        
        
        #  ParameterQuery 
        self.textParameterQuery = ScrolledText(self.frameQuery, height=4)
        self.textParameterQuery.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)

        #  Query 
        self.textQuery = ScrolledText(self.frameQuery, height=20)
        self.textQuery.grid(row = 1, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)

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
        ttk.Checkbutton(self, text='Auto fetch parameters', variable=self.autoFetchParameters).grid(row = 0, column = 10, columnspan=2, sticky = tk.E, padx =5, pady=5)
        
        ttk.Button(self, text='Guess').grid(row = 0, column = 12, sticky = tk.W, padx =5, pady=5)
        
        #%% BOTTOM
        #ScrolledText(self, height=3).grid(row=5, column=0, columnspan=13, sticky=tk.NW + tk.SE)

        self.pyTable = PyTable(self)
        self.pyTable.grid(row=5, column=2, columnspan=11, sticky=tk.NW + tk.SE)
        self.pyTable.grid_forget()
        
        ttk.Button(self, text = "Run", command=self.runQuery).grid(row = 12, column = 2, sticky = tk.W, padx =5, pady=5)
        ttk.Button(self, text = "Save").grid(row = 12, column = 3, sticky = tk.W, padx =5, pady=5)
        ttk.Button(self, text = "Save as...").grid(row = 12, column = 4, sticky = tk.W, padx =5, pady=5)

        ttk.Label(self, text = "Variable").grid(row = 12, column = 6, sticky = tk.W, padx =5, pady=5)
        self.pythonVar = tk.StringVar()
        self.pythonVar.set('d')
        ttk.Entry(self, textvariable=self.pythonVar).grid(row = 12, column = 7, sticky = tk.W, padx =5, pady=5)

        ttk.Button(self, text = "Excel").grid(row = 12, column = 11, sticky = tk.E, padx =5, pady=5)
        ttk.Button(self, text = "Python", command=self.createPythonData).grid(row = 12, column = 12, sticky = tk.W, padx =5, pady=5)

#%% Allow the class to run stand-alone.
if __name__ == "__main__":
    PyData().mainloop()

