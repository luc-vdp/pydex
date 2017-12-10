# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Scripts

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk

class PyScripts(ttk.Frame):
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
        self.columnconfigure(0, weight=1)        
        self.columnconfigure(2, weight=4)        

        # Tree
        self.treeview = ttk.Treeview(self)
        self.treeview.grid(row = 0, column = 0, rowspan=13, sticky = tk.NE + tk.SW, padx =1, pady=1)

        # Label
        tk.Label(self, text='Title').grid(row = 0, column = 2, sticky = tk.NW + tk.SE, padx =5, pady=5)

        # Description
        tk.Text(self, height=5, width=50).grid(row = 1, column = 2, rowspan=11, sticky = tk.NW + tk.SE, padx =5, pady=1)

        # Buttons
        ttk.Button(self, text = "Test").grid(row = 12, column = 2, sticky = tk.NW, padx =5, pady=5)
        ttk.Button(self, text = "Save").grid(row = 12, column = 2, sticky = tk.NE, padx =5, pady=5)
        
# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyScripts().mainloop()

