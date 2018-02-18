# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - GraphDetails

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
from PyData import PyData

class PyGraphDetails(ttk.Frame):
    def __init__(self, master = None, connectionStringMeta=None):
        # Define connection to the meta data
        if connectionStringMeta is None:
            self.connectionStringMeta = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        else:
            self.connectionStringMeta = connectionStringMeta
        # Store dataframes
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        # Make row and column stretchable         
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        # Create the widgets
        self.createWidgets()

    def selectQuery(self):
        # Create top level window
        self.toplevel = tk.Toplevel()
        # Add Query management widget
        self.pyData = PyData(self.toplevel, connectionStringMeta=self.connectionStringMeta, queryId=self.queryId.get())
        self.pyData.grid(row=0, column=0, columnspan=3, sticky=tk.NW+tk.SE)
        # Add OK button
        buttonOK = tk.Button(self.toplevel, text="   OK   ", width=8, command=self.queryOK)
        buttonOK.grid(row=1, column=1, sticky=tk.SE, padx=5, pady=5)
        # Add Cancel button
        buttonCancel = tk.Button(self.toplevel, text="Cancel", width=8, command=self.queryCancel)
        buttonCancel.grid(row=1, column=2, sticky=tk.SE, padx=5, pady=5)
        
    def queryOK(self):
