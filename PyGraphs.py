# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Databases

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerLine2D

from PyTree import PyTree
from PyTable import PyTable

import database

class PyGraphs(ttk.Frame):
    def __init__(self, master = None, connectionString = None):
        # Define connection to the meta data
        if connectionString is None:
            self.connectionStringMeta = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
        else:
            self.connectionStringMeta = connectionString
            
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    #%% Actions to do when a treeview item is selected in the Query Tree
    def selectGraph(self, event):
        # Get selected tree item
        self.Id = self.treeviewGraphs.Id       
        # Get corresponding info from database
        query = "Select * From Graphs Where Id = " + self.Id

        query = ( 
        '''SELECT A.[Id]
                 ,A.[Status]
                 ,A.[ParentId]
                 ,A.[Level]
                 ,A.[Nr]
                 ,RTrim(A.[Title])      As Title
                 ,RTrim(A.[QueryName])  As QueryName
                 ,A.[GraphType]
                 ,A.[Y_max]
                 ,A.[Y_min]
                 ,A.[Autoscale_Y]
                 ,A.[Autoscale_X]
                 ,A.[Interval_min]
                 ,A.[Interval_max]
                 ,A.[Interval_count]
                 ,A.[Box]
                 ,A.[Whisker]
                 ,RTrim(A.[X_variable]) As X_variable
                 ,RTrim(D.[ColumnName]) As ColumnName
                 ,RTrim(A.[ColorBy])    As ColorBy
                 ,A.[Regression]
                 ,RTrim(A.[UserId])     As UserId
                 ,A.[TimeChanged]
                 ,B.[SQL_Data]
                 ,B.[SQL_Parameters]
                 ,B.[AutoFetchParameters]
                 ,C.[DatabaseId]
                 ,CASE WHEN C.[User] = '' THEN 'DRIVER={' + Rtrim(C.Driver) + '};Server=' + Rtrim(C.Server) + ';Database=' + Rtrim(C.[Database]) + ';Trusted_Connection=yes;' 
                       ELSE 'DRIVER={' + Rtrim(C.Driver) + '};Server=' + Rtrim(C.Server) + ';Database=' + Rtrim(C.[Database]) + ';UID=' + Rtrim(C.[User]) + ';PWD=' + Rtrim(C.[Password]) END As ConnectionString
             FROM [Metadata].[dbo].[Graphs] A LEFT  OUTER JOIN [Metadata].[dbo].[Y_variables] D ON D.[ID] = A.[ID]
                , [Metadata].[dbo].[Queries] B
                , [Metadata].[dbo].[Connections] C
             WHERE A.[QueryName] = B.[QueryName]
               AND B.[Status] = 'A'
               AND B.[ConnectionId] = C.Id
               AND C.[Status] = 'A'
               AND A.[ID] = ''' + self.Id)
                              
        # Get the metadata
        self.metadata = database.getData(self.connectionStringMeta, query)
        
    def showGraph(self, event=None):
        # Get the data
        connectionStringData = self.metadata.ConnectionString[0]
        query = self.metadata.SQL_Data[0]
        self.data = database.getData(connectionStringData, query)
        # Show the data in the table
        self.pyTable.addDataframe(dataframe = self.data)
        # Determine X-variable
        X_variable = self.metadata.X_variable[0].strip()
        # Determine Y-variables
        if self.metadata.ColumnName[0] != None:
            Y_variable = []
            # Get all defined Y-variables
            for i in self.metadata.index:
                Y_variable.append(self.metadata.ColumnName[i].strip())
        else:
            # Get all numerical columns
            Y_variable = self.data._get_numeric_data().columns
                
        # Show the data in the graph
        for i in self.metadata.index:
            Y_variable = self.metadata.ColumnName[i].strip()
            cmd = 'self.ax.plot(self.data.' + X_variable + ', self.data.' + Y_variable + ', label = "' + Y_variable + '")'
            print(cmd)
            eval(cmd)
        # Add Title
        self.ax.set_title(self.treeviewGraphs.FullTitle())
        # Add xlabel
        self.ax.set_xlabel(X_variable)
        # Add legend
        #self.ax.legend(['test1','test2'])
        self.ax.legend(self.metadata.ColumnName)
        # Refresh
        self.canvas.draw()
        
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Make certain rows and columns stretchable
        self.rowconfigure(0, weight=1)        
        self.columnconfigure(0, weight=1)

        # Paned window (stack horizontal, i.e. next to each other)
        self.panedwindowMain = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedwindowMain.grid(row = 0, column = 0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Create frameLeft and add it to the paned window
        self.frameLeft = ttk.Frame(self.panedwindowMain)
        self.panedwindowMain.add(self.frameLeft)

        # Make frameLeft stretchable
        self.frameLeft.rowconfigure(0, weight=1)
        self.frameLeft.columnconfigure(1, weight=1)
        
        # Create tree and add it to the left frame
        self.treeviewGraphs = PyTree(self.frameLeft, connectionString=self.connectionStringMeta, table='Graphs')
        self.treeviewGraphs.grid(row = 0, column = 0, columnspan = 2, sticky = tk.NE + tk.SW, padx =1, pady=1)

        # Pass events
        self.frameLeft.bind('<<TreeviewSelect>>', self.selectGraph)
        self.frameLeft.bind('<<Double-Button-1>>', self.showGraph)
        
        # Number of graphs
        ttk.Label(self.frameLeft, text = "Graphs:").grid(row = 1, column = 0, sticky = tk.W, padx =5, pady=5)
        self.numberOfGraphs = tk.StringVar()
        comboboxGraphs = ttk.Combobox(self.frameLeft, textvariable=self.numberOfGraphs, width=8)
        comboboxGraphs['values'] = ['1x1','2x1','3x1','4x1','5x1','6x1','1x2','2x2','3x2']
        comboboxGraphs.current(0)
        comboboxGraphs.grid(row = 1, column = 1, sticky = tk.W, padx =5, pady=5)
        
        # Number of points
        ttk.Label(self.frameLeft, text = "Points:").grid(row = 2, column = 0, sticky = tk.W, padx =5, pady=5)
        self.NumberOfPoints = tk.IntVar()
        self.NumberOfPoints.set(50)
        self.spinboxNumberOfPoints = tk.Spinbox(self.frameLeft, from_=0, to=10000, increment=10, textvariable=self.NumberOfPoints, width=8)
        self.spinboxNumberOfPoints.setvar(name='self.NumberOfPoints', value=50)
        self.spinboxNumberOfPoints.grid(row = 2, column = 1, sticky = tk.W, padx =5, pady=5)
                
        # Synchronize
        self.Synchronize = tk.IntVar()
        self.Synchronize.set(1)
        self.checkbuttonSynchronize = ttk.Checkbutton(self.frameLeft, text = "Synchronize", variable=self.Synchronize)
        self.checkbuttonSynchronize.grid(row = 3, column = 0, columnspan = 2, sticky = tk.W, padx =5, pady=5)

        # Create panedwindowRight and add it to the panedwindowMain
        self.panedwindowRight = tk.PanedWindow(self, orient=tk.VERTICAL)
        self.panedwindowMain.add(self.panedwindowRight)
    
        # Create matplotlib figure and add it to frameRight
        self.fig = Figure(figsize=(12, 10), tight_layout=True)

        self.ax1 = self.fig.add_subplot(3,1,1)
        self.ax1.set_title('title 1')
        self.ax1.set_xlabel( 'X-axis' )
        self.ax1.set_ylabel( 'Y-axis' )
        self.ax1.grid(True)
        
        self.ax2 = self.fig.add_subplot(3,1,2)
        self.ax2.set_title('title 2')
        self.ax2.set_xlabel( 'X-axis' )
        self.ax2.set_ylabel( 'Y-axis' )
        self.ax2.grid(True)
            
        self.ax3 = self.fig.add_subplot(3,1,3)
        self.ax3.set_title('title 3')
        self.ax3.set_xlabel( 'X-axis' )
        self.ax3.set_ylabel( 'Y-axis' )
        self.ax3.grid(True)
            
        self.ax = self.ax1
        self.ax.set_facecolor('#FFFFE0')
                               
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panedwindowRight)
        self.canvas.show()
        self.canvas.draw()
        self.panedwindowRight.add(self.canvas.get_tk_widget())        
        
        self.cid = self.canvas.mpl_connect('button_press_event', self)
        
        # Create Table and add it to frameRight
        self.pyTable = PyTable(self.panedwindowRight)
        self.panedwindowRight.add(self.pyTable)
        
