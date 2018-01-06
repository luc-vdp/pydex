# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:19:14 2017

@author: a0113945
"""
#import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import PyExplore as PyExplore

#def explore():
#    app = PyExplore(dataframes=globals()) 
#    #app.master.title('PyExplore - Python Data Exploration Tool - version 0.1')
#    app.mainloop()  
    
def histogram(x, sel=None, cumulative=False, bins=0, ax=None):
    '''   
    Draws a histogram (a distribution plot)
    
    20178-12-01 - luc.vandeputte@arcelormittal.com
    
    Examples: px.histogram(d.C_bta_r)
              px.histogram(d.C_bta_r, sel=(d.C_bta_r<1000))
              px.histogram(d.C_bta_r, sel=(d.C_bta_r<1000), bins=5)
              px.histogram(d.C_bta_r, sel=(d.C_bta_r<1000), bins=range(0,1000,100))
              
    '''
    #ax.clear() 
    #ax.set_xlabel(x)
    if type(sel)==pd.Series:
        x = x[sel]

    if cumulative:
        if bins > 0:
            if ax != None:
                sb.distplot(x.dropna(), bins=bins, hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, ax=ax)
            else:
                sb.distplot(x.dropna(), bins=bins, hist_kws={'cumulative': True}, kde_kws={'cumulative': True})
        else:
            if ax != None:
                sb.distplot(x.dropna(), hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, ax=ax)
            else:
                sb.distplot(x.dropna(), hist_kws={'cumulative': True}, kde_kws={'cumulative': True})
    else:
        if type(bins)==range:
            if ax != None:
                sb.distplot(x.dropna(), bins=bins, ax=ax)
            else:
                sb.distplot(x.dropna(), bins=bins)
        elif (type(bins)==int) & (bins>1):
            if ax != None:
                sb.distplot(x.dropna(), bins=bins, ax=ax)
            else:
                sb.distplot(x.dropna(), bins=bins)
        else:
            if ax != None:
                sb.distplot(x.dropna(), ax=ax)
            else:
                sb.distplot(x.dropna())
    
    if ax != None:
        ax.grid(True)
    else:
        plt.grid(True)       

   