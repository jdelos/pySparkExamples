# -*- coding: utf-8 -*-
"""
This script generates the memory perfomance plots used to analyse the 
memory usage from a web service monitored using nagios.

The generated plots are written to html files containing javascripts allowing
to interact with the results. All this is provided using bokeh.

The performance plots combine a bar plot that shows the maximum memory usage
and the average memory usage. On top is ploted a boxplot to provide extra info
regarding the distributions of the measures.

The ploting functions are implmented in the ploting_lib 

Created on Wed Nov 02 20:26:49 2016

@author: julia.delos
"""
#Import modules 
import pandas as pd
import numpy as np
from ploting_lib import plotBarBoxPlot
from bokeh.plotting import output_file, show
from bokeh.layouts import column


#load the services memory information it contains the average 
# and the inferred VM memory size
tmem = pd.read_csv('tmem.csv')
#Adding a column that sorts the 
tmem['type']=np.round(np.log2(tmem['tpmGb']/1.75)).astype(int) 


#Load the services box plot description
boxPrms = pd.read_csv('./boxPlots.csv')
#First data has to be transfomred from Mb to Gb
boxPrms.loc[:,'Q1':'Qmin'] = boxPrms.loc[:,'Q1':'Qmin']/1024

#The outliers column has been converted to a big string it has to be reparsed 
# into a list of values 
lst_prsd = [None] * len(boxPrms['OL'])
i=0
for val in boxPrms['OL']:
    if len(val) > 2:
            lst_prsd[i] = (np.array(map(float,val[1:-1].split(',')))/1024).tolist()
    i=i+1
#The parsed result is stored in the OL column   
boxPrms['OL'] = lst_prsd

#Merge both tables in a single one
tdata = pd.merge(tmem,boxPrms,how='left',left_on='SrvName',right_on='key')

#Shape the data within the necessary format structure for the plotting function
#  CAT | AVG | MAX_VAL | Q1 | Q2 | Q3| ICQ |Qmax | Qmin | [OL]
# That will be mapped as 
# SrvNameInst -->
# avgGb       --> 
tdata_frmt = tdata[['SrvNameInst','tpmGb','avgGb','Q1','Q2','Q3','IQR','Qmax','Qmin','OL']]


#Define two sizes for the plots
lyt1=[[400,500], [800,400]]        

table=tdata_frmt[tmem['type']>3]
table.iloc[:,0] = ['B2B','PROD','PAK','AGT']

#Plot the big VM
output_file("boxplot_1.html", title="boxplot.py example")
p1 = plotBarBoxPlot(table,lyt1[0],'Biggest VM',
                    plot_ol     = False,
                    bar_color   = ['#66CDAA','#329a77'],
                    box_width   = 0.25,
                    ol_mk_alpha = 0.3,
                    ol_mk_color = 'black',
                    ol_mk_size  = 3)
p1.xaxis.axis_label = "Service name"
p1.yaxis.axis_label = "memory [GiB]"
#p1.background_fill_color = "withe"
#p1.background_fill_alpha = 0.3
show(p1)

