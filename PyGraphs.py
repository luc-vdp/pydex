# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk

class PyGraphs(ttk.Frame):
    def __init__(self, master = None):
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make row 10 stretchable         
        self.rowconfigure(10, weight=1)

        # Make certain columns stretchable
        self.columnconfigure(2, weight=1)        
        self.columnconfigure(3, weight=5)        

        # Tree
        self.treeview = ttk.Treeview(self)
        self.treeview.grid(row = 0, column = 0, rowspan=13, columnspan=3, sticky = tk.NE + tk.SW, padx =1, pady=1)

        # Number of graphs
        ttk.Label(self, text = "Graphs:").grid(row = 13, column = 0, sticky = tk.W, padx =5, pady=5)
        ttk.Combobox(self).grid(row = 13, column = 1, sticky = tk.W, padx =5, pady=5)
        # Number of points
        ttk.Label(self, text = "Graphs:").grid(row = 14, column = 0, sticky = tk.W, padx =5, pady=5)
        tk.Spinbox(self).grid(row = 14, column = 1, sticky = tk.W, padx =5, pady=5)
        # Synchronize
        ttk.Checkbutton(self, text = "Synchronize:").grid(row = 15, column = 0, sticky = tk.W, padx =5, pady=5)
    
        # Graphs
        ttk.Label(self, text = "Graphs should come here").grid(row = 0, column = 3, rowspan=13, sticky = tk.NW+tk.SE, padx =5, pady=5)

        # Data table
        ttk.Label(self, text = "Data tble should come here").grid(row = 13, column = 3, sticky = tk.NW+tk.SE, padx =5, pady=5)
        

# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyGraphs().mainloop()

