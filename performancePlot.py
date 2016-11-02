# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 20:26:49 2016

@author: julia.delos
"""

from bokeh.plotting import figure, output_file
from bokeh.io import push_notebook
import pandas as pd
from pandas import pi



p = figure(plot_width=800,plot_height=400,x_range=tmem10['SrvNameInst'].tolist())

p.vbar(x=tmem10['SrvNameInst'].tolist(), width=0.5, bottom=0, top=tmem10['tpmGb'].tolist() )
p.xaxis.major_label_orientation = pi/4
p.vbar(x=tmem10['SrvNameInst'].tolist(), color='#001234',width=0.5, bottom=0, top=tmem10['avgGb'].tolist(),alpha=0.7 )
#p.line(x=tmem10['SrvNameInst'].tolist(), color='#001234',y=tmem10['avgGb'].tolist() )

sel = boxPrms[boxPrms['key'] == 'PPO']

#p.rect(x[1],(sel['Q3']+sel['Q2'])/2,1,sel['Q3']-sel['Q2'],line_width=2, line_color="black")
output_file("boxplot.html", title="boxplot.py example")


show(p)
