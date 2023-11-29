# IESVic Pyomo for OSeMOSYS:
# Script for visualizing relevant resukts from OSeMOSYS runs
'''
from __future__ import division
from pyomo.environ import *
from pyomo.core import *
import ctypes
import os
import sys
import pandas as pd
import numpy as np

# Functions for visualization

# Taken inspiration from: 
# https://stackoverflow.com/questions/67491499/how-to-extract-indexed-variable-information-in-pyomo-model-and-build-pandas-data
# and: https://stackoverflow.com/questions/32957441/putting-many-python-pandas-dataframes-to-one-excel-worksheet
# and: https://stackoverflow.com/questions/41215508/using-loop-to-create-excel-sheets-with-dataframe-pandas
def Variable_Frame(instance):
    # Set-up step 
    Variables_file = pd.ExcelWriter('./Model-Results/Variables_DataFrame.xlsx')#, engine='xlsxwriter')
    variable_series = []
    model_vars = instance.component_map(ctype=Var)
    
    # Get resulting variables values
    for k in model_vars.keys():
        v = model_vars[k]
        series = pd.Series(v.extract_values(), index=v.extract_values().keys())

        if type(series.index[0]) == tuple:
            series = series.unstack(level=1)
        else:
            series = pd.DataFrame(series)
        
        series.columns = pd.MultiIndex.from_tuples([(k, t) for t in series.columns])
        variable_series.append(series)
    
    # Write to Excel file 
    for i, temp_df in enumerate(variable_series):
        #temp_df = pd.DataFrame(i)
        temp_df.to_excel(Variables_file, sheet_name=f'Sheet{i}')# + str(counter), index=True)
    Variables_file.save()

'''