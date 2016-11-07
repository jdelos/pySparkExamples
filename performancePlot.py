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
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.io import push_notebook
from bokeh.layouts import column, row, gridplot
import pandas as pd
import numpy as np
from numpy import pi
from math import ceil

def plotHBarOver(xs,ys_bot,ys_top,width=0.5,color=None,line_width=1,alpha=None,
                 plt=None,plt_size=[400,400],title=None):
    """
     Function returns a figure object of an overlay of horizontal bar plot.
     Input arguments:
        xs      --> Categories for the x axis. All layers share the same categories
                    Each element represents a layer of the box plot

        ys_bot  --> List with the bottom values. Each element
                    represents a layer of the box plot
                    [[y_bot1],[y_bot2]]

        ys_bot  --> List with the top values. Each element
                    represents a layer of the box plot
                    [[y_top1],[y_top2]]
        plt_size --> [width, high] of the plot Default: 400px X 400px
        width  --> Width of the bar. If scalar all layers will used the same. Default=0.5
        color  --> List with filling colors for the plots.
        line_width  --> List with the line with for each plot. If scalar all layers will used the same. Default=1
        alpha       --> Alpha value for the fill color. Default=1
        plt         --> Figure handler, if not given a new handler will be created.
                        If given the arguments plt_size, title are ignored.
        title       --> String defining the title of the plot.

    """
    if plt is None:
        # Test if categories are strings
        if type(table.iloc[0, 0]) == str:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       x_range=xs,
                       title=title)
            # In such a case string will be tilted for better reading
            plt.xaxis.major_label_orientation = pi / 4
        else:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       title=title)

    #Check that all arguments have the right length
    if len(ys_bot)==len(ys_top):
        n_layers = len(ys_bot)
    else:
        raise ValueError("ys_bot and ys_top have different size. Both have to be the same.")

    #Check the width parameters
    if type(width) == list:
        if len(width) != n_layers:
            raise ValueError("width: the argument list has the wrong length.")
    else:
        width = [width]*n_layers

    #Define a generic color list
    color_def = ['DarkBlue', 'DarkGreen', 'DarkCyan', 'DarkSlateGray', 'DarkRed', 'DarkViolet','DarkGrey']
    n_colors = float(len(color_def))

    #Check color parameter
    if color is None:
        color = (color_def* int(ceil(n_layers/n_colors)))[:n_layers] #Generate a color list
    elif type(color) == list:
        if len(color) != n_layers:
            raise ValueError("color: the argument list has the wrong length.")


    # Check the line_width parameters
    if type(line_width) == list:
        if len(line_width) != n_layers:
            raise ValueError("line_width: the argument list has the wrong length.")
    else:
        line_width = [line_width] * n_layers

    # Check the line_width parameters
    if (alpha is not None) and len(alpha) != n_layers:
        raise ValueError("alpha: the argument list has the wrong length.")

    #Generate the plots
    for idx in range(0,n_layers):
        # Plot first bar plot
        plt.vbar(x=xs, width=width[idx],bottom=ys_bot[idx], top=ys_top[idx],
                color=color[idx],line_width=line_width[idx],alpha=alpha[idx])

    return plt


def plotBoxPlot(x_cats,q1,q2,q3,qmin,qmax,OL,
                 box_alpha_fill=1,box_color_fill='green',
                 box_line_width=1, box_line_color='black',
                 box_width=0.5,
                 wsk_color='black', wsk_line_width=1, wsk_limits_width=0.25,
                 ol_point_color='red',
                 plt=None,plt_size=[400,400],title=None):
    """
     Function returns a figure object of an overlay of horizontal bar plot.
     Input arguments:
        xs      --> Categories for the x axis. All layers share the same categories
                    Each element represents a layer of the box plot

        q1      -->  First quartile.
        q2      -->  Second quartile, the same as the median.
        q3      -->  Third quartile.
        qmin    -->  Minimum value from the dataset without the outliners
        qmax    -->  Maximum value from the dataset without the outliners
        OL      -->  Outliners array, None in case if no outliners

        Box design arguments:
        box_alpha_fill --> Value for the box filling. Default: 1 (opaque)
        box_color_fill --> Color used to fill the box. Default green.
                           Color can be defined by the standard CSS HTML color name of HTML code.
        box_line_width --> Line with for the box. Default 1
        box_line_width --> Color for the box lines. Default 'black'
        box_width      --> Width of the box plot. Default=0.5

        Whiskers design arguments:
        wsk_color      --> Color for the whiskers lines. Default 'black'
        wsk_line_width --> Width for the whiskers lines. Default 1
        wsk_limits_width --> Width of the limit markers for the whiskers. Default 0.25.

        Outliner points design arguments:
        ol_point_color --> Color for the outliner points. Default 'red'

        plt         --> Figure handler, if not given a new handler will be created.
                        If given the arguments plt_size, title are ignored.
        title       --> String defining the title of the plot.
        plt_size    --> [width, high] of the plot Default: 400px X 400px

    """

    if plt is None:
        # Test if categories are strings
        if type(table.iloc[0, 0]) == str:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       x_range=xs,
                       title=title)
            # In such a case string will be tilted for better reading
            plt.xaxis.major_label_orientation = pi / 4
        else:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       title=title)

    #Generate the main box
    # Create a box between Q1 and Q3
    plt.vbar(x=x_cats, width=box_width, bottom=q1, top=q3,
             line_width=box_line_width, line_color=box_line_color,
             fill_color=box_color_fill, fill_alpha=box_alpha_fill)
    # Mark the median
    plt.vbar(x=x_cats, width=box_width, bottom=q2, top=q2,
             line_width=box_line_width, line_color=box_line_color,
             fill_color=box_color_fill, fill_alpha=box_alpha_fill)

    # Genertare the whiskers
    # Mark the bottom limit
    plt.vbar(x=x_cats, width=wsk_limits_width, bottom=qmin, top=qmin,
             line_width=wsk_line_width, line_color=wsk_color,
             fill_color=wsk_color)
    # Mark the top of the segment
    plt.vbar(x=x_cats, width=wsk_limits_width, bottom=qmax, top=qmax,
             line_width=wsk_line_width, line_color=wsk_color,
             fill_color=wsk_color)

    # Generate the multiplot lines for the whiskers
    xs_cats = [[x_cat, x_cat] for x_cat in x_cats]
    ys_whsk_top = [[q3[i], qmax[i]] for i in range(0, len(q3))]
    ys_whsk_bot = [[qmin[i], q1[i]] for i in range(0, len(q3))]

    plt.multi_line(xs=xs_cats, ys=ys_whsk_top,
                   line_width=wsk_line_width, color=wsk_color)
    plt.multi_line(xs=xs_cats, ys=ys_whsk_bot,
                   line_width=wsk_line_width, color=wsk_color)

    # Generate the lists to plot all the outliners
    ol_pts = []
    ol_cats = []
    idx = 0
    for ol_points in OL:
        if ol_points:
            ol_pts = ol_pts + ol_points
            ol_cats = ol_cats + [x_cats[idx]] * len(ol_points)
    plt.asterisk(x=ol_cats, y=ol_pts, color=ol_point_color)

    # Return the figure object
    return plt


