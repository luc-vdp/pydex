# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Tree

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import statements
import tkinter as tk
import tkinter.ttk as ttk
import pyodbc 
import pandas as pd

#%% Class definition
class PyTree(ttk.Frame):
    def __init__(self, master = None, connectionString = None, table = None, filterColumn = None, filterId = None):
        # Define connection
        if connectionString is None:
            self.connection = pyodbc.connect("DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;")
        else:
            self.connection = pyodbc.connect(connectionString)
        
        # Define table
        if connectionString is None:
            self.table = 'Connections'
        else:
            self.table = table
        
        # Copy filterColumn and filterId
        self.filterColumn = filterColumn
        self.filterId = filterId
        
    
        # Actions to do when a treeview item is right clicked
        def popupMenu(event):
            # Display the popup menu
            try:
                #self.popup.selection = self.treeview.set(self.treeview.identify_row(event.y))
                self.popup.post(event.x_root, event.y_root)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.popup.grab_release()
       
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

        # Create the popup menu
        self.createPopupMenu()

        # Create the widgets
        self.createWidgets()

        # Define events
        self.treeview.bind('<<TreeviewSelect>>', self.selectItem)
        self.treeview.bind("<Button-3>", popupMenu)

    # Actions to do when a treeview item is selected
    def selectItem(self, event):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Propagate the event
        self.master.event_generate('<<TreeviewSelect>>')

    def editTreeItem(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('editTreeItem ' + self.Id)

    def renameTreeItem(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('renameTreeItem ' + self.Id)

    def moveTreeItem(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('moveTreeItem ' + self.Id)

    def addTreeItemBefore(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('addTreeItemBefore ' + self.Id)

    def addTreeItemAfter(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('addTreeItemAfter ' + self.Id)

    def addTreeItemIn(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('addTreeItemIn ' + self.Id)

    def deleteTreeItem(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('deleteTreeItem ' + self.Id)

    def refreshTree(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('Refresh tree')
        
    def createPopupMenu(self):
        #Create menu
        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Edit...", command=self.editTreeItem)
        self.popup.add_command(label="Rename...", command=self.renameTreeItem)
        self.popup.add_separator()
        self.popup.add_command(label="Move...", command=self.moveTreeItem)
        self.popup.add_command(label="Add before...", command=self.addTreeItemBefore)
        self.popup.add_command(label="Add after...", command=self.addTreeItemAfter)
        self.popup.add_command(label="Add in...", command=self.addTreeItemIn)
        self.popup.add_separator()
        self.popup.add_command(label="Delete...", command=self.deleteTreeItem)
        self.popup.add_separator()
        self.popup.add_command(label="Refresh", command=self.refreshTree)
        
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        

        # Make rows and columns stretchable
        self.rowconfigure(0, weight=1)        
        self.columnconfigure(0, weight=1)        

        # Tree
        self.treeview = ttk.Treeview(self)
        self.treeview.grid(row = 0, column = 0, rowspan=13, sticky = tk.NE + tk.SW, padx =2, pady=2)
        self.treeview['show'] = 'tree'
        self.treeview.column('#0', stretch=tk.YES, minwidth=500, width=200)
             
        # Get tree data from database        
        if self.filterColumn is None:
            treedata = pd.io.sql.read_sql("Select * From " + self.table + 
                                          " Where Status = 'A' " +
                                          " Order By [Level], Nr", self.connection)
        else:
            treedata = pd.io.sql.read_sql("Select * From " + self.table + 
                                          " Where " + self.filterColumn + " = " + self.filterId +
                                          "   And Status = 'A' " +
                                          " Order By [Level], Nr", self.connection)
    
        # Fill tree
        for i in treedata.index:
            if (i==0) | (treedata.ParentId[i]==0):
                self.treeview.insert('', treedata.Nr[i]-1, iid=treedata.Id[i], text=treedata.Title[i].strip())
            else:
                self.treeview.insert(treedata.ParentId[i], treedata.Nr[i]-1, iid=treedata.Id[i], text=treedata.Title[i].strip())

        # Open first treeview item
        self.treeview.item(treedata.Id[0], open=True)
        
        # Vertical scrollbar
        scrollVertical = ttk.Scrollbar(self)       
        scrollVertical.grid(row=0, column=1, sticky=tk.NE+tk.SW)
        scrollVertical.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollVertical.set)

        # Horizontal scrollbar
        scrollHorizontal = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollHorizontal.grid(row=1, column=0, sticky=tk.NE+tk.SW)
        scrollHorizontal.configure(command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scrollHorizontal.set)


# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyTree().mainloop()

