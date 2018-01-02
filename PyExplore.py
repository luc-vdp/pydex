# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Explore

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class PyExplore(ttk.Frame):
    def __init__(self, master = None, dataframes = None):
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        # Store dataframes
        self.dataframes = dataframes
        # Create widgets
        self.createWidgets()

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

    def showGraph():
        pass

    def listVars(self):
        self.comboboxDataframes['values'] = list(self.dataframes.keys())
        
    def ListColumns(self, event):
        self.listboxColumns.delete(0, tk.END)
        df = self.comboboxDataframes.get()
        if df != '':
            vars = self.dataframes[df].columns.values
            # Filtering listbox using search term from searchValue box 
            search_term = self.searchValue.get()
            for item in vars:
                if search_term.lower() in item.lower():
                    self.listboxColumns.insert(tk.END, item)
 
    # Callback function - Show Python code
    def code(self):
        if self.buttonCode.cget('text') == 'Show Code':
            self.panedwindowMain.add(self.frameRight)
            self.buttonCode.configure(text = 'Hide Code')
        else:
            self.panedwindowMain.forget(self.frameRight)
            self.buttonCode.configure(text = 'Show Code')
        
        
    # Callback function - Clicked somewhere
#    def click(event):
#        if self.focus_get() == textY:
#            selectedVar.set('Y')
#        elif self.focus_get() == textX:
#            selectedVar.set('X')
#        elif self.focus_get() == textS:
#            selectedVar.set('S')
#        elif self.focus_get() == textG:
#            selectedVar.set('G')

           
    def createWidgets(self):  
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make row 10 stretchable         
#        self.rowconfigure(10, weight=1)

        # Make certain rows and columns stretchable
        self.rowconfigure(0, weight=1)        
        self.columnconfigure(0, weight=1)

        #%% Main paned window
        # Paned window (stack horizontal, i.e. next to each other)
        self.panedwindowMain = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedwindowMain.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Create frameLeft and add it to the paned window
        self.frameLeft = ttk.Frame(self.panedwindowMain)
        self.panedwindowMain.add(self.frameLeft)
        self.panedwindowMain.paneconfigure(self.frameLeft, sticky=tk.NW+tk.SE)
        # Make frameLeft stretchable
        self.frameLeft.rowconfigure(1, weight=1)
        self.frameLeft.columnconfigure(1, weight=1)

        # Create frameMiddle and add it to the paned window
        self.frameMiddle = ttk.Frame(self.panedwindowMain)
        self.panedwindowMain.add(self.frameMiddle)
        self.panedwindowMain.paneconfigure(self.frameMiddle, sticky=tk.NW+tk.SE)
        # Make frameMiddle stretchable
        self.frameMiddle.rowconfigure(1, weight=1)
        self.frameMiddle.columnconfigure(8, weight=1)

        # Create frameRight and add it to the paned window
        self.frameRight = ttk.Frame(self.panedwindowMain)
        self.panedwindowMain.add(self.frameRight)
        self.panedwindowMain.paneconfigure(self.frameRight, sticky=tk.NW+tk.SE)
        self.panedwindowMain.forget(self.frameRight)
        # Make frameRight stretchable
        self.frameRight.rowconfigure(1, weight=1)
        self.frameRight.columnconfigure(0, weight=1)


        #%% LEFT
        # Combobox to select a dataframe
        self.comboboxDataframes = ttk.Combobox(self.frameLeft, postcommand=self.listVars)
        self.comboboxDataframes.grid(row = 0, column = 0, columnspan=3, sticky = tk.NE + tk.SW, padx =5, pady=5)
        self.comboboxDataframes.bind('<Return>',self.ListColumns)
        self.comboboxDataframes.bind('<<ComboboxSelected>>',self.ListColumns)
        
        # listbox with scrollbar to select a variable (column in the data frame)
        self.frameListbox = ttk.Frame(self.frameLeft, relief='solid', borderwidth=1)
        self.frameListbox.grid(row = 1, column = 0, columnspan=2, sticky = tk.NE + tk.SW, padx =5, pady=5)
        self.frameListbox.rowconfigure(0, weight=1)
        self.frameListbox.columnconfigure(0, weight=1)
        # Listview of columns in the dataframe
        self.scrollbarColumns = ttk.Scrollbar(self.frameListbox, orient=tk.VERTICAL)
        self.listboxColumns = tk.Listbox(self.frameListbox, yscrollcommand=self.scrollbarColumns.set)
        self.scrollbarColumns.config(command=self.listboxColumns.yview)
        self.scrollbarColumns.grid(row=0, column=1, sticky =tk.NW+tk.SE)
        #self.listboxColumns.bind('<<ListboxSelect>>',self.SelectColumn)
        self.listboxColumns.grid(row=0, column = 0, sticky = tk.NE + tk.SW)

        # Search field
        ttk.Label(self.frameLeft, text = "Find").grid(row = 14, column = 0, sticky = tk.W, padx =5, pady=5)
        self.searchValue = tk.StringVar()
        self.searchValue.trace_add("write", self.ListColumns(None))      
        #self.entryFind = ttk.Entry(self, textvariable=self.searchValue, command=self.ListColumns(None))
        self.entryFind = ttk.Entry(self.frameLeft, textvariable=self.searchValue)
        self.entryFind.grid(row = 14, column = 1, columnspan=2, sticky=tk.W+tk.E, padx =5, pady=5)

        # Properties
        ttk.Label(self.frameLeft, text = "Properties").grid(row = 15, column = 0, sticky = tk.W, padx =5, pady=5)
        
        #%% MIDDLE
        # Chart type
        self.graphtype = tk.StringVar() 
        self.graphtype.set('H')
        ttk.Radiobutton(self.frameMiddle, text='Histogram ', variable=self.graphtype, value='H', command=self.histogram).grid(row = 0, column = 0, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self.frameMiddle, text='Trend     ', variable=self.graphtype, value='T', command=self.trend).grid(row = 0, column = 1, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self.frameMiddle, text='XY        ', variable=self.graphtype, value='S', command=self.scatter).grid(row = 0, column = 2, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self.frameMiddle, text='Bar       ', variable=self.graphtype, value='R', command=self.bargraph).grid(row = 0, column = 3, sticky = tk.W, padx =5, pady=5)
        ttk.Radiobutton(self.frameMiddle, text='Boxplot   ', variable=self.graphtype, value='B', command=self.boxplot).grid(row = 0, column = 4, sticky = tk.W, padx =5, pady=5)

        self.buttonRefresh = ttk.Button(self.frameMiddle, text='Refresh', command=self.showGraph)
        self.buttonRefresh.grid(row = 0, column = 9, sticky = tk.W, padx =5, pady=5)
        self.buttonCode = ttk.Button(self.frameMiddle, text='Show Code', command=self.code)
        self.buttonCode.grid(row = 0, column = 10, sticky = tk.W, padx =5, pady=5)

        # Middle paned window (stack vertical, i.e. under each other)
        self.panedwindowMiddle = tk.PanedWindow(self.frameMiddle, orient=tk.VERTICAL)
        self.panedwindowMiddle.grid(row = 1, column = 0, columnspan=11, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Create matplotlib figure and add it to frameMiddle
        self.fig = Figure(figsize=(10, 8), tight_layout=True)

        self.ax1 = self.fig.add_subplot(1,1,1)
        self.ax1.set_title('title 1')
        self.ax1.set_xlabel( 'X-axis' )
        self.ax1.set_ylabel( 'Y-axis' )
        self.ax1.grid(True)
        
#        self.ax2 = self.fig.add_subplot(2,2,2)
#        self.ax2.set_title('title 2')
#        self.ax2.set_xlabel( 'X-axis' )
#        self.ax2.set_ylabel( 'Y-axis' )
#        self.ax2.grid(True)
#            
#        self.ax3 = self.fig.add_subplot(2,2,3)
#        self.ax3.set_title('title 3')
#        self.ax3.set_xlabel( 'X-axis' )
#        self.ax3.set_ylabel( 'Y-axis' )
#        self.ax3.grid(True)
            
        self.ax = self.ax1
        self.ax.set_facecolor('#FFFFE0')
                               
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frameMiddle)
        self.canvas.show()
        self.canvas.draw()
        self.panedwindowMiddle.paneconfigure(self.canvas.get_tk_widget(), sticky=tk.NW+tk.SE)
        self.panedwindowMiddle.add(self.canvas.get_tk_widget())   
        self.cid = self.canvas.mpl_connect('button_press_event', self)

        # Create frameSelection and add it to the paned window
        self.frameSelection = ttk.Frame(self.panedwindowMiddle, relief='ridge', borderwidth=4)
        # Make frameSelection stretchable
        self.frameSelection.rowconfigure(4, weight=1)
        self.frameSelection.columnconfigure(1, weight=1)
        # Y, X, Select and Group by labels
        self.selectedVar = tk.StringVar()
        self.selectedVar.set('Y')
        ttk.Radiobutton(self.frameSelection, text='Y       ', variable=self.selectedVar, value='Y').grid(row=0, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        ttk.Radiobutton(self.frameSelection, text='X       ', variable=self.selectedVar, value='X').grid(row=1, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        ttk.Radiobutton(self.frameSelection, text='Select  ', variable=self.selectedVar, value='S').grid(row=2, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        ttk.Radiobutton(self.frameSelection, text='Group by', variable=self.selectedVar, value='G').grid(row=3, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        # Y, X, Select and Group by entries
        self.textY = ttk.Entry(self.frameSelection).grid(row=0, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.textX = ttk.Entry(self.frameSelection).grid(row=1, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.textS = ttk.Entry(self.frameSelection).grid(row=2, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.textG = ttk.Entry(self.frameSelection).grid(row=3, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Text area for Info
        self.textInfo = ScrolledText(self.frameSelection, height=4) 
        self.textInfo.grid(row=4, column=0, columnspan=2, sticky = tk.NE + tk.SW, padx =1, pady=1)

        self.panedwindowMiddle.paneconfigure(self.frameSelection, sticky=tk.NW+tk.SE)
        self.panedwindowMiddle.add(self.frameSelection, minsize=100)
        
#        # Text area for Info
#        self.textInfo = ScrolledText(self.panedwindowMiddle, height=4) 
#        self.panedwindowMiddle.add(self.textInfo)
#        self.panedwindowMiddle.paneconfigure(self.textInfo, sticky=tk.NW+tk.SE)

        
        #%% RIGHT
        # Code
        ttk.Label(self.frameRight, text = "Code").grid(row = 0, column = 0, sticky = tk.NW+tk.SE, padx =5, pady=5)

        # Text area for generated code
        self.textCode = ScrolledText(self.frameRight, height=4) 
        self.textCode.grid(row = 1, column = 0, sticky = tk.NW+tk.SE, padx =5, pady=5)

# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyExplore().mainloop()