#        print(self.pyData.entryName.get())
#        print(self.pyData.Id.get())
#        print(self.pyData.connectionStringData)
#        
#        self.Data.set(self.pyData.entryName.get())
#        self.queryId.set(self.pyData.Id.get())
#        self.queryName = self.pyData.connectionStringData
        self.toplevel.destroy()
        
    def queryCancel(self):
        self.toplevel.destroy()
        
    def run(self):
        pass
        
    def save(self):
        pass
    
    #%% Create widgets
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()

        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        
        # Make rows and columns stretchable
        self.rowconfigure(0, weight=0)        
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Reference to the Query
        self.QueryName = tk.StringVar()
        #styleLeftAligned = ttk.Style()
        #styleLeftAligned.configure('LeftAligned.TButton', foreground='maroon', justify=tk.LEFT)
        ttk.Label(self, text = "Query:").grid(row = 0, column = 0, sticky = tk.NE, padx =5, pady=5)
        self.buttonQuery = ttk.Button(self, text = "Select query", textvariable=self.QueryName, width=40, command=self.selectQuery)
        self.buttonQuery.grid(row = 0, column = 1, columnspan=1, sticky = tk.NW + tk.NE, padx =5, pady=5)
        self.queryId = tk.StringVar()
        self.queryId.set("0")
        ttk.Label(self, textvariable=self.queryId).grid(row = 0, column = 2, sticky = tk.NW, padx =5, pady=5)
        
        # ListBox with scrollbar
        scrollbarAllVars = ttk.Scrollbar(self, orient=tk.VERTICAL)
        listboxAllVars = tk.Listbox(self, height=20, yscrollcommand=scrollbarAllVars.set)
        scrollbarAllVars.config(command=listboxAllVars.yview)
        scrollbarAllVars.grid(row = 1, column = 2, rowspan = 10, sticky = tk.NW+tk.S, padx =2, pady=2)
        #listboxAllVars.bind('<<ListboxSelect>>',SelectColumn)
        listboxAllVars.grid(row = 1, column = 0, rowspan = 10, columnspan=2, sticky = tk.NW+tk.SE, padx =2, pady=2)

        # Graph type
        self.graphType = tk.StringVar()
        radiobuttonHistogram = ttk.Radiobutton(self, text="Histogram    ", value='H', variable=self.graphType)
        radiobuttonHistogram.grid(row = 0, column = 3, sticky = tk.NW, padx =2, pady=2)
        radiobuttonTrend = ttk.Radiobutton(self, text="Trend        ", value='T', variable=self.graphType)
        radiobuttonTrend.grid(row = 0, column = 4, sticky = tk.NW, padx =2, pady=2)
        radiobuttonScatter = ttk.Radiobutton(self, text="X-Y          ", value='X', variable=self.graphType)
        radiobuttonScatter.grid(row = 0, column = 5, sticky = tk.NW, padx =2, pady=2)
        radiobuttonBoxAndWhisker = ttk.Radiobutton(self, text="Box & Whisker", value='B', variable=self.graphType)
        radiobuttonBoxAndWhisker.grid(row = 0, column = 6, sticky = tk.NW, padx =2, pady=2)
        radiobuttonCuSum = ttk.Radiobutton(self, text="CuSum        ", value='C', variable=self.graphType)
        radiobuttonCuSum.grid(row = 0, column = 7, sticky = tk.NW, padx =2, pady=2)
        radiobuttonBar = ttk.Radiobutton(self, text="Bar          ", value='R', variable=self.graphType)
        radiobuttonBar.grid(row = 0, column = 8, sticky = tk.NW, padx =2, pady=2)
        radiobuttonStacked = ttk.Radiobutton(self, text="Stacked      ", value='S', variable=self.graphType)
        radiobuttonStacked.grid(row = 0, column = 9, sticky = tk.NW, padx =2, pady=2)

        # Max Y
        ttk.Label(self, text="Max:").grid(row = 1, column = 3, sticky=tk.SE, padx = 2, pady = 2)
        self.maxY = tk.StringVar()
        self.entryMaxY = ttk.Entry(self, textvariable=self.maxY ,width=8)
        self.entryMaxY.grid(row = 2, column = 3, sticky=tk.E, padx = 2, pady = 2)
        
        # Empty
        ttk.Label(self, text=" ").grid(row = 3, column = 3, sticky=tk.SE, padx = 2, pady = 2)

        # Autoscale
        ttk.Checkbutton(self, text="Autoscale").grid(row = 4, column = 3, padx = 2, pady = 2)

        # Empty
        ttk.Label(self, text=" ").grid(row = 5, column = 3, sticky=tk.SE, padx = 2, pady = 2)

        # Min Y
        ttk.Label(self, text="Min:").grid(row = 6, column = 3, sticky=tk.SE, padx = 2, pady = 2)
        self.minY = tk.StringVar()
        self.entryMinY = ttk.Entry(self, textvariable=self.minY, width=8)
        self.entryMinY.grid(row = 7, column = 3, sticky=tk.E, padx = 2, pady = 2)

        # ListBox with scrollbar
        scrollbarYVars = ttk.Scrollbar(self, orient=tk.VERTICAL)
        listboxYVars = tk.Listbox(self, yscrollcommand=scrollbarYVars.set)
        scrollbarYVars.config(command=listboxYVars.yview)
        scrollbarYVars.grid(row = 1, column = 8, rowspan = 7, sticky = tk.NW+tk.S, padx =2, pady=2)
        #listboxYVars.bind('<<ListboxSelect>>',SelectColumn)
        listboxYVars.grid(row = 1, column = 4, rowspan = 7, columnspan=4, sticky = tk.NW+tk.SE, padx =2, pady=2)

        # Regression
        self.checkRegression = ttk.Checkbutton(self, text="Regression")
        self.checkRegression.grid(row = 2, column = 9, padx = 2, pady = 2)

        # Min X
        ttk.Label(self, text="Min:").grid(row = 8, column = 3, sticky=tk.SE, padx = 2, pady = 2)
        self.minX = tk.StringVar()
        self.entryMinX = ttk.Entry(self, textvariable=self.minX, width=8)
        self.entryMinX.grid(row = 8, column = 4, sticky=tk.NW, padx = 2, pady = 2)

        # X-variable
        self.comboboxXvariable = ttk.Combobox(self)
        self.comboboxXvariable.grid(row=8, column=5, columnspan = 2, sticky=tk.NW+tk.SE, padx = 2, pady = 2)
        
        # Max X
        ttk.Label(self, text="Max:").grid(row = 8, column = 7, sticky=tk.SE, padx = 2, pady = 2)
        self.maxX = tk.StringVar()
        self.entryMaxX = ttk.Entry(self, textvariable=self.maxX, width=8)
        self.entryMaxX.grid(row = 8, column = 8, sticky=tk.NW, padx = 2, pady = 2)

        # Intervals
        self.intervals = tk.StringVar()
        self.entryIntervals = ttk.Entry(self, textvariable=self.intervals, width=8)
        self.entryIntervals.grid(row = 9, column = 5, sticky=tk.SE, padx = 2, pady = 2)
        ttk.Label(self, text="intervals").grid(row = 9, column = 6, sticky=tk.NW, padx = 2, pady = 2)

        # Buttons        
        self.buttonRun = ttk.Button(self, text="Run   ", command=self.run)
        self.buttonRun.grid(row = 10, column = 3, sticky = tk.E, padx =2, pady=2)
        
        self.buttonSave = ttk.Button(self, text="Save ", command=self.save)
        self.buttonSave.grid(row = 10, column = 4, sticky = tk.W, padx =2, pady=2)
        
#        self.buttonShow = ttk.Button(self, text="Show ", command=self.clearData)
#        self.buttonShow.grid(row = 10, column = 9, sticky = tk.E, padx =2, pady=2)
#        
#        self.buttonOK = ttk.Button(self, text="  OK   ", command=self.clearData)
#        self.buttonOK.grid(row = 10, column = 10, sticky = tk.E, padx =2, pady=2)
#        
#        self.buttonClose = ttk.Button(self, text="Close ", command=self.clearData)
#        self.buttonClose.grid(row = 10, column = 11, sticky = tk.W, padx =2, pady=2)
        
# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyGraphDetails().mainloop()