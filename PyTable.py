# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import filedialog
import pandas as pd

class PyTable(ttk.Frame):
    def __init__(self, master = None, dataframe=None):
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        # Make row and column stretchable         
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        # Create the widgets
        self.createWidgets()

    def importData(self):
        filename = filedialog.askopenfilename()
        if filename != None:
            # Set wait cursor
            self.config(cursor="wait")
            self.update()
            # Read Excel file            
            d = pd.read_excel(filename)
            # Set wait cursor again
            self.config(cursor="wait")
            self.update()
            # Add dataframe to the table
            self.addDataframe(d)
            # Remove wait cursor
            self.config(cursor="")
        
    def exportData(self):
        pass
    
    def clearData(self):
        self.treeview.delete(*self.treeview.get_children())

    
    #%% Create widgets
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()

        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        
        # Make rows and columns stretchable
        self.rowconfigure(0, weight=0)        
        self.rowconfigure(1, weight=0)        
        self.rowconfigure(2, weight=1)        
        self.columnconfigure(0, weight=1)        

        # Buttons
        self.buttonImport = ttk.Button(self, text="Import...", command=self.importData)
        self.buttonImport.grid(row = 0, column = 2, sticky = tk.NW, padx =2, pady=2)
        
        self.buttonExport = ttk.Button(self, text="Export...", command=self.exportData)
        self.buttonExport.grid(row = 1, column = 2, sticky = tk.NW, padx =2, pady=2)
        
        self.buttonClear = ttk.Button(self, text="Clear...", command=self.clearData)
        self.buttonClear.grid(row = 2, column = 2, sticky = tk.NW, padx =2, pady=2)
        
        # Tree
        self.treeview = ttk.Treeview(self, show="headings")
        self.treeview.grid(row = 0, column = 0, rowspan=3, sticky = tk.NE + tk.SW, padx =2, pady=2)

        # Vertical scrollbar
        scrollVertical = ttk.Scrollbar(self)       
        scrollVertical.grid(row=0, column=1, rowspan=3, sticky=tk.NE+tk.SW)
        scrollVertical.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollVertical.set)

        # Horizontal scrollbar
        scrollHorizontal = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollHorizontal.grid(row=3, column=0, sticky=tk.NE+tk.SW)
        scrollHorizontal.configure(command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scrollHorizontal.set)

    def addDataframe(self, dataframe=None):
        # Clear the treeview first
        self.clearData()
        
        # make dataframe available
        self.data = dataframe
        
        # Make list of columns
        self.columns = dataframe.columns.tolist()

        # Add columns to treeview
        self.treeview.configure(columns=self.columns)

        # Set column headings and widths
        for col in self.columns:
            # Add header
            self.treeview.heading(col, text=col, anchor=tk.W)
            # Adjust the column's width to the header string
            self.treeview.column(col, width=tkFont.Font().measure(col.title())+10)
            self.treeview.column(col, stretch=1)
         
        # Add data to treeview
        for row in dataframe.itertuples(index=False, name='Pandas'):
            self.treeview.insert('', tk.END, values=row)
    
# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyTable().mainloop()