# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from PyDatabases import PyDatabases
from PyData import PyData
from PyGraphs import PyGraphs
from PyExplore import PyExplore
from PyScripts import PyScripts

class PyDex(ttk.Frame):
    def __init__(self, master = None):
        # Define connection
        self.connectionStringMeta = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        # Make row and column stretchable         
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        # Store all dataframes
#        global glb
#        glb = globals()
        self.dataframes = {}
        # Create the menus
        # self.CreateMenus()
        # Connection properties
        self.connectionId = None
        self.connectionName = None
        self.connectionString = None
        # Create the widgets
        self.createWidgets()

    # Create the menus
    def CreateMenus(self):
        # Menu bar
        self.menuMain = tk.Menu(self)
        self.master.config(menu=self.menuMain)

        # File menu        
        self.menuFile = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="File", menu=self.menuFile)
        self.menuFile.add_command(label="New", command=self.NewFile)
        self.menuFile.add_command(label="Open...", command=self.OpenFile)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit", command=self.master.destroy)

        # Edit menu        
        self.menuEdit = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="Edit", menu=self.menuEdit)
        self.menuEdit.add_command(label="Rename...", command=self.RenameDataframe)
        
        # Tools menu
        self.menuTools = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="Tools", menu=self.menuTools)
        self.menuTools.add_command(label="Preferences...", command=self.Preferences)
        
        # Help menu
        self.menuHelp = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="Help", menu=self.menuHelp)
        self.menuHelp.add_command(label="About...", command=self.About)
        
    # Define menu callbacks
    def NewFile(self):
        messagebox.showinfo("New file","TO DO")
        
    def OpenFile(self):
        name = filedialog.askopenfilename()
        messagebox.showinfo("File to open",name)
        
    def Preferences(self):
        messagebox.showinfo("Preferences","TO DO")
        
    def RenameDataframe(self):
        messagebox.showinfo("Rename Dataframe","TO DO")
        
    def About(self):
        messagebox.showinfo("About pydex","Python Data Exploration Tool")
        
    def selectDatabaseTab(self, event):
        self.notebook.select(4)
        #print(PyData.getConnectionId(PyData))
        #PyDatabases.setItem(PyData.getConnectionId(PyData))
        
    # Create the widgets
    def createWidgets(self):
        # Create tabbed control (notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row = 0, column = 0, sticky = tk.NE + tk.SW)
        
        # Data tab page
        self.frameData = ttk.Frame(self.notebook) 
        self.notebook.add(self.frameData, text=' Data ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameData.rowconfigure(0, weight=1)
        self.frameData.columnconfigure(0, weight=1)        
        # Add Data widget
        self.pyData = PyData(self.frameData, self.connectionStringMeta, self.dataframes, self.connectionId, self.connectionName, self.connectionString)
        self.pyData.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =5, pady=5)
        self.pyData.bind('<<DatabaseSelect>>', self.selectDatabaseTab)

        # Graphs tab page
        self.frameGraphs = ttk.Frame(self.notebook) 
        self.notebook.add(self.frameGraphs, text=' Graphs ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameGraphs.rowconfigure(0, weight=1)
        self.frameGraphs.columnconfigure(0, weight=1)        
        # Add Database widget
        self.pyGraphs = PyGraphs(self.frameGraphs, self.connectionStringMeta)
        self.pyGraphs.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =5, pady=5)

        # Explore tab page
        self.frameExplore = ttk.Frame(self.notebook) 
        self.notebook.add(self.frameExplore, text=' Explore ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameExplore.rowconfigure(0, weight=1)
        self.frameExplore.columnconfigure(0, weight=1)        
        # Add Database widget
        self.pyExplore = PyExplore(self.frameExplore, self.dataframes)
        self.pyExplore.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =5, pady=5)

        # Scripts tab page
        self.frameScripts = ttk.Frame(self.notebook) 
        self.notebook.add(self.frameScripts, text=' Scripts ', sticky=tk.NW + tk.SE)
        # Make row and column stretchable         
        self.frameScripts.rowconfigure(0, weight=1)
        self.frameScripts.columnconfigure(0, weight=1)        
        # Add Database widget
        self.pyScripts = PyScripts(self.frameScripts)
        self.pyScripts.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =5, pady=5)

# Allow the class to run stand-alone.
if __name__ == "__main__":
    app = PyDex() 
    app.master.title('PyDex - Python Data Exploration Tool - version 0.1')
    app.master.geometry("1280x640")
    app.mainloop()