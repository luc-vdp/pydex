# -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Explore

@date: 2018-01-03

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sb
import statsmodels.api as sm

class PyExplore(ttk.Frame):
    def __init__(self, master = None, dataframes = None):
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        # Bind click event
        self.bind_all('<Button-1>', self.click)
        # Place the main frame on the grid
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        # Store dataframes
        self.dataframes = dataframes
        # Create widgets
        self.createWidgets()
        
    # Callback function - Clicked somewhere
    def click(self, event):
        try:
            if self.focus_get() == self.entryY:
                self.selectedVar.set('Y')
            elif self.focus_get() == self.entryX:
                self.selectedVar.set('X')
            elif self.focus_get() == self.entryS:
                self.selectedVar.set('S')
            elif self.focus_get() == self.entryG:
                self.selectedVar.set('G')
        except:
            pass
        
    def histogram(self):
        #Show properties frame for histogram (and hide others)
        self.frameHistogram.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.frameTrend.grid_forget()
        self.frameScatter.grid_forget()
        self.frameBargraph.grid_forget()
        self.frameBoxplot.grid_forget()
        # Clear labelExplanation
#        labelExplanation['text'] = ''
        # Show histogram
        self.ax.clear() 
        self.ax.set_xlabel(self.entryY.get())
        
        if self.cumulative.get():
            if len(self.entryBins.get()) > 0:
                sb.distplot(self.values(self.entryY).dropna(), bins=int(self.entryBins.get()), hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, ax=self.ax)
            else:
                sb.distplot(self.values(self.entryY).dropna(), hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, ax=self.ax)
        else:
            if len(self.entryBins.get()) > 0:
                sb.distplot(self.values(self.entryY).dropna(), bins=int(self.entryBins.get()), ax=self.ax)
            else:
                sb.distplot(self.values(self.entryY).dropna(), ax=self.ax)              
        self.ax.grid(True)
        self.canvas.show()  

    def trend(self):
        # Show properties frame for trend (and hide others)
        self.frameTrend.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.frameHistogram.grid_forget()
        self.frameScatter.grid_forget()
        self.frameBargraph.grid_forget()
        self.frameBoxplot.grid_forget()
#        # Clear labelExplanation
#        labelExplanation['text'] = ''
        # Show trend
        self.ax.clear() 
        self.ax.set_xlabel(self.entryX.get())
        self.ax.set_ylabel(self.entryY.get())
        if len(self.entryX.get()) > 0:
            self.ax.plot(self.values(self.entryX),self.values(self.entryY))
        else:
            self.ax.plot(eval(self.comboboxDataframes.get() + '.index.get_values()'),self.values(self.entryY))
            
        self.ax.grid(True)
        self.canvas.show()
        return

    def scatter(self):
        # Show properties frame for scatter graph (and hide others)
        self.frameScatter.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.frameHistogram.grid_forget()
        self.frameTrend.grid_forget()
        self.frameBargraph.grid_forget()
        self.frameBoxplot.grid_forget()
        # Clear labelExplanation
#        labelExplanation['text'] = ''
        # Show trend
        self.ax.clear() 
        self.ax.set_xlabel(self.entryX.get())
        self.ax.set_ylabel(self.entryY.get())
        if len(self.entryX.get()) > 0:
            self.ax.scatter(self.values(self.entryX),self.values(self.entryY))
            #Add bissectrice
            if self.bissectrice.get()==1:
                self.ax.plot(self.values(self.entryX),self.values(self.entryX),'k')
            #Add regression
            if self.regression.get()==1:
                y = self.values(self.entryY)
                x = self.values(self.entryX)
                s = (~y.isnull()) & (~x.isnull())
                y = y[s]
                x = x[s]
                X = sm.add_constant(x)
                model = sm.OLS(y,X).fit()
                self.ax.plot(x,model.predict(X),'r')
                #messagebox.showinfo("Regression info", model.summary())
#                labelExplanation['text'] = str(model.summary())
        else:
            self.ax.scatter(eval(self.comboboxDataframes.get() + '.index.get_values()'),self.values(self.entryY))
        self.ax.grid(True)
        self.canvas.show()
        return
        
    def bargraph(self):
        # Show properties frame for bar graph (and hide others)
        self.frameBargraph.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.frameHistogram.grid_forget()
        self.frameTrend.grid_forget()
        self.frameScatter.grid_forget()
        self.frameBoxplot.grid_forget()
        # Clear labelExplanation
