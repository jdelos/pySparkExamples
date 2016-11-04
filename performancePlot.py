# -*- coding: utf-8 -*-
"""
This script generates the memory perfomance plots used to analyse the 
memory usage from a web service monitored using nagios.

The script is very dependent on the data fromat however it can be used to
learn how to generate this plots.

The generated plots are written to html files containing javascripts allowing
to interact with the results. All this is provided using bokeh.

The performance plots combine a bar plot that shows the maximum memory usage
and the average memory usage. On top is ploted a boxplot to provide extra info
regarding the distributions of the measures.

Created on Wed Nov 02 20:26:49 2016

@author: julia.delos
"""


#Import modules 
from bokeh.plotting import figure, output_file, show
from bokeh.io import push_notebook
from bokeh.layouts import column, row, gridplot
import pandas as pd
import numpy as np
from numpy import pi



def addBoxPlot(table,plt):
    

def plotBarBoxPlot(table,plt_size,tstr):
    """
     This function takes a pandasdf with the following schema:
       CAT | MAX_VAL | AVG  | Q1 | Q2 | Q3| ICQ |Qmax | Qmin | [OL]
       
       where each column is defined as:
       CAT     --> Category used for the x acces 
       AVG     --> Average value
       MAX_VAL --> Maximum value 
       The following values define a box plot:
       Q1      --> First quatrile, 25% of the data is below this value.
       Q2      --> Second quartile (median), 50% of the data is below this value
       Q3      --> Third quartile, 75% of the data is blow this value.
       Qmin    --> Minumum value after removing the outliners
       Qmax    --> Maximum value after removing the outliners
       OL      --> String list containing the outliners values       
               
    """
    #Test if categories are strings 
    if type(table.iloc[0,0]) = str:
        
        p = figure(plot_width=plt_size[0],
               plot_height=plt_size[1],
               x_range=tmem['SrvNameInst'].tolist(),
               title=tstr)
        #In such a case string will be tilted for better reading       
        p.xaxis.major_label_orientation = pi/4
    else:
        p = figure(plot_width=plt_size[0],
               plot_height=plt_size[1],
               title=tstr)

    #Parse input table to variables
    x_cats = table.iloc[:,0].tolist()
    y_bar1 = table.iloc[:,1].tolist()
    y_bar2 = table.iloc[:,2].tolist()
    q1     = table.iloc[:,3].tolist()
    q2     = table.iloc[:,4].tolist()
    q3     = table.iloc[:,5].tolist()
    icq    = table.iloc[:,6].tolist()
    qmax   = table.iloc[:,7].tolist()
    qmin   = table.iloc[:,8].tolist()
    OL     = table.iloc[:,9].tolist()

    
    #Plot first bar plot       
    p.vbar(x=x_cats, width=0.5, bottom=0, top=y_bar1 )
    #Overlay another bar plot
    p.vbar(x=x_cats, color='#001234',width=0.5, bottom=0, top=y_bar2,alpha=0.7 )
    
    #Create a box between Q1 and Q3
    p.vbar(x=x_cats,width=0.75,bottom=q1,top=q3,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='green',fill_alpha=0.2)
    #Mark the median   
    p.vbar(x=[cat],width=0.75,bottom=q2,top=q2,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='green',fill_alpha=0.2)
    #Mark the bottom of the segment            
    p.vbar(x=[cat],width=0.75,bottom=qmin,top=qmin,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='black',fill_alpha=0.2)
    #Mark the top of the segment    
    p.vbar(x=[cat],width=0.75,bottom=qmax,top=qmax,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='black',fill_alpha=0.2)
    #Mark the            
    p.line(x=[cat,cat],y=[float(sel['Q3']/1024),float(sel['Qmax']/1024)],
               line_width=1,line_color='black')
               
    p.line(x=[cat,cat],y=[float(sel['Qmin']/1024),float(sel['Q1']/1024)],
               line_width=1,line_color='black')
        olStr = sel['OL'].tolist()[0]
        if len(olStr) > 2:
            ol_points = np.array(map(float,olStr[1:-1].split(',')))/1024
            cats = [cat] * len(ol_points)
            p.asterisk(x=cats,y=ol_points,color='red')
    return p     

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
            lst_prsd[i] = np.array(map(float,val[1:-1].split(',')))/1024
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



lyt1=[[400,400], [800,400],[800,400]]        

output_file("boxplot_1.html", title="boxplot.py example")
p1 = plotSubpot(tdata_frmt[tmem['type']>2],lyt1[0],'Biggest VM')

show(p1)

output_file("boxplot_2.html", title="boxplot.py example")

p2 = plotSubpot(tdata_frmt[tmem['type']==2].head(n=9),lyt1[1],'14 Gb VM')
p3 = plotSubpot(tdata_frmt[tmem['type']==2].tail(n=8),lyt1[2],'14 Gb VM')

show(column(p2,p3))     


output_file("boxplot_3.html", title="boxplot.py example")

p4 = plotSubpot(tdata_frmt[tmem['type']==1].head(n=11),lyt1[1],'7 Gb VM')
p5 = plotSubpot(tdata_frmt[tmem['type']==1].tail(n=10),lyt1[2],'7 Gb VM')

show(column(p4,p5))  

output_file("boxplot_4.html", title="boxplot.py example")

p6 = plotSubpot(tdata_frmt[tmem['type']==0].head(n=22),lyt1[1],'3.5 Gb VM')
p7 = plotSubpot(tdata_frmt[tmem['type']==0].tail(n=22),lyt1[2],'3.5 Gb VM')

show(column(p6,p7))  



