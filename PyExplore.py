# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Explore

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk

class PyExplore(ttk.Frame):
    def __init__(self, master = None):
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()



    def createWidgets(self):
        def histogram():
            pass
    
        def trend():
            pass
    
        def scatter():
            pass
    
        def bargraph():
            pass
    
        def boxplot():
            pass
    
        def code():
            pass
    
        def showGraph():
            pass
    
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make row 10 stretchable         
        self.rowconfigure(10, weight=1)

        # Make certain columns stretchable     
        self.columnconfigure(9, weight=5)        

        #%% LEFT
        # Combobox to select a dataframe
        self.comboboxDataframe = ttk.Combobox(self)
        self.comboboxDataframe.grid(row = 0, column = 0, columnspan=2, sticky = tk.NE + tk.SW, padx =5, pady=5)
        
        # Listview of columns in the dataframe
        self.listboxColumns = tk.Listbox(self)
        self.listboxColumns.grid(row = 1, column = 0, rowspan=13, columnspan=2, sticky = tk.NE + tk.SW, padx =5, pady=1)

        # Search field
        ttk.Label(self, text = "Find").grid(row = 14, column = 0, sticky = tk.W, padx =5, pady=5)
        ttk.Entry(self).grid(row = 14, column = 1, sticky = tk.W, padx =5, pady=5)

        # Properties
        
        #%% RIGHT
        # Chart type
        self.graphtype = tk.StringVar() 
        self.graphtype.set('H')
        ttk.Radiobutton(self, text='Histogram ', variable=self.graphtype, value='H', command=histogram).grid(row = 0, column = 2, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text='Trend     ', variable=self.graphtype, value='T', command=trend).grid(row = 0, column = 3, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text='XY        ', variable=self.graphtype, value='S', command=scatter).grid(row = 0, column = 4, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text='Bar       ', variable=self.graphtype, value='R', command=bargraph).grid(row = 0, column = 5, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self, text='Boxplot   ', variable=self.graphtype, value='B', command=boxplot).grid(row = 0, column = 6, sticky = tk.W, padx =5, pady=5)

        ttk.Button(self, text='Refresh', command=showGraph).grid(row = 0, column = 11, sticky = tk.W, padx =5, pady=5)
        ttk.Button(self, text='Show Code', command=code).grid(row = 0, column = 12, sticky = tk.W, padx =5, pady=5)

        # Graphs
        ttk.Label(self, text = "Graphs should come here").grid(row = 1, column = 2, rowspan=13, columnspan=6, sticky = tk.NW+tk.SE, padx =5, pady=5)

        # Specify Y, X, Select, Group by
        ttk.Label(self, text = "Y, X, Select, Group by should come here").grid(row = 13, column = 2, columnspan=6, sticky = tk.NW+tk.SE, padx =5, pady=5)
        
        # Info
        ttk.Label(self, text = "Info should come here").grid(row = 16, column = 2, columnspan=6, sticky = tk.NW+tk.SE, padx =5, pady=5)

        
# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyExplore().mainloop()

