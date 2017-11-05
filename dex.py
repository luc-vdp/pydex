# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:05:47 2017

@author: luc.vandeputte@arcelormittal.com
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog

import pandas as pd
import seaborn as sb

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#from pandastable import Table

#import matplotlib
#matplotlib.use('Agg')

# See https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

# Main window
root = tk.Tk()
root.title('Python Data Exploration Tool')
root.geometry("1280x640")

# Define menu callbacks
def NewFile():
    messagebox.showinfo("New file","TO DO")
    
def OpenFile():
    name = filedialog.askopenfilename()
    messagebox.showinfo("File to open",name)
    
def Preferences():
    messagebox.showinfo("Preferences","TO DO")
    
def RenameDataframe():
    messagebox.showinfo("Rename Dataframe","TO DO")
    
def About():
    messagebox.showinfo("About pydex","Python Data Exploration Tool")

# Add menu
menuMain = tk.Menu(root)
root.config(menu=menuMain)

menuFile = tk.Menu(menuMain, tearoff=False)
menuMain.add_cascade(label="File", menu=menuFile)
menuFile.add_command(label="New", command=NewFile)
menuFile.add_command(label="Open...", command=OpenFile)
menuFile.add_separator()
menuFile.add_command(label="Exit", command=root.destroy)

menuEdit = tk.Menu(menuMain, tearoff=False)
menuMain.add_cascade(label="Edit", menu=menuEdit)
menuEdit.add_command(label="Rename...", command=RenameDataframe)

menuTools = tk.Menu(menuMain, tearoff=False)
menuMain.add_cascade(label="Tools", menu=menuTools)
menuTools.add_command(label="Preferences...", command=Preferences)

menuHelp = tk.Menu(menuMain, tearoff=False)
menuMain.add_cascade(label="Help", menu=menuHelp)
menuHelp.add_command(label="About...", command=About)

# Callback function - Handle exceptions
def handle_exception(exception, value, traceback):
    messagebox.showinfo('Error',value)

# setup custom exception handling
root.report_callback_exception=handle_exception

# Callback function - Exit the program
def exit_program():
    root.destroy()
        
# Callback function - Show Python code (for the moment just testing)
def code():
    messagebox.showinfo('titel','test')
    
# Callback function - Clicked somewhere
def click(event):
    print(root.focus_get())
    
    if root.focus_get() == textY:
        selectedVar.set('Y')
    elif root.focus_get() == textX:
        selectedVar.set('X')
    elif root.focus_get() == textS:
        selectedVar.set('S')
    elif root.focus_get() == textG:
        selectedVar.set('G')
            
    
# Callback function - Show list of colums in selected data frame
def ListColumns(evt):
    listbox.delete(0,tk.END)
    vars = eval(combobox.get()).columns.values
    for var in vars:
        listbox.insert(tk.END, var)
    
# Callback function - Add selected variable
def SelectColumn(evt):
    if selectedVar.get() == 'Y': 
        addVar(textY)
    elif selectedVar.get() == 'X': 
        addVar(textX)
    elif selectedVar.get() == 'S': 
        addVar(textS)
    elif selectedVar.get() == 'G': 
        addVar(textG)
    
    showGraph()
    
def addVar(Entry):
    varname =combobox.get() + '.' + listbox.get(listbox.curselection())
    if len(Entry.get()) == 0:
        Entry.insert(0, varname)
    elif Entry.get()[-1] in ',+-*/':
        Entry.insert(tk.END, ' ' + varname)
    elif Entry.get()[-1] in ' ':
        Entry.insert(tk.END, varname)
    else:      
        Entry.delete(0, tk.END)
        Entry.insert(0, varname)
    
def showGraph():
    if graphtype.get() == 'H': 
        histogram()
    elif graphtype.get() == 'T': 
        trend()
    elif graphtype.get() == 'S': 
        scatter()
    elif graphtype.get() == 'B': 
        boxplot()
        
def histogram():
    #Show properties frame for histogram (and hide others)
    frameHistogram.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameTrend.pack_forget()
    frameScatter.pack_forget()
    frameBoxplot.pack_forget()
    # Show histogram
    ax.clear() 
    ax.set_xlabel(textY.get())
    #ax.hist(eval(textY.get()))
    #sb.distplot(eval('(' + textY.get() + ').dropna()'), ax=ax)
    sb.distplot(values(textY), ax=ax)
    ax.grid(True)
    canvas.show()    
    
