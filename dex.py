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

import statsmodels.api as sm

#from pandastable import Table

#import matplotlib
#matplotlib.use('Agg')

# See https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

# Main window
root = tk.Tk()
root.title('Python Data Exploration Tool - version 0.1')
root.geometry("1280x640")

# Define menu callbacks
def NewFile():
    messagebox.showinfo("New file","TO DO")
    
def OpenFile():
    filename = filedialog.askopenfilename()
    pos1 = filename.rfind('/')
    pos2 = filename.rfind('.')
    dfname = filename[pos1+1:pos2]
    extension = filename[pos2+1:-1]
    print(filename)    
    if (extension == 'xls') | (extension == 'xlsx'):
        exec("globals()['" + dfname +"'] = pd.read_excel('" + filename +"')")
    return
    messagebox.showinfo("File opened",dfname)
    
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
    vars = eval(comboboxDataframes.get()).columns.values
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
        textS.insert(tk.END, '>0')
    elif selectedVar.get() == 'G': 
        addVar(textG)
    
    showGraph()

# Add selected variable to selected text box
def addVar(entry):
    varname =comboboxDataframes.get() + '.' + listbox.get(listbox.curselection())
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
    
def showGraph():
    if graphtype.get() == 'H': 
        histogram()
    elif graphtype.get() == 'T': 
        trend()
    elif graphtype.get() == 'S': 
        scatter()
    elif graphtype.get() == 'R': 
        bargraph()
    elif graphtype.get() == 'B': 
        boxplot()
        
def histogram():
    #Show properties frame for histogram (and hide others)
    frameHistogram.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameTrend.pack_forget()
    frameScatter.pack_forget()
    frameBargraph.pack_forget()
    frameBoxplot.pack_forget()
    # Clear labelExplanation
    labelExplanation['text'] = ''
    # Show histogram
    ax.clear() 
    ax.set_xlabel(textY.get())
    
    if cumulative.get():
        if len(entryBins.get()) > 0:
            sb.distplot(values(textY).dropna(), bins=int(entryBins.get()), hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, ax=ax)
        else:
            sb.distplot(values(textY).dropna(), hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, ax=ax)
    else:
        if len(entryBins.get()) > 0:
            sb.distplot(values(textY).dropna(), bins=int(entryBins.get()), ax=ax)
        else:
            sb.distplot(values(textY).dropna(), ax=ax)
            
    ax.grid(True)
    canvas.show()    
    
def trend():
    # Show properties frame for trend (and hide others)
    frameTrend.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameScatter.pack_forget()
    frameBargraph.pack_forget()
    frameBoxplot.pack_forget()
    # Clear labelExplanation
    labelExplanation['text'] = ''
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    if len(textX.get()) > 0:
        ax.plot(values(textX),values(textY))
    else:
        ax.plot(eval(comboboxDataframes.get() + '.index.get_values()'),values(textY))
        
    ax.grid(True)
    canvas.show()
    return
    
def scatter():
    # Show properties frame for scatter graph (and hide others)
    frameScatter.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameTrend.pack_forget()
    frameBargraph.pack_forget()
    frameBoxplot.pack_forget()
    # Clear labelExplanation
    labelExplanation['text'] = ''
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    if len(textX.get()) > 0:
        ax.scatter(values(textX),values(textY))
        #Add bissectrice
        if bissectrice.get()==1:
            ax.plot(values(textX),values(textX),'k')
        #Add regression
        if regression.get()==1:
            y = values(textY)
            x = values(textX)
            s = (~y.isnull()) & (~x.isnull())
            y = y[s]
            x = x[s]
            X = sm.add_constant(x)
            model = sm.OLS(y,X).fit()
            ax.plot(x,model.predict(X),'r')
            #messagebox.showinfo("Regression info", model.summary())
            labelExplanation['text'] = str(model.summary())
    else:
        ax.scatter(eval(comboboxDataframes.get() + '.index.get_values()'),values(textY))
    ax.grid(True)
    canvas.show()
    return
    
