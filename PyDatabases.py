# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import libraries
import tkinter as tk
import tkinter.ttk as ttk
import pyodbc 
import pandas as pd
from PyTree import PyTree

#%% Main Class
class PyDatabases(ttk.Frame):

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

    #%% Actions to do when a treeview item is selected
    def selectItem(self, event):
        # Get selected tree item
        Id = self.treeview.Id
        
        # Get corresponding info from database
        self.connection = pyodbc.connect(self.connectionString)
        data = pd.io.sql.read_sql("Select * From Connections Where Id = " + Id, self.connection)
        
        # Clear entries
        self.entryName.delete(0, tk.END)
        self.comboboxDriver.delete(0, tk.END)
        self.entryServer.delete(0, tk.END)
        self.entryDatabase.delete(0, tk.END)
        #self.windowsSecurity = 1
        self.entryUsername.delete(0, tk.END)
        self.entryPassword.delete(0, tk.END)
        self.entryDatabaseId.delete(0, tk.END)
        #self.labelLastUpdated.delete(0, tk.END)
        #self.textDescription.delete(0, tk.END)
        
        # Fill in Name
        if data.ConnectionName[0] is not None:
            self.entryName.insert(0, data.ConnectionName[0])
        
        # Fill in Driver
        if data.Driver[0] is not None:
            self.comboboxDriver.insert(0, data.Driver[0])
        
        # Fill in Server
        if data.Server[0] is not None:
            self.entryServer.insert(0, data.Server[0])
        
        # Fill in Database
        if data.Database[0] is not None:
            self.entryDatabase.insert(0, data.Database[0])

        # Fill in Username
        if data.User[0] is not None:
            self.entryUsername.insert(0, data.User[0])
            
        if data.User[0].strip() == '':
            self.windowsSecurity.set(1)
        else:
            self.windowsSecurity.set(0)
                
        # Fill in Password
        if data.Password[0] is not None:
            self.entryPassword.insert(0, data.Password[0])
            
        # Fill in DatabaseId
        if data.DatabaseId[0] is not None:
            self.entryDatabaseId.insert(0, data.DatabaseId[0])
            
        # Fill in LastUpdated
#        if data.TimeChanged[0] is not None:
#            self.labelLastUpdated.insert(0, data.TimeChanged[0] + ' by ' + data.UserId[0])

        # Fill in Description
#        if data.Description[0] is not None:
#            self.textDescription.insert(0, data.Description[0])
      
    def changeWindowsSecurity(self):
        if self.windowsSecurity.get() == 1:
            self.entryUsername.grid_forget()
            self.entryPassword.grid_forget()
        else:
            self.entryUsername.grid()
            self.entryPassword.grid()
            
        
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
        self.columnconfigure(0, weight=2)        
        self.columnconfigure(2, weight=4)        
        self.columnconfigure(3, weight=1)        
        self.columnconfigure(4, weight=1)        
        self.columnconfigure(5, weight=1)        
        self.columnconfigure(6, weight=1)        

        # Tree
        self.treeview = PyTree(self, connectionString=self.connectionString, table='Connections')
        
        # Define events
        self.bind('<<TreeviewSelect>>', self.selectItem)

        self.treeview.grid(row = 0, column = 0, rowspan=13, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Name
        ttk.Label(self, text = "Name:").grid(row = 0, column = 1, sticky = tk.NE, padx =5, pady=5)
        self.entryName = ttk.Entry(self)
        self.entryName.grid(row = 0, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Driver
        ttk.Label(self, text = "Driver:").grid(row = 1, column = 1, sticky = tk.E, padx =5, pady=5)
        self.comboboxDriver = ttk.Combobox(self)
        self.comboboxDriver.grid(row = 1, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Server
        ttk.Label(self, text = "Server:").grid(row = 2, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryServer = ttk.Entry(self)
        self.entryServer.grid(row = 2, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Database
        ttk.Label(self, text = "Database:").grid(row = 3, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryDatabase = ttk.Entry(self)
        self.entryDatabase.grid(row = 3, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Windows security
        self.windowsSecurity = tk.IntVar()
        self.checkbuttonWindowsSecurity = ttk.Checkbutton(self, text = "Windows security", variable=self.windowsSecurity, command=self.changeWindowsSecurity)
        self.checkbuttonWindowsSecurity.grid(row = 4, column = 2, sticky = tk.W, padx =5, pady=5)
        
        # Username
        ttk.Label(self, text = "Username:").grid(row = 5, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryUsername = ttk.Entry(self)
        self.entryUsername.grid(row = 5, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Password
        ttk.Label(self, text = "Password:").grid(row = 6, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryPassword = ttk.Entry(self)
        self.entryPassword.grid(row = 6, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # DatabaseId
        ttk.Label(self, text = "DatabaseId:").grid(row = 7, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryDatabaseId = ttk.Entry(self)
        self.entryDatabaseId.grid(row = 7, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Last updated
        ttk.Label(self, text = "Last updated:").grid(row = 8, column = 1, sticky = tk.E, padx =5, pady=5)
        self.labelLastUpdated = ttk.Label(self, text = "-")
        self.labelLastUpdated.grid(row = 8, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Description
        ttk.Label(self, text = "Description:").grid(row = 9, column = 1, sticky = tk.NE, padx =5, pady=5)
        self.textDescription = tk.Text(self, height=5, width=50)
        self.textDescription.grid(row = 9, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Buttons
        ttk.Button(self, text = "Test").grid(row = 10, column = 2, sticky = tk.NW, padx =5, pady=5)
        ttk.Button(self, text = "Save").grid(row = 10, column = 2, sticky = tk.NE, padx =5, pady=5)
        
        # Show/Hide listbox
        self.showDependents = tk.StringVar()
        self.showDependents.set('Hide')
        def showListbox():
            if self.showDependents.get() == 'Hide':
                self.listbox.grid_forget()
            else:
                self.listbox.grid(row = 1, column = 3, rowspan=10, columnspan=4, sticky = tk.NW+tk.SE, padx =5, pady=5)

        # Hide/Tables/Views/Queries
        ttk.Radiobutton(self, text = "Hide", variable=self.showDependents, value='Hide', command=showListbox).grid(row = 0, column = 3, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text = "Tables", variable=self.showDependents, value='Tables', command=showListbox).grid(row = 0, column = 4, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text = "Views", variable=self.showDependents, value='Views', command=showListbox).grid(row = 0, column = 5, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text = "Queries", variable=self.showDependents, value='Queries', command=showListbox).grid(row = 0, column = 6, sticky = tk.W, padx =5, pady=5)
        
        # TabControl
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row = 1, column = 3, rowspan=10, columnspan=4, sticky = tk.NW+tk.SE, padx =5, pady=5)
        self.listbox.grid_forget()
    

# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyDatabases().mainloop()

