# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - GraphDetails

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk

class PyParameters(ttk.Frame):
    def __init__(self, master = None, connectionString = None, queryId='0', dict=None):
        # Define connectionString
        if connectionString is None:
            self.connectionString = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        else:
            self.connectionString = connectionString
        
        # Store queryId
        self.queryId = queryId
        
        # Store dict
        self.dict = dict
        
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        
        # Make row and column stretchable         
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        
        # Create the widgets
        self.createWidgets()

    def save(self):
        pass
    
    def clear(self):
        pass
    
    def get(self):
        pass

    def run(self):
        # Set parameters
        idx = 0            
        for key in self.dict:
            self.dict[key] = self.parameter[idx].get()
            idx += 1
        # Print parameters
        print(self.dict)
            
    #%% Create widgets
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()

        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        
        # Make rows and columns stretchable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Parameters
        if self.dict == None:
            self.dict = {'n' : '100'}

        self.parameterName = []
        self.parameter = []
        idx = 0            
        for key in self.dict:
            self.parameterName.append(ttk.Label(self, text=key))
            self.parameterName[idx].grid(row=idx, column=0, columnspan=2, sticky=tk.SE, padx = 2, pady = 2)

            self.parameter.append(ttk.Entry(self))
            self.parameter[idx].grid(row=idx, column=2, columnspan=2, sticky=tk.SE+tk.SW, padx = 2, pady = 2)
            idx += 1
        
        # Buttons        
        self.buttonSave = ttk.Button(self, text="Save", command=self.save)
        self.buttonSave.grid(row = 9, column = 0, sticky = tk.NE, padx =2, pady=2)
        
        self.buttonClear = ttk.Button(self, text="Clear", command=self.clear)
        self.buttonClear.grid(row = 9, column = 1, sticky = tk.NE+tk.SW, padx =2, pady=2)
        
        self.buttonGet = ttk.Button(self, text="Get ", command=self.get)
        self.buttonGet.grid(row = 9, column = 2, sticky = tk.NE+tk.SW, padx =2, pady=2)
        
        self.buttonRun = ttk.Button(self, text="Run ", command=self.run)
        self.buttonRun.grid(row = 9, column = 3, sticky = tk.NE+tk.SW, padx =2, pady=2)

# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyParameters().mainloop()