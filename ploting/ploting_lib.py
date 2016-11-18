# -*- coding: utf-8 -*-
"""

ploting_lib is a collection of functions that allows to overlay box plots 
and bar plots.



Created on Mon Nov 07 16:06:16 2016

@author: Julia Delos
@mail:   julia.delos@ict.nl
"""

from bokeh.plotting import figure
from numpy import pi
from math import ceil

def plotHBarOver(xs,ys_bot,ys_top,width=0.5,color=None,line_width=1,alpha=None,
                 plt=None,plt_size=[400,400],title=None,legend=['Total','Mean'],
                 ):
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
    # Check arguments
    if type(xs) == list:
        n_cats = len(xs)
    else:
        raise ValueError("xs is not a list")

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

    if plt is None:
        # Test if categories are strings
        if type(xs[0]) == str:
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


    #Generate the plots
    for idx in range(0,n_layers):
        # Plot first bar plot
        plt.vbar(x=xs, width=width[idx],bottom=ys_bot[idx], top=ys_top[idx],
                color=color[idx],line_width=line_width[idx],alpha=alpha[idx],
                line_alpha=0,legend=legend[idx])

    return plt


def plotBoxPlot(x_cats,q1,q2,q3,qmin,qmax,OL,
                 plot_ol=False,
                 box_alpha_fill=1,
                 box_line_width=1.5, 
                 box_line_color='#555555',
                 box_width=0.35,
                 wsk_color='#555555', 
                 wsk_line_width=1.5, 
                 wsk_limits_width=0.25,
                 box_top_fill='#fbaf5d',
                 box_low_fill='#fff568',
                 ol_mk_alpha=0.3,
                 ol_mk_color='black',
                 ol_mk_size=10,
                 plt=None,plt_size=[400,400],title=None):
    """
     Function returns a figure object of an overlay of horizontal bar plot.
     Input arguments:
        x_cats  --> Categories for the x axis. All layers share the same categories
                    Each element represents a layer of the box plot

        q1      -->  First quartile.
        q2      -->  Second quartile, the same as the median.
        q3      -->  Third quartile.
        qmin    -->  Minimum value from the dataset without the outliners
        qmax    -->  Maximum value from the dataset without the outliners
        OL      -->  Outliners array, None in case if no outliners

        Box design arguments:
        box_alpha_fill --> Value for the box filling. Default: 1 (opaque)
        box_low_fill  --> Lower box (Q1-Q2) fill color. Default Yellow 
        box_top_fill -->  Top box (Q2-Q3) fill color. Default Light orange 
                           Color used to fill the box. Default green.
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

    #Check arguments
    if type(x_cats) == list:
        n_cats = len(x_cats)
    else:
        raise ValueError("x_cats is not a list")

    if type(q1) == list:
        if len(q1) != n_cats:
            raise ValueError("q1 has the wrong length")
    else:
        raise ValueError("q1 is not a list")

    if type(q2) == list:
        if len(q2) != n_cats:
            raise ValueError("q2 has the wrong length")
    else:
        raise ValueError("q2 is not a list")

    if type(q3) == list:
        if len(q3) != n_cats:
            raise ValueError("q3 has the wrong length")
    else:
        raise ValueError("q3 is not a list")
    if type(qmin) == list:
        if len(qmin) != n_cats:
            raise ValueError("qmin has the wrong length")
    else:
        raise ValueError("qmin is not a list")

    if type(qmax) == list:
        if len(qmax) != n_cats:
            raise ValueError("qmax has the wrong length")
    else:
        raise ValueError("qmax is not a list")

    if type(OL) == list:
        if len(OL) != n_cats:
            raise ValueError("OL has the wrong length")
    else:
        raise ValueError("OL is not a list")

    if plt is None:
        # Test if categories are strings
        if type(x_cats[0]) == str:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       x_range=xs,
                       title=title)
            # In such a case string will be tilted for better reading
            plt.xaxis.major_label_orientation = pi / 6
        else:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       title=title)

    if plot_ol == True:
        #Generate the lists to plot all the outliners
        ol_pts = []
        ol_cats = []
        idx = 0
        for ol_points in OL:
            if ol_points:
                ol_pts = ol_pts + ol_points
                ol_cats = ol_cats + [x_cats[idx]] * len(ol_points)
            idx += 1
        plt.scatter(x=ol_cats, y=ol_pts,
                    marker='o',
                    alpha=ol_mk_alpha,
                    fill_color=ol_mk_color,
                    size=ol_mk_size,
                    line_alpha=0)

    #Generate the main box
    # Create the lower box between Q1 and Q2
    plt.vbar(x=x_cats, width=box_width, bottom=q1, top=q2,
             line_width=box_line_width, line_color=box_line_color,
             fill_color=box_low_fill, fill_alpha=box_alpha_fill)

    # Mark the median
    plt.vbar(x=x_cats, width=box_width, bottom=q2, top=q3,
             line_width=box_line_width, line_color=box_line_color,
             fill_color=box_top_fill, fill_alpha=box_alpha_fill)

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



    # Return the figure object
    return plt


def plotBarBoxPlot(table,plt_size,tstr,plt=None,bar_color=['#90EE90','#20B2AA'],
                         plot_ol = False,
                         box_alpha_fill=1,
                         box_width=0.5,
                         wsk_limits_width=0.15,
                         ol_mk_alpha=0.3,
                         ol_mk_color='black',
                         ol_mk_size=10):
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
       bar_color --> 
               
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

    #Generate a figure to add the plots
    if plt is None:
        # Test if categories are strings
        if type(table.iloc[0, 0]) == str:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       x_range=x_cats,
                       title=tstr)
            # In such a case string will be tilted for better reading
            plt.xaxis.major_label_orientation = pi / 6
        else:
            plt = figure(plot_width=plt_size[0],
                       plot_height=plt_size[1],
                       title=tstr)


    #Generate the overlay boxPlot
    plt = plotHBarOver(plt=plt, #Pass the figure handler to add the plots
                       xs=x_cats,width=0.5,ys_bot=[[0]*len(x_cats),[0]*len(x_cats)],
                       ys_top=[y_bar1,y_bar2],alpha=[1, 0.7],color=bar_color)

    #Create
    plt = plotBoxPlot(plt=plt, #Pass the figure handler to add the plots
                      x_cats=x_cats, q1=q1,q2=q2,q3=q3,qmin=qmin,qmax=qmax,OL=OL,
                      plot_ol=plot_ol,
                      box_width=box_width,box_alpha_fill=box_alpha_fill,
                      wsk_limits_width=wsk_limits_width,
                      ol_mk_alpha=ol_mk_alpha,
                      ol_mk_color=ol_mk_color,
                      ol_mk_size=ol_mk_size)
    return plt