#        labelExplanation['text'] = ''
        # Show trend
        self.ax.clear() 
        self.ax.set_xlabel(self.entryX.get())
        self.ax.set_ylabel(self.entryY.get())
        if len(self.entryX.get()) == 0:
            sb.barplot(y=self.values(self.entryY),ax=self.ax)
        elif len(self.entryY.get()) == 0:
            sb.barplot(x=self.values(self.entryY),ax=self.ax)
        elif len(self.values(self.entryX).unique()) < 100:
            sb.barplot(x=self.values(self.entryX),y=self.values(self.entryY),ax=self.ax)
        else:
            messagebox.showinfo('Warning','Too many categories')
        self.ax.grid(True)
        self.canvas.show()
        return
    
    def boxplot(self):
        # Show properties frame for boxplot (and hide others)
        self.frameBoxplot.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.frameHistogram.grid_forget()
        self.frameTrend.grid_forget()
        self.frameScatter.grid_forget()
        self.frameBargraph.grid_forget()
        # Clear labelExplanation
#        labelExplanation['text'] = ''
        # Show trend
        self.ax.clear() 
        self.ax.set_xlabel(self.entryX.get())
        self.ax.set_ylabel(self.entryY.get())
        if len(self.entryX.get()) == 0:
            sb.boxplot(y=self.values(self.entryY),notch=True,ax=self.ax)
        elif len(self.entryY.get()) == 0:
            sb.boxplot(x=self.values(self.entryY),notch=True,ax=self.ax)
        elif len(self.values(self.entryX).unique()) < 100:
            sb.boxplot(x=self.values(self.entryX),y=self.values(self.entryY),notch=True,ax=self.ax)
        else:
            messagebox.showinfo('Warning','Too many categories')
        self.ax.grid(True)
        self.canvas.show()
        return

    def showGraph(self):
        if self.graphtype.get() == 'H': 
            self.histogram()
        elif self.graphtype.get() == 'T': 
            self.trend()
        elif self.graphtype.get() == 'S': 
            self.scatter()
        elif self.graphtype.get() == 'R': 
            self.bargraph()
        elif self.graphtype.get() == 'B': 
            self.boxplot()

    def values(self, obj):
        if len(self.entryS.get()) > 0:
            # values, filtered
            data = eval('(' + obj.get() + ')[' + self.entryS.get() +']')
        else:
            # values, without filter
            data = eval('(' + obj.get() + ')')
        # Show error message if no values found
        if data.count() == 0:
            messagebox.showinfo('Error','No data found')
        # return data
        return data

    def listVars(self):
        if self.dataframes != None:
            self.comboboxDataframes['values'] = list(self.dataframes.keys())
        else:
            self.comboboxDataframes['values'] = [var for var in globals() if isinstance(eval(var), pd.core.frame.DataFrame)]
        
    def ListColumns(self, event):
        # Clear list
        self.listboxColumns.delete(0, tk.END)
        # Get selected dataframe name
        df = self.comboboxDataframes.get()
        if df != '':
            try:
                vars = self.dataframes[df].columns.values
                # Filtering listbox using search term from searchValue box 
                search_term = self.searchValue.get()
                for item in vars:
                    if search_term.lower() in item.lower():
                        self.listboxColumns.insert(tk.END, item)
            except:
