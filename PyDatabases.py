# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import statements
import tkinter as tk
import tkinter.ttk as ttk
import pyodbc 
import pandas as pd
from PyTree import PyTree

#%% Class definition
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

    # Actions to do when a treeview item is selected
    def selectItem(self, event):
        # Get selected tree item
        Id = self.treeview.Id
        # Get corresponding info from database
        self.connection = pyodbc.connect(self.connectionString)
        data = pd.io.sql.read_sql("Select * From Connections Where Id = " + Id, self.connection)
        # Fill in Name
        self.entryName.delete(0, tk.END)
        if data.ConnectionName[0] is not None:
            self.entryName.insert(0, data.ConnectionName[0])
        # Fill in Server
        self.entryServer.delete(0, tk.END)
        if data.Server[0] is not None:
            self.entryServer.insert(0, data.Server[0])
        # Fill in Database
        self.entryDatabase.delete(0, tk.END)
        if data.Database[0] is not None:
            self.entryDatabase.insert(0, data.Database[0])
        
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
#        self.treeview = ttk.Treeview(self)
#        self.treeview.grid(row = 0, column = 0, rowspan=13, sticky = tk.NE + tk.SW, padx =1, pady=1)
#        self.treeview['show'] = 'tree'
#        # Get tree data from database        
#        treedata = pd.io.sql.read_sql("Select * From Connections Where Status = 'A' Order By [Level], Nr", self.connection)
#        # Fill tree
#        for i in treedata.index:
#            if i==0:
#                self.treeview.insert('', treedata.Nr[i]-1, iid=treedata.Id[i], text=treedata.Title[i].strip())
#            else:
#                self.treeview.insert(treedata.ParentId[i], treedata.Nr[i]-1, iid=treedata.Id[i], text=treedata.Title[i].strip())
        
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
        ttk.Combobox(self).grid(row = 1, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
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
        ttk.Checkbutton(self, text = "Windows security", variable=self.windowsSecurity).grid(row = 4, column = 2, sticky = tk.W, padx =5, pady=5)
        # Username
        ttk.Label(self, text = "Username:").grid(row = 5, column = 1, sticky = tk.E, padx =5, pady=5)
        ttk.Entry(self).grid(row = 5, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        # Password
        ttk.Label(self, text = "Password:").grid(row = 6, column = 1, sticky = tk.E, padx =5, pady=5)
        ttk.Entry(self).grid(row = 6, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        # DatabaseId
        ttk.Label(self, text = "DatabaseId:").grid(row = 7, column = 1, sticky = tk.E, padx =5, pady=5)
        ttk.Entry(self).grid(row = 7, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        # Last updated
        ttk.Label(self, text = "Last updated:").grid(row = 8, column = 1, sticky = tk.E, padx =5, pady=5)
        ttk.Label(self, text = "-").grid(row = 8, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        # Description
        ttk.Label(self, text = "Description:").grid(row = 9, column = 1, sticky = tk.NE, padx =5, pady=5)
        tk.Text(self, height=5, width=50).grid(row = 9, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
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

