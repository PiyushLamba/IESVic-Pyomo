# IESVic Pyomo for OSeMOSYS:

from __future__ import division
from pyomo.environ import *
from pyomo.core import *
from pyomo.util.infeasible import log_infeasible_constraints
import os
import sys
import logging
import ctypes
import pandas as pd
import numpy as np

# Debugging tools

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


def Create_Log_Files(instance, final_result):
	# Model lp
	my_path = "./"
	filename = os.path.join(my_path, 'Log-files/pyomo_model.lp') # LP file of the instance
	instance.write(filename, io_options={'symbolic_solver_labels': True})
	
	# Vartiables log
	'''
	variable_log = open("./Log-files/Variables.log", "w")
	for v in instance.component_data_objects(Var):
		print(str(v), v.value, file=variable_log)
	'''
	Variable_Frame(instance)

	# Model log
	logfile = open("./Log-files/pyomomodel.log", "w")
	instance.pprint(ostream=logfile)
	instance.solutions.load_from(final_result)
	
	# Infeasible constraints log
	log_infeasible_constraints(instance, log_expression=True, log_variables=True)

	# Duals log
	dual_logfile = open("./Log-files/Duals.log", "w") # Create file to print instance duals
	print("Model duals:\n", file=dual_logfile)
	instance.dual.pprint(dual_logfile)
	print("\nConstraint slacks:\n", file=dual_logfile)
	print("Constraint || Lower Slack || Upper Slack", file=dual_logfile)
	for c in instance.component_objects(Constraint, active=True):
		for index in c:
			print(c[index], " || ", c[index].lslack(), " || ", c[index].uslack(), file=dual_logfile)