def trend():
    # Show properties frame for trend (and hide others)
    frameTrend.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameScatter.pack_forget()
    frameBoxplot.pack_forget()
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    ax.plot(eval(textX.get()),eval(textY.get()))
    ax.grid(True)
    canvas.show()
    return
    
def scatter():
    # Show properties frame for scatter graph (and hide others)
    frameScatter.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameTrend.pack_forget()
    frameBoxplot.pack_forget()
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    ax.scatter(eval(textX.get()),eval(textY.get()))
    ax.grid(True)
    canvas.show()
    return
    
def boxplot():
    # Show properties frame for boxplot (and hide others)
    frameBoxplot.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameTrend.pack_forget()
    frameScatter.pack_forget()
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    #ax.boxplot(eval(textY.get()),eval(textX.get()))
    sb.boxplot(x=eval('(' + textX.get() + ').dropna()'),y=eval('(' + textY.get() + ').dropna()'),notch=True,ax=ax)
    ax.grid(True)
    canvas.show()
    return
    
def values(obj):
    data = eval('(' + obj.get() + ').dropna()')
    if data.count() == 0:
        messagebox.showinfo('Error','No data found')

    return data
    

# Left frame
leftFrame = ttk.Frame(root)
leftFrame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y, padx=4, pady=2)

# Combobox to select a data frame
combobox = ttk.Combobox(leftFrame)
variables= [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
combobox['values'] = variables
combobox.bind('<Return>',ListColumns)
combobox.bind('<<ComboboxSelected>>',ListColumns)
combobox.pack(pady=4)

# Properties panel 
frameProperties = ttk.Frame(leftFrame, relief='ridge', borderwidth=4)
frameProperties.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

# Properties panel Histogram
frameHistogram = ttk.Frame(frameProperties)
frameHistogram.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

labelHistogram = ttk.Label(frameHistogram, text='bins(min:step:max)')
labelHistogram.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)

entryBins = ttk.Entry(frameHistogram)
entryBins.pack()

histtype = tk.StringVar() 
histtype.set('H')
optionHist   = ttk.Radiobutton(frameHistogram, text='Histogram ', variable=histtype, value='H', command=histogram)
optionStairs = ttk.Radiobutton(frameHistogram, text='Stairs    ', variable=histtype, value='T', command=histogram)
optionHist.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)
optionStairs.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)

cumulative = tk.IntVar()
checkCumulative = ttk.Checkbutton(frameHistogram, text='Cumulative', variable=cumulative, command=histogram)
checkCumulative.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)
    
percentage = tk.IntVar()
checkPercentage = ttk.Checkbutton(frameHistogram, text='Percentage', variable=percentage, command=histogram)
checkPercentage.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)
    
histtest = tk.IntVar()
checkHisttest = ttk.Checkbutton(frameHistogram, text='t-test + F-test/Z-test', variable=histtest, command=histogram)
checkHisttest.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)
    
# Properties panel Trend
frameTrend = ttk.Frame(frameProperties)
frameTrend.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

movingFunction = tk.IntVar()
checkMoving = ttk.Checkbutton(frameTrend, text='Moving function', variable=movingFunction, command=trend)
checkMoving.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)

frameTrend.pack_forget()

# Properties panel Scatter
frameScatter = ttk.Frame(frameProperties)
frameScatter.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

bissectrice = tk.IntVar()
checkBissectrice = ttk.Checkbutton(frameScatter, text='Bissectrice', variable=bissectrice, command=scatter)
checkBissectrice.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)

regression = tk.IntVar()
checkRegression = ttk.Checkbutton(frameScatter, text='Regression', variable=bissectrice, command=scatter)
checkRegression.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)

frameScatter.pack_forget()

# Properties panel Boxplot
frameBoxplot = ttk.Frame(frameProperties)
frameBoxplot.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

labelStep = ttk.Label(frameBoxplot, text='Step')
labelStep.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=2)

entryStep = ttk.Entry(frameBoxplot)
entryStep.pack()

frameBoxplot.pack_forget()


# Textbox for searching a variable
textEntry = ttk.Entry(leftFrame)
textEntry.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.X, pady=4)

# listbox with scrollbar to select a variable (column in the data frame)
frameListbox = ttk.Frame(leftFrame, relief='ridge', borderwidth=1)
frameListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=4)

scrollbar = ttk.Scrollbar(frameListbox, orient=tk.VERTICAL)
listbox = tk.Listbox(frameListbox, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.bind('<<ListboxSelect>>',SelectColumn)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


#listbox.bind('<Return>',SelectColumn)


# Right frame
rightFrame = ttk.Frame(root)
rightFrame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH, expand=True, pady=2)

