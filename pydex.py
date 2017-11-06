# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool

Created on Sun Nov  5 12:59:18 2017

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
#from tkinter import messagebox
from tkinter import filedialog

import pandas as pd
#import seaborn as sb

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

class PyDex(ttk.Frame):
    def __init__(self, master):
        self.master = master
        master.title("PyDex - Python Data Exploration Tool - version 0.1")
        master.geometry("1280x640")
        
        # Add menu
        self.menuMain = tk.Menu(self.master)
        self.master.config(menu=self.menuMain)
        
        self.menuFile = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="File", menu=self.menuFile)
        self.menuFile.add_command(label="New", command=self.NewFile)
        self.menuFile.add_command(label="Open...", command=self.OpenFile)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit", command=root.destroy)
        
        self.menuEdit = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="Edit", menu=self.menuEdit)
        self.menuEdit.add_command(label="Rename...", command=self.RenameDataframe)
        
        self.menuTools = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="Tools", menu=self.menuTools)
        self.menuTools.add_command(label="Preferences...", command=self.Preferences)
        
        self.menuHelp = tk.Menu(self.menuMain, tearoff=False)
        self.menuMain.add_cascade(label="Help", menu=self.menuHelp)
        self.menuHelp.add_command(label="About...", command=self.About)

        # Left frame
        self.frameLeft = ttk.Frame(self.master)
        self.frameLeft.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y, padx=4, pady=2)
        
        # Combobox to select a data frame
        self.combobox = ttk.Combobox(self.frameLeft)
        variables= [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
        self.combobox['values'] = variables
#        #self.combobox.bind('<Return>',ListColumns)
#        #self.combobox.bind('<<ComboboxSelected>>',ListColumns)
#        self.combobox.pack(pady=4)

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

root = tk.Tk()
my_gui = PyDex(root)
root.mainloop()