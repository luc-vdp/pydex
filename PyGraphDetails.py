# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - GraphDetails

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pandas as pd

class PyGraphDetails(ttk.Frame):
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
        d = pd.read_excel('data.xlsx')
        self.addDataframe(d)
    
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
        self.rowconfigure(0, weight=1)        
        self.rowconfigure(5, weight=7)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=3)
        self.columnconfigure(6, weight=3)
        self.columnconfigure(7, weight=3)
        self.columnconfigure(8, weight=3)
        self.columnconfigure(9, weight=3)

        # Buttons
        self.graphType = tk.StringVar()
        self.graphType.set('T')
        ttk.Radiobutton(self, text="Histogram    ", value='H', variable=self.graphType).grid(row = 0, column = 0, sticky = tk.NW, padx =2, pady=2)
        ttk.Radiobutton(self, text="Trend        ", value='T', variable=self.graphType).grid(row = 0, column = 1, sticky = tk.NW, padx =2, pady=2)
        ttk.Radiobutton(self, text="X-Y          ", value='X', variable=self.graphType).grid(row = 0, column = 2, columnspan=3, sticky = tk.NW, padx =2, pady=2)
        ttk.Radiobutton(self, text="Box & Whisker", value='B', variable=self.graphType).grid(row = 0, column = 5, sticky = tk.NW, padx =2, pady=2)
        ttk.Radiobutton(self, text="CuSum        ", value='C', variable=self.graphType).grid(row = 0, column = 6, sticky = tk.NW, padx =2, pady=2)
        ttk.Radiobutton(self, text="Bar          ", value='R', variable=self.graphType).grid(row = 0, column = 7, sticky = tk.NW, padx =2, pady=2)
        ttk.Radiobutton(self, text="Stacked      ", value='S', variable=self.graphType).grid(row = 0, column = 8, sticky = tk.NW, padx =2, pady=2)
        
        # ListBox with scrollbar
        scrollbarAllVars = ttk.Scrollbar(self, orient=tk.VERTICAL)
        listboxAllVars = tk.Listbox(self, yscrollcommand=scrollbarAllVars.set)
        scrollbarAllVars.config(command=listboxAllVars.yview)
        scrollbarAllVars.grid(row = 1, column = 2, rowspan = 9, sticky = tk.NW+tk.S, padx =2, pady=2)
        #listboxAllVars.bind('<<ListboxSelect>>',SelectColumn)
        listboxAllVars.grid(row = 1, column = 0, rowspan = 9, columnspan=2, sticky = tk.NW+tk.SE, padx =2, pady=2)

        # Max Y
        ttk.Label(self, text="Max:").grid(row = 1, column = 3, sticky=tk.SE, padx = 2, pady = 2)
        ttk.Entry(self, width=5).grid(row = 1, column = 4, sticky=tk.NW, padx = 2, pady = 2)
        
        # Empty
        ttk.Label(self, text=" ").grid(row = 2, column = 3, sticky=tk.SE, padx = 2, pady = 2)

        # Autoscale
        ttk.Checkbutton(self, text="Autoscale").grid(row = 3, column = 3, columnspan=2, sticky=tk.SE, padx = 2, pady = 2)

        # Empty
        ttk.Label(self, text=" ").grid(row = 4, column = 3, sticky=tk.SE, padx = 2, pady = 2)

        # Min Y
        ttk.Label(self, text="Min:").grid(row = 6, column = 3, sticky=tk.SE, padx = 2, pady = 2)
        ttk.Entry(self, width=5).grid(row = 6, column = 4, sticky=tk.NW, padx = 2, pady = 2)

        # ListBox with scrollbar
        scrollbarYVars = ttk.Scrollbar(self, orient=tk.VERTICAL)
        listboxYVars = tk.Listbox(self, yscrollcommand=scrollbarYVars.set)
        scrollbarYVars.config(command=listboxYVars.yview)
        scrollbarYVars.grid(row = 1, column = 9, rowspan = 6, sticky = tk.NW+tk.S, padx =2, pady=2)
        #listboxYVars.bind('<<ListboxSelect>>',SelectColumn)
        listboxYVars.grid(row = 1, column = 5, rowspan = 6, columnspan=4, sticky = tk.NW+tk.SE, padx =2, pady=2)

        # Min X
        ttk.Label(self, text="Min:").grid(row = 7, column = 4, sticky=tk.SE, padx = 2, pady = 2)
        ttk.Entry(self, width=5).grid(row = 7, column = 5, sticky=tk.NW, padx = 2, pady = 2)

        # X-variable
        ttk.Combobox(self).grid(row=7, column=6, columnspan = 2, sticky=tk.NW+tk.SE, padx = 2, pady = 2)
        
        # Max X
        ttk.Label(self, text="Max:").grid(row = 7, column = 8, sticky=tk.SE, padx = 2, pady = 2)
        ttk.Entry(self, width=5).grid(row = 7, column = 9, sticky=tk.NW, padx = 2, pady = 2)

        # Intervals
        ttk.Entry(self, width=5).grid(row = 8, column = 6, sticky=tk.SE, padx = 2, pady = 2)
        ttk.Label(self, text="intervals").grid(row = 8, column = 7, sticky=tk.NW, padx = 2, pady = 2)

        # Buttons        
        self.buttonRun = ttk.Button(self, text="Run   ", command=self.exportData)
        self.buttonRun.grid(row = 9, column = 4, sticky = tk.E, padx =2, pady=2)
        
        self.buttonSave = ttk.Button(self, text="Save ", command=self.clearData)
        self.buttonSave.grid(row = 9, column = 5, sticky = tk.W, padx =2, pady=2)
        
        self.buttonShow = ttk.Button(self, text="Show ", command=self.clearData)
        self.buttonShow.grid(row = 9, column = 9, sticky = tk.E, padx =2, pady=2)
        
        self.buttonOK = ttk.Button(self, text="  OK   ", command=self.clearData)
        self.buttonOK.grid(row = 9, column = 10, sticky = tk.E, padx =2, pady=2)
        
        self.buttonClose = ttk.Button(self, text="Close ", command=self.clearData)
        self.buttonClose.grid(row = 9, column = 11, sticky = tk.W, padx =2, pady=2)
        


# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyGraphDetails().mainloop()