# Button frame
graphtypeFrame = ttk.Frame(rightFrame)
graphtypeFrame.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X, expand=False, padx=4)

# Buttons
graphtype = tk.StringVar() 
graphtype.set('H')
optionHistogram = ttk.Radiobutton(graphtypeFrame, text='Histogram ', variable=graphtype, value='H', command=histogram)
optionTrend     = ttk.Radiobutton(graphtypeFrame, text='Trend     ', variable=graphtype, value='T', command=trend)
optionScatter   = ttk.Radiobutton(graphtypeFrame, text='XY        ', variable=graphtype, value='S', command=scatter)
optionBoxplot   = ttk.Radiobutton(graphtypeFrame, text='Boxplot   ', variable=graphtype, value='B', command=boxplot)

buttonExit      = ttk.Button(graphtypeFrame, text='Exit', command=exit_program)
buttonCode      = ttk.Button(graphtypeFrame, text='Code', command=code)
buttonRefresh   = ttk.Button(graphtypeFrame, text='Refresh', command=showGraph)


optionHistogram.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionTrend.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionScatter.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionBoxplot.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)

buttonExit.pack(side=tk.RIGHT, anchor=tk.NE, padx=4, pady=4)
buttonCode.pack(side=tk.RIGHT, anchor=tk.NE, padx=4, pady=4)
buttonRefresh.pack(side=tk.RIGHT, anchor=tk.NE, padx=4, pady=4)

# Notebook (tab control)
notebook = ttk.Notebook(rightFrame)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
notebook.add(frame1, text='Page 1', )
notebook.add(frame2, text='Page 2')
notebook.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=True, padx=4)

#fig = Figure(figsize=(6, 4), dpi=100 )
fig = Figure(figsize=(6, 4))
ax = fig.add_axes( (.06, .10, .88, .80), frameon=True)
ax.set_xlabel( 'X-axis' )
ax.set_ylabel( 'Y-axis' )
ax.grid(True)
    
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.show()
#     
#toolbar = NavigationToolbar2TkAgg(canvas, frame1)
#toolbar.pack(side=tk.TOP)
#toolbar.update()

# Frame for Y, X, Select and Group specification
frameVars = ttk.Frame(rightFrame, relief='ridge', borderwidth=4)
frameVars.pack(side=tk.LEFT, anchor=tk.SW, fill=tk.X, expand=True, padx=4, pady=4)


# Frame for Y, X, Select and Group labels
labelsFrame = ttk.Frame(frameVars)
labelsFrame.pack(side=tk.LEFT, anchor=tk.SW, fill=tk.NONE, expand=False, pady=2)

# Y, X, Select and Group specification labels
selectedVar = tk.StringVar()
selectedVar.set('Y')
optionY = ttk.Radiobutton(labelsFrame, text='Y       ', variable=selectedVar, value='Y'); optionY.pack(anchor=tk.W, padx=4, pady=2)
optionX = ttk.Radiobutton(labelsFrame, text='X       ', variable=selectedVar, value='X'); optionX.pack(anchor=tk.W, padx=4, pady=2)
optionS = ttk.Radiobutton(labelsFrame, text='Select  ', variable=selectedVar, value='S'); optionS.pack(anchor=tk.W, padx=4, pady=2)
optionG = ttk.Radiobutton(labelsFrame, text='Group by', variable=selectedVar, value='G'); optionG.pack(anchor=tk.W, padx=4, pady=2)

# Frame Y, X, Select and Group Entry boxes
textEntryFrame = ttk.Frame(frameVars)
textEntryFrame.pack(side=tk.LEFT, anchor=tk.SW, fill=tk.X, expand=True, pady=2)

# Y, X, Select and Group specification
textY = ttk.Entry(textEntryFrame, text='Y'); textY.pack(fill=tk.X, expand=True, padx=4, pady=2)
textX = ttk.Entry(textEntryFrame, text='X'); textX.pack(fill=tk.X, expand=True, padx=4, pady=2)
textS = ttk.Entry(textEntryFrame, text='Select'); textS.pack(fill=tk.X, expand=True, padx=4, pady=2)
textG = ttk.Entry(textEntryFrame, text='Group by'); textG.pack(fill=tk.X, expand=True, padx=4, pady=2)

# Table at bottom
# pt = Table(rightFrame)
# pt.show()

# 
root.bind('<Button-1>', click)
root.mainloop()    