#                vars = eval(self.comboboxDataframes.get()).columns.values
                self.dataframes = {}
                self.dataframes[df] = eval(self.comboboxDataframes.get())
                vars = self.dataframes[df].columns.values
                # Filtering listbox using search term from textSearch box 
                for item in vars:
                    #if search_term.lower() in item.lower():
                    self.listboxColumns.insert(tk.END, item)

    # Callback function - Add selected variable
    def SelectColumn(self, event):
        if self.selectedVar.get() == 'Y': 
            self.addVar(self.entryY)
        elif self.selectedVar.get() == 'X': 
            self.addVar(self.entryX)
        elif self.selectedVar.get() == 'S': 
            self.addVar(self.entryS)
            self.entryS.insert(tk.END, '>0')
        elif self.selectedVar.get() == 'G': 
            self.addVar(self.entryG)
        self.showGraph()
            
    # Add selected variable to selected text box
    def addVar(self,entry):
        varname = self.comboboxDataframes.get() + '.' + self.listboxColumns.get(self.listboxColumns.curselection())
        if len(entry.get()) == 0:
            # If nothing yet there, simply add the variable
            entry.insert(0, varname)
        elif entry.get()[-1] in ',+-*/':
            # If there is something already and it ends with , or + or - or * or /, then add the variable
            entry.insert(tk.END, ' ' + varname)
        elif entry.get()[-1] in ' ':
            # If there is something already and there is an extra space, then add the variable
            entry.insert(tk.END, varname)
        else:      
            # replace the existing text
            entry.delete(0, tk.END)
            entry.insert(0, varname)

    # Callback function - Show Python code
    def code(self):
        if self.buttonCode.cget('text') == 'Show Code':
            self.panedwindowMain.add(self.frameRight)
            self.buttonCode.configure(text = 'Hide Code')
        else:
            self.panedwindowMain.forget(self.frameRight)
            self.buttonCode.configure(text = 'Show Code')
                   
    def createWidgets(self):  
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

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
        #self.frameMiddle.rowconfigure(0, weight=1)
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
        self.listboxColumns.bind('<<ListboxSelect>>',self.SelectColumn)
        self.listboxColumns.grid(row=0, column = 0, sticky = tk.NE + tk.SW)

        # Search field
        ttk.Label(self.frameLeft, text = "Find").grid(row = 14, column = 0, sticky = tk.W, padx =5, pady=5)
        self.searchValue = tk.StringVar()
        self.searchValue.trace_add("write", self.ListColumns(None))      
        #self.entryFind = ttk.Entry(self, textvariable=self.searchValue, command=self.ListColumns(None))
        self.entryFind = ttk.Entry(self.frameLeft, textvariable=self.searchValue)
        self.entryFind.grid(row = 14, column = 1, columnspan=2, sticky=tk.W+tk.E, padx =5, pady=5)

        # Properties frame
        self.frameProperties = ttk.Frame(self.frameLeft, relief='ridge', borderwidth=4)
        self.frameProperties.grid(row = 15, column = 0, columnspan=3, sticky = tk.W, padx =5, pady=5)
        
        # Properties frame Histogram
        self.frameHistogram = ttk.Frame(self.frameProperties)
        self.frameHistogram.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.labelHistogram = ttk.Label(self.frameHistogram, text='number of bins:')
        self.labelHistogram.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entryBins = ttk.Entry(self.frameHistogram)
        self.entryBins.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.histtype = tk.StringVar() 
        self.histtype.set('H')
        self.optionHist   = ttk.Radiobutton(self.frameHistogram, text='Histogram ', variable=self.histtype, value='H', command=self.histogram)
        self.optionStairs = ttk.Radiobutton(self.frameHistogram, text='Stairs    ', variable=self.histtype, value='T', command=self.histogram)
        self.optionHist.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.optionStairs.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.cumulative = tk.IntVar()
        self.checkCumulative = ttk.Checkbutton(self.frameHistogram, text='Cumulative', variable=self.cumulative, command=self.histogram)
        self.checkCumulative.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
            
        self.percentage = tk.IntVar()
        self.checkPercentage = ttk.Checkbutton(self.frameHistogram, text='Percentage', variable=self.percentage, command=self.histogram)
        self.checkPercentage.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
            
        self.histtest = tk.IntVar()
        self.checkHisttest = ttk.Checkbutton(self.frameHistogram, text='t-test + F-test/Z-test', variable=self.histtest, command=self.histogram)
        self.checkHisttest.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Properties frame Trend 
        self.frameTrend = ttk.Frame(self.frameProperties)
        self.frameTrend.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.movingFunction = tk.IntVar()
        self.checkMoving = ttk.Checkbutton(self.frameTrend, text='Moving function', variable=self.movingFunction, command=self.trend)
        self.checkMoving.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.frameTrend.grid_forget()
        
        # Properties frame Scatter
        self.frameScatter = ttk.Frame(self.frameProperties)
        self.frameScatter.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.bissectrice = tk.IntVar()
        self.checkBissectrice = ttk.Checkbutton(self.frameScatter, text='Bissectrice', variable=self.bissectrice, command=self.scatter)
        self.checkBissectrice.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.regression = tk.IntVar()
        self.checkRegression = ttk.Checkbutton(self.frameScatter, text='Regression', variable=self.regression, command=self.scatter)
        self.checkRegression.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.frameScatter.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # Properties panel Bargraph
        self.frameBargraph = ttk.Frame(self.frameProperties)
        self.frameBargraph.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.labelAggregateFunction = ttk.Label(self.frameBargraph, text='Function')
        self.labelAggregateFunction.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.comboboxAggregateFunction = ttk.Combobox(self.frameBargraph)
        self.listFunctions = ['count','mean','sum','min','max','stdev']
        self.comboboxAggregateFunction['values'] = self.listFunctions
        self.comboboxAggregateFunction.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
                
        self.frameBargraph.grid_forget()
        
        # Properties panel Boxplot
        self.frameBoxplot = ttk.Frame(self.frameProperties)
        self.frameBoxplot.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.labelStep = ttk.Label(self.frameBoxplot, text='Step')
        self.labelStep.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entryStep = ttk.Entry(self.frameBoxplot)
        self.entryStep.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.frameBoxplot.grid_forget()
               
        
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
        self.fig = Figure(figsize=(10, 7), tight_layout=True)

        self.ax1 = self.fig.add_subplot(1,1,1)
        self.ax1.set_title('title 1')
        self.ax1.set_xlabel( 'X-axis' )
        self.ax1.set_ylabel( 'Y-axis' )
        #self.ax1.grid(True)
        
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
        #self.canvas.show()
        #self.canvas.draw()

        self.panedwindowMiddle.paneconfigure(self.canvas.get_tk_widget(), sticky=tk.NW+tk.SE)
        self.panedwindowMiddle.add(self.canvas.get_tk_widget())   

        #self.cid = self.canvas.mpl_connect('button_press_event', self)

        # Create frameSelection and add it to the paned window
        self.frameSelection = ttk.Frame(self.panedwindowMiddle, relief='ridge', borderwidth=4)
        # Make frameSelection stretchable
        self.frameSelection.rowconfigure(4, weight=1)
        self.frameSelection.columnconfigure(1, weight=1)
                
        # Y, X, Select and Group by labels
        self.selectedVar = tk.StringVar()
        self.selectedVar.set('Y')
        self.radiobuttonY = ttk.Radiobutton(self.frameSelection, text='Y       ', variable=self.selectedVar, value='Y')
        self.radiobuttonY.grid(row=0, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.radiobuttonX = ttk.Radiobutton(self.frameSelection, text='X       ', variable=self.selectedVar, value='X')
        self.radiobuttonX.grid(row=1, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.radiobuttonS = ttk.Radiobutton(self.frameSelection, text='Select  ', variable=self.selectedVar, value='S')
        self.radiobuttonS.grid(row=2, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.radiobuttonG = ttk.Radiobutton(self.frameSelection, text='Group by', variable=self.selectedVar, value='G')
        self.radiobuttonG.grid(row=3, column=0, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Y, X, Select and Group by entries
        self.entryY = ttk.Entry(self.frameSelection)
        self.entryY.grid(row=0, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.entryX = ttk.Entry(self.frameSelection)
        self.entryX.grid(row=1, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.entryS = ttk.Entry(self.frameSelection)
        self.entryS.grid(row=2, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        self.entryG = ttk.Entry(self.frameSelection)
        self.entryG.grid(row=3, column=1, sticky = tk.NE + tk.SW, padx =1, pady=1)
        
        # Text area for Info
        self.textInfo = ScrolledText(self.frameSelection, height=4) 
        self.textInfo.grid(row=4, column=0, columnspan=2, sticky = tk.NE + tk.SW, padx =1, pady=1)

        self.panedwindowMiddle.add(self.frameSelection, minsize=80)
        self.panedwindowMiddle.paneconfigure(self.frameSelection, sticky=tk.NW+tk.SE)

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