def plotBarBoxPlot(table,plt_size,tstr,plt=None):
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

    if plt is None:
        # Test if categories are strings
        if type(table.iloc[0, 0]) == str:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       x_range=x_cats,
                       title=tstr)
            # In such a case string will be tilted for better reading
            plt.xaxis.major_label_orientation = pi / 4
        else:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       title=tstr)


    #Generate the overlay boxPlot
    plt = plotHBarOver(plt=plt,xs=x_cats,width=0.5,ys_bot=[[0]*len(x_cats),[0]*len(x_cats)],
                       ys_top=[y_bar1,y_bar2],alpha=[1, 0.7],color=['#1F77B4','#001234'])

    #Create a box between Q1 and Q3
    plt.vbar(x=x_cats,width=0.75,bottom=q1,top=q3,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='green',fill_alpha=0.2)
    #Mark the median
    plt.vbar(x=x_cats,width=0.75,bottom=q2,top=q2,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='green',fill_alpha=0.2)

    #Mark the bottom of the segment
    plt.vbar(x=x_cats,width=0.5,bottom=qmin,top=qmin,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='black',fill_alpha=0.2)
    #Mark the top of the segment
    plt.vbar(x=x_cats,width=0.5,bottom=qmax,top=qmax,
               line_width=1,line_color="black",line_alpha=1,
               fill_color='black',fill_alpha=0.2)

    #Generate the multiplot lines for the whiskers
    xs_cats = [ [x_cat,x_cat] for x_cat in x_cats ]
    ys_whsk_top = [ [  q3[i], qmax[i]] for i in range(0,len(q3))]
    ys_whsk_bot = [ [qmin[i],   q1[i]] for i in range(0,len(q3))]

    plt.multi_line(xs=xs_cats,ys=ys_whsk_top,
               line_width=1,color='black')
    plt.multi_line(xs=xs_cats,ys=ys_whsk_bot,
                 line_width=1,color='black')

    #Generate the lists to plot all the outliners
    ol_pts=[]
    ol_cats=[]
    idx=0
    for ol_points in OL:
        if ol_points:
            ol_pts = ol_pts+ol_points
            ol_cats = ol_cats+[x_cats[idx]]*len(ol_points)
    plt.asterisk(x=ol_cats,y=ol_pts,color='red')
    return plt

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



lyt1=[[400,400], [800,400],[800,400]]        

output_file("boxplot_1.html", title="boxplot.py example")
p1 = plotBarBoxPlot(tdata_frmt[tmem['type']>3],lyt1[0],'Biggest VM')

show(p1)

output_file("boxplot_2.html", title="boxplot.py example")

p2 = plotBarBoxPlot(tdata_frmt[tmem['type']==3].head(n=8),lyt1[1],'14 Gb VM')
p3 = plotBarBoxPlot(tdata_frmt[tmem['type']==3].tail(n=8),lyt1[2],'14 Gb VM')

show(column(p2,p3))


output_file("boxplot_3.html", title="boxplot.py example")

p4 = plotBarBoxPlot(tdata_frmt[tmem['type']==2].head(n=11),lyt1[1],'7 Gb VM')
p5 = plotBarBoxPlot(tdata_frmt[tmem['type']==2].tail(n=10),lyt1[2],'7 Gb VM')

show(column(p4,p5))

output_file("boxplot_4.html", title="boxplot.py example")

p6 = plotBarBoxPlot(tdata_frmt[tmem['type']==1],lyt1[1],'3.5 Gb VM')
p7 = plotBarBoxPlot(tdata_frmt[tmem['type']==0],lyt1[2],'3.5 Gb VM')

show(column(p6,p7))