def bargraph():
    # Show properties frame for bar graph (and hide others)
    frameBargraph.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameTrend.pack_forget()
    frameScatter.pack_forget()
    frameBoxplot.pack_forget()
    # Clear labelExplanation
    labelExplanation['text'] = ''
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    if len(textX.get()) == 0:
        sb.barplot(y=values(textY),ax=ax)
    elif len(textY.get()) == 0:
        sb.barplot(x=values(textY),ax=ax)
    elif len(values(textX).unique()) < 100:
        sb.barplot(x=values(textX),y=values(textY),ax=ax)
    else:
        messagebox.showinfo('Warning','Too many categories')
    ax.grid(True)
    canvas.show()
    return

def boxplot():
    # Show properties frame for boxplot (and hide others)
    frameBoxplot.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)
    frameHistogram.pack_forget()
    frameTrend.pack_forget()
    frameScatter.pack_forget()
    frameBargraph.pack_forget()
    # Clear labelExplanation
    labelExplanation['text'] = ''
    # Show trend
    ax.clear() 
    ax.set_xlabel(textX.get())
    ax.set_ylabel(textY.get())
    if len(textX.get()) == 0:
        sb.boxplot(y=values(textY),notch=True,ax=ax)
    elif len(textY.get()) == 0:
        sb.boxplot(x=values(textY),notch=True,ax=ax)
    elif len(values(textX).unique()) < 100:
        sb.boxplot(x=values(textX),y=values(textY),notch=True,ax=ax)
    else:
        messagebox.showinfo('Warning','Too many categories')
    ax.grid(True)
    canvas.show()
    return
    
def values(obj):
    if len(textS.get()) > 0:
        # values, filtered
        data = eval('(' + obj.get() + ')[' + textS.get() +']')
    else:
        # values, without filter
        data = eval('(' + obj.get() + ')')
    # Show error message if no values found
    if data.count() == 0:
        messagebox.showinfo('Error','No data found')
    # return data
    return data
    

# Left frame
frameLeft = ttk.Frame(root)
frameLeft.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y, padx=4, pady=2)

# Combobox to select a data frame
comboboxDataframes = ttk.Combobox(frameLeft)
variables= [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
comboboxDataframes['values'] = variables
comboboxDataframes.bind('<Return>',ListColumns)
comboboxDataframes.bind('<<ComboboxSelected>>',ListColumns)
comboboxDataframes.pack(pady=4)

# Properties panel 
frameProperties = ttk.Frame(frameLeft, relief='ridge', borderwidth=4)
frameProperties.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

# Properties panel Histogram
frameHistogram = ttk.Frame(frameProperties)
frameHistogram.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

labelHistogram = ttk.Label(frameHistogram, text='number of bins:')
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
checkRegression = ttk.Checkbutton(frameScatter, text='Regression', variable=regression, command=scatter)
checkRegression.pack(side=tk.TOP, anchor=tk.NW, padx=4, pady=2)

frameScatter.pack_forget()

# Properties panel Bargraph
frameBargraph = ttk.Frame(frameProperties)
frameBargraph.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

labelAggregateFunction = ttk.Label(frameBargraph, text='Function')
labelAggregateFunction.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=2)

comboboxAggregateFunction = ttk.Combobox(frameBargraph)
listFunctions = ['count','mean','sum','min','max','stdev']
comboboxAggregateFunction['values'] = listFunctions
comboboxAggregateFunction.pack()
        
frameBargraph.pack_forget()

# Properties panel Boxplot
frameBoxplot = ttk.Frame(frameProperties)
frameBoxplot.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.Y, pady=4)

labelStep = ttk.Label(frameBoxplot, text='Step')
labelStep.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=2)

entryStep = ttk.Entry(frameBoxplot)
entryStep.pack()

frameBoxplot.pack_forget()


# Textbox for searching a variable
textSearch = ttk.Entry(frameLeft)
textSearch.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.X, pady=4)

# listbox with scrollbar to select a variable (column in the data frame)
frameListbox = ttk.Frame(frameLeft, relief='ridge', borderwidth=1)
frameListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=4)

scrollbar = ttk.Scrollbar(frameListbox, orient=tk.VERTICAL)
listbox = tk.Listbox(frameListbox, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.bind('<<ListboxSelect>>',SelectColumn)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


# Frame for right side of the window
frameRight = ttk.Frame(root)
frameRight.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH, expand=True, pady=2)

