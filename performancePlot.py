# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 20:26:49 2016

@author: julia.delos
"""

from bokeh.plotting import figure, output_file, show
from bokeh.io import push_notebook
import pandas as pd
import numpy as np
from numpy import pi


tmem10 = pd.read_csv('tmem10.csv')
boxPrms = pd.read_csv('./boxPlots.csv')

DicSrv = tmem10[['SrvNameInst','SrvName']].to_dict()



p = figure(plot_width=800,plot_height=400,x_range=tmem10['SrvNameInst'].tolist())

p.vbar(x=tmem10['SrvNameInst'].tolist(), width=0.5, bottom=0, top=tmem10['tpmGb'].tolist() )
p.xaxis.major_label_orientation = pi/4
p.vbar(x=tmem10['SrvNameInst'].tolist(), color='#001234',width=0.5, bottom=0, top=tmem10['avgGb'].tolist(),alpha=0.7 )
#p.line(x=tmem10['SrvNameInst'].tolist(), color='#001234',y=tmem10['avgGb'].tolist() )

for idx, Srv in  DicSrv['SrvName'].items():
    
    sel = boxPrms[boxPrms['key'] == Srv]
    cat = DicSrv['SrvNameInst'][idx]
    
    p.vbar(x=[cat],width=0.75,bottom=sel['Q1']/1024,top=sel['Q3']/1024,
           line_width=1,line_color="black",line_alpha=1,
           fill_color='green',fill_alpha=0.2)
           
    p.vbar(x=[cat],width=0.75,bottom=sel['Q2']/1024,top=sel['Q2']/1024,
           line_width=1,line_color="black",line_alpha=1,
           fill_color='green',fill_alpha=0.2)
           
    p.vbar(x=[cat],width=0.75,bottom=sel['Qmin']/1024,top=sel['Qmin']/1024,
           line_width=1,line_color="black",line_alpha=1,
           fill_color='black',fill_alpha=0.2)
    
    p.vbar(x=[cat],width=0.75,bottom=sel['Qmax']/1024,top=sel['Qmax']/1024,
           line_width=1,line_color="black",line_alpha=1,
           fill_color='black',fill_alpha=0.2)
           
    p.line(x=[cat,cat],y=[float(sel['Q3']/1024),float(sel['Qmax']/1024)],
           line_width=1,line_color='black')
           
    p.line(x=[cat,cat],y=[float(sel['Qmin']/1024),float(sel['Q1']/1024)],
           line_width=1,line_color='black')
    olStr = sel['OL'].tolist()[0]
    if len(olStr) > 2:
        ol_points = np.array(map(float,olStr[1:-1].split(',')))/1024
        cats = [cat] * len(ol_points)
        p.asterisk(x=cats,y=ol_points,color='red')
        
       

output_file("boxplot.html", title="boxplot.py example")


show(p)