#        # Graphs
#        ttk.Label(self, text = "Graphs should come here").grid(row = 0, column = 3, rowspan=13, sticky = tk.NW+tk.SE, padx =5, pady=5)
#
#        # Data table
#        self.pyTable = PyTable(self)
#        self.pyTable.grid(row = 13, column = 3, sticky = tk.NW+tk.SE, padx =5, pady=5)
        
    def __call__(self, event):
        #print('click', event)
        if event.inaxes == self.ax1:
            self.ax1.set_facecolor('#FFFFE0')
            self.ax2.set_facecolor('#FFFFFF')
            self.ax3.set_facecolor('#FFFFFF')
            self.ax = self.ax1
        elif event.inaxes == self.ax2:
            self.ax1.set_facecolor('#FFFFFF')
            self.ax2.set_facecolor('#FFFFE0')
            self.ax3.set_facecolor('#FFFFFF')
            self.ax = self.ax2
        elif event.inaxes == self.ax3:
            self.ax1.set_facecolor('#FFFFFF')
            self.ax2.set_facecolor('#FFFFFF')
            self.ax3.set_facecolor('#FFFFE0')
            self.ax = self.ax3
        # Redraw
        self.canvas.draw()
                                  
#        if event.inaxes!=self.line.axes: return
#        self.xs.append(event.xdata)
#        self.ys.append(event.ydata)
#        self.line.set_data(self.xs, self.ys)
#        self.line.figure.canvas.draw()
        
# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyGraphs().mainloop()

