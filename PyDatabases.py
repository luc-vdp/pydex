# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import libraries
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import pyodbc 
import pandas as pd
from PyTree import PyTree
import getpass
import datetime
import database
    
#%% Main Class
class PyDatabases(ttk.Frame):
    def __init__(self, master = None, connectionString = None):        
#        # setup custom exception handling
#        self.report_callback_exception = self.handle_exception

        # Define connection
        if connectionString is None:
            self.connectionString = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        else:
            self.connectionString = connectionString

        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

#    # Callback function - Handle exceptions
#    def handle_exception(exception, value, traceback):
#        messagebox.showinfo('Error',value)

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
        
        # Fill in Id
        if data.Id[0] is not None:
            self.Id.set(data.Id[0])
        
        # Fill in Name
        if data.ConnectionName[0] is not None:
            self.entryName.insert(0, data.ConnectionName[0].strip())
        
        # Fill in Driver
        if data.Driver[0] is not None:
            self.comboboxDriver.insert(0, data.Driver[0].strip())
        
        # Fill in Server
        if data.Server[0] is not None:
            self.entryServer.insert(0, data.Server[0].strip())
        
        # Fill in Database
        if data.Database[0] is not None:
            self.entryDatabase.insert(0, data.Database[0].strip())

        # Fill in Username
        if data.User[0] is not None:
            self.entryUsername.insert(0, data.User[0].strip())
            
        if data.User[0].strip() == '':
            self.windowsSecurity.set(1)
        else:
            self.windowsSecurity.set(0)
        self.changeWindowsSecurity()
        
        # Fill in Password
        if data.Password[0] is not None:
            self.entryPassword.insert(0, data.Password[0].strip())
            
        # Fill in DatabaseId
        if data.DatabaseId[0] is not None:
            self.entryDatabaseId.insert(0, data.DatabaseId[0])
            
        # Fill in LastUpdated
        if data.TimeChanged[0] is not None:
            self.LastUpdated.set(str(data.TimeChanged[0])[:-7] + ' by ' + data.UserId[0])

        # Fill in Description
        if data.Description[0] is not None:
            self.textDescription.insert(1.0, data.Description[0].strip())
        else:
            self.textDescription.insert(1.0, '')
      
    def changeWindowsSecurity(self):
        if self.windowsSecurity.get() == 1:
            self.labelUsername.grid_forget()
            self.entryUsername.grid_forget()
            self.labelPassword.grid_forget()
            self.entryPassword.grid_forget()
        else:
            self.labelUsername.grid(row = 6, column = 1, sticky = tk.E, padx =5, pady=5)
            self.entryUsername.grid(row = 6, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
            self.labelPassword.grid(row = 7, column = 1, sticky = tk.E, padx =5, pady=5)
            self.entryPassword.grid(row = 7, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
            
    def showListbox(self):
        if self.showDependents.get() == 'Hide':
            self.listbox.grid_forget()
        else:
            self.listbox.grid(row = 1, column = 3, rowspan=10, columnspan=4, sticky = tk.NW+tk.SE, padx =5, pady=5)
    
    def testConnection(self):
        try:
            if self.entryUsername.get().strip() == '':
                connectionString = 'DRIVER={' + self.comboboxDriver.get().strip() + '};Server=' + self.entryServer.get().strip() + ';Database=' + self.entryDatabase.get().strip() + ';Trusted_Connection=yes;'
            else:
                connectionString = 'DRIVER={' + self.comboboxDriver.get().strip() + '};Server=' + self.entryServer.get().strip() + ';Database=' + self.entryDatabase.get().strip() + ';UID=' + self.entryUsername.get().strip() + ';PWD=' + self.entryPassword.get().strip()
                                      
            pyodbc.connect(connectionString)
            
            messagebox.showinfo(message="Test connection succeeded")
        except pyodbc.Error as ex: 
            messagebox.showerror("Test connection failed", "ConnectionString:\n" + connectionString + "\n\nError:\n" + ex.args[1])
        
    def save(self):
        # Write update query
        query = ("UPDATE [dbo].[Connections] " +
                 "SET [ConnectionName] = '" + self.entryName.get()       + "' " +
                 "   ,[Driver]         = '" + self.comboboxDriver.get()  + "' " +
                 "   ,[Server]         = '" + self.entryServer.get()     + "' " +
                 "   ,[Database]       = '" + self.entryDatabase.get()   + "' " +
                 "   ,[User]           = '" + self.entryUsername.get()   + "' " +
                 "   ,[Password]       = '" + self.entryPassword.get()   + "' " +
                 "   ,[DatabaseId]     =  " + self.entryDatabaseId.get() + "  " +
                 "   ,[Description]    = '" + self.textDescription.get(1.0, tk.END).strip() + "' " +
                 "   ,[UserId]         = '" + getpass.getuser()         + "' " +
                 "   ,[TimeChanged]    = '" + str(datetime.datetime.now()) + "' " +
                 " WHERE Id = " + self.Id.get())
        
        # Execute update query
        database.setData(self.connectionString, query)
            
        # Refresh the tree
        self.treeview.refreshTree(id=self.Id.get())
                
    #%% Create widgets
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make row 10 stretchable         
        self.rowconfigure(11, weight=1)

        # Make certain columns stretchable
        self.columnconfigure(0, weight=2)        
        self.columnconfigure(2, weight=4)        
        self.columnconfigure(3, weight=1)        
        self.columnconfigure(4, weight=1)        
        self.columnconfigure(5, weight=1)        
        self.columnconfigure(6, weight=1)        

        #%% LEFT
        # Tree
        self.treeview = PyTree(self, connectionString=self.connectionString, table='Connections')
        
        # Define events
        self.bind('<<TreeviewSelect>>', self.selectItem)

        self.treeview.grid(row = 0, column = 0, rowspan=13, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        #%% MIDDLE
        # Id
        ttk.Label(self, text = "Id:").grid(row = 0, column = 1, sticky = tk.NE, padx =5, pady=5)
        self.Id = tk.StringVar()
        self.labelId = ttk.Label(self, textvariable=self.Id)
        self.labelId.grid(row = 0, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Name
        ttk.Label(self, text = "Name:").grid(row = 1, column = 1, sticky = tk.NE, padx =5, pady=5)
        self.entryName = ttk.Entry(self)
        self.entryName.grid(row = 1, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Driver
        ttk.Label(self, text = "Driver:").grid(row = 2, column = 1, sticky = tk.E, padx =5, pady=5)
        self.comboboxDriver = ttk.Combobox(self)
        self.comboboxDriver.grid(row = 2, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Server
        ttk.Label(self, text = "Server:").grid(row = 3, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryServer = ttk.Entry(self)
        self.entryServer.grid(row = 3, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Database
        ttk.Label(self, text = "Database:").grid(row = 4, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryDatabase = ttk.Entry(self)
        self.entryDatabase.grid(row = 4, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Windows security
        self.windowsSecurity = tk.IntVar()
        self.checkbuttonWindowsSecurity = ttk.Checkbutton(self, text = "Windows security", variable=self.windowsSecurity, command=self.changeWindowsSecurity)
        self.checkbuttonWindowsSecurity.grid(row = 5, column = 2, sticky = tk.W, padx =5, pady=5)
        
        # Username
        self.labelUsername = ttk.Label(self, text = "Username:")
        self.labelUsername.grid(row = 6, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryUsername = ttk.Entry(self)
        self.entryUsername.grid(row = 6, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Password
        self.labelPassword = ttk.Label(self, text = "Password:")
        self.labelPassword.grid(row = 7, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryPassword = ttk.Entry(self)
        self.entryPassword.grid(row = 7, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # DatabaseId
        ttk.Label(self, text = "DatabaseId:").grid(row = 8, column = 1, sticky = tk.E, padx =5, pady=5)
        self.entryDatabaseId = ttk.Entry(self)
        self.entryDatabaseId.grid(row = 8, column = 2, sticky = tk.W, padx =5, pady=5)
        
        # Last updated
        ttk.Label(self, text = "Last updated:").grid(row = 9, column = 1, sticky = tk.E, padx =5, pady=5)
        self.LastUpdated = tk.StringVar()
        self.labelLastUpdated = ttk.Label(self, text = "-", textvariable=self.LastUpdated)
        self.labelLastUpdated.grid(row = 9, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Description
        ttk.Label(self, text = "Description:").grid(row = 10, column = 1, sticky = tk.NE, padx =5, pady=5)
        self.textDescription = tk.Text(self, height=5, width=50)
        self.textDescription.grid(row = 10, column = 2, sticky = tk.W + tk.E, padx =5, pady=5)
        
        # Buttons
        ttk.Button(self, text = "Test", command=self.testConnection).grid(row = 11, column = 2, sticky = tk.NW, padx =5, pady=5)
        ttk.Button(self, text = "Save", command=self.save).grid(row = 11, column = 2, sticky = tk.NE, padx =5, pady=5)
        
        #%% RIGHT
        # Show/Hide listbox
        self.showDependents = tk.StringVar()
        self.showDependents.set('Hide')
        
        # Hide/Tables/Views/Queries
        ttk.Radiobutton(self, text = "Hide", variable=self.showDependents, value='Hide', command=self.showListbox).grid(row = 0, column = 3, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text = "Tables", variable=self.showDependents, value='Tables', command=self.showListbox).grid(row = 0, column = 4, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text = "Views", variable=self.showDependents, value='Views', command=self.showListbox).grid(row = 0, column = 5, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text = "Queries", variable=self.showDependents, value='Queries', command=self.showListbox).grid(row = 0, column = 6, sticky = tk.W, padx =5, pady=5)
        
        # TabControl
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row = 1, column = 3, rowspan=10, columnspan=4, sticky = tk.NW+tk.SE, padx =5, pady=5)
        self.listbox.grid_forget()
    

# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyDatabases().mainloop()

