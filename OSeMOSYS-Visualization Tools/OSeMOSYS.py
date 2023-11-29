import sys
import os

import pandas as pd; import numpy as np; import matplotlib.pyplot as plt
import panel as pn
from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets
pn.extension()
from pylab import * 
import panel as pn
from bokeh.embed import components
import string
import pyam
import sys
from format_data import *
import random

YEAR_LIST = [i for i in range(2015,2066)]

filename = input("Enter the CSV name (e.g. SelRes.csv):\n")
region = data_formatting(filename)
osmosis = pd.read_csv(f"{filename.split('.')[0]}-formatted.csv")


osmosis.head()

osmosis_df = pyam.IamDataFrame(osmosis)

osmosis.head()

capacity_title_list, new_capacity_title_list, dELEC_title_list, annual_emissions_title_list = [],[],[],[]
for row in osmosis["Variable"]:
    if "Total Capacity" in row:
        capacity_title_list.append(row)
    if "Electricity Generation" in row:
        dELEC_title_list.append(row)
    if "New Capacity" in row:
        new_capacity_title_list.append(row)
    if "Annual Emissions" in row:
        annual_emissions_title_list.append(row)

plot_dictionary = dict()
plot_dictionary["Total Capacity*"] = dict(titles=capacity_title_list)
plot_dictionary["Electricity Generation*"]= dict(titles=dELEC_title_list)
plot_dictionary["New Capacity*"] = dict(titles=new_capacity_title_list)
plot_dictionary["Annual Emissions*"] = dict(titles=annual_emissions_title_list)

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvas
import numpy as np
import matplotlib.pyplot as plt


#%matplotlib inline

def str_value(long_string):
        long_string.replace("]","0")
        #print(long_string)
        
        split_string = long_string.split(" ")
      
        value = split_string[-1]
        value = value.rstrip(value[-1])
       
        #value = value[:-1]

        return value

#ATTEMPT WE MIGHT DISCARD
def ex_fig_general(plot_name, region):
       
    all_y_data = [] # (list of lists)

    new_y_title_list = []
   
    y_tile_list = plot_dictionary[plot_name]["titles"]

    for y_title in y_tile_list:
        y_data = produce_list(y_title, plot_name, plot_dictionary, region)
        if len(y_data) > 0:
            all_y_data.append(y_data)
            new_y_title_list.append(y_title)
        else:
            continue
    
    print("HERE IS THE Y DATA")
    print(all_y_data)
    fig = Figure(figsize=(12,7))
    FigureCanvas(fig) # not needed in mpl >= 3.1
    ax = fig.add_subplot()
    colours = []
    for i in range(0,25):
        r = random.random()
        g = random.random()
        b = random.random()
        rgb = (r,g,b)
        colours.append(rgb)
        
    ax.stackplot(YEAR_LIST, *all_y_data, labels=new_y_title_list, colors=colours)
    
    ax.legend(loc='upper left', fontsize = '6.5')
    ax.set_xlabel("Year")
    if plot_name == "Total Capacity*":
        ax.set_ylabel("Total Generation Capacity(GW)")
    elif plot_name == "Electricity Generation*":
        ax.set_ylim([0, 160000])
        ax.set_ylabel("Electricity Generation(GWh)")
    elif plot_name == "New Capacity*":
        ax.set_ylabel("New Capacity(GW)")
    elif plot_name == "Annual Emissions*":
        if "CH4" in new_y_title_list[0]:
            ax.set_ylabel("Annual CH4 Emissions(Megatonnes/GWh)")
        elif "CO2" in new_y_title_list[0]:
            ax.set_ylabel("Annual CO2 Emissions(Megatonnes/GWh)")
    fig.savefig('img.jpg', dpi = 300)
    return fig

def produce_list(title, Variable, plot_dictionary, region):
   
    plotyrs = YEAR_LIST
    plotdf = create_df(Variable, region)

    foo = plotdf.filter(variable = title, year = plotyrs)

    container = []
    for i in foo.data.values:
        bar = str(i)
        test_value = str_value(bar)
        num = float(test_value)

        container.append(num)
    return container

def create_df(Variable, region):
    v_df = osmosis_df.filter(variable = Variable,region = region)
  

    return v_df


def change_plot(Variable, view_fn=ex_fig_general):
    return view_fn(Variable, region)

y = "<br>\n# OSeMOSYS Plot\nChoose between the following options"

interact_dict = dict(Variable=["Total Capacity*","Electricity Generation*","New Capacity*","Annual Emissions*"])


i = pn.interact(change_plot, **interact_dict)
[""]

i.pprint()
p = pn.Row(pn.Column(y, i[0][0]), i[1][0])
p.show()