# Frame with graph types
frameGraphtype = ttk.Frame(frameRight)
frameGraphtype.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X, expand=False, padx=4)

# Buttons
graphtype = tk.StringVar() 
graphtype.set('H')
optionHistogram = ttk.Radiobutton(frameGraphtype, text='Histogram ', variable=graphtype, value='H', command=histogram)
optionTrend     = ttk.Radiobutton(frameGraphtype, text='Trend     ', variable=graphtype, value='T', command=trend)
optionScatter   = ttk.Radiobutton(frameGraphtype, text='XY        ', variable=graphtype, value='S', command=scatter)
optionBargraph  = ttk.Radiobutton(frameGraphtype, text='Bar       ', variable=graphtype, value='R', command=bargraph)
optionBoxplot   = ttk.Radiobutton(frameGraphtype, text='Boxplot   ', variable=graphtype, value='B', command=boxplot)

buttonExit      = ttk.Button(frameGraphtype, text='Exit', command=exit_program)
buttonCode      = ttk.Button(frameGraphtype, text='Code', command=code)
buttonRefresh   = ttk.Button(frameGraphtype, text='Refresh', command=showGraph)


optionHistogram.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionTrend.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionScatter.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionBargraph.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)
optionBoxplot.pack(side=tk.LEFT, anchor=tk.NW, padx=4, pady=4)

buttonExit.pack(side=tk.RIGHT, anchor=tk.NE, padx=4, pady=4)
buttonCode.pack(side=tk.RIGHT, anchor=tk.NE, padx=4, pady=4)
buttonRefresh.pack(side=tk.RIGHT, anchor=tk.NE, padx=4, pady=4)

# Notebook (tab control)
notebook = ttk.Notebook(frameRight)
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
frameVars = ttk.Frame(frameRight, relief='ridge', borderwidth=4)
frameVars.pack(side=tk.TOP, anchor=tk.SW, fill=tk.X, expand=False, padx=4, pady=4)

# Frame for Y, X, Select and Group labels
frameLabels = ttk.Frame(frameVars)
frameLabels.pack(side=tk.LEFT, anchor=tk.SW, fill=tk.NONE, expand=False, pady=2)

# Y, X, Select and Group specification labels
selectedVar = tk.StringVar()
selectedVar.set('Y')
optionY = ttk.Radiobutton(frameLabels, text='Y       ', variable=selectedVar, value='Y'); optionY.pack(anchor=tk.W, padx=4, pady=2)
optionX = ttk.Radiobutton(frameLabels, text='X       ', variable=selectedVar, value='X'); optionX.pack(anchor=tk.W, padx=4, pady=2)
optionS = ttk.Radiobutton(frameLabels, text='Select  ', variable=selectedVar, value='S'); optionS.pack(anchor=tk.W, padx=4, pady=2)
optionG = ttk.Radiobutton(frameLabels, text='Group by', variable=selectedVar, value='G'); optionG.pack(anchor=tk.W, padx=4, pady=2)

# Frame Y, X, Select and Group Entry boxes
frameEntryboxes = ttk.Frame(frameVars)
frameEntryboxes.pack(side=tk.LEFT, anchor=tk.SW, fill=tk.X, expand=True, pady=2)

# Y, X, Select and Group specification
textY = ttk.Entry(frameEntryboxes, text='Y'); textY.pack(fill=tk.X, expand=True, padx=4, pady=2)
textX = ttk.Entry(frameEntryboxes, text='X'); textX.pack(fill=tk.X, expand=True, padx=4, pady=2)
textS = ttk.Entry(frameEntryboxes, text='Select'); textS.pack(fill=tk.X, expand=True, padx=4, pady=2)
textG = ttk.Entry(frameEntryboxes, text='Group by'); textG.pack(fill=tk.X, expand=True, padx=4, pady=2)

# Table at bottom
labelExplanation = ttk.Label(frameRight, text='Info', font='Consolas 10')
labelExplanation.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.BOTH, expand=False, padx=4)
# pt.show()

# 
root.bind('<Button-1>', click)
root.mainloop()    