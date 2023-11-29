# OSeMOSYS Pyomo Implementation by IESVic #
## Authors
* Cristiano Fernandes - 3rd Year Electrical Engineering at the University of Victoria
* Henry Jiang - 4th Year Computer Science at the University of Victoria
* Piyush Lamba - 4th Year Computer Science at the University of Victoria
* Dr. Jacob Monroe - team supervisor (IESVic)

---------------------------------------------------------------------------------------------------------------------------------------------------

## Linear solvers
To run the Pyomo implementation of OSeMOSYS you will first need a linear solver installed in your machine.

* You can get the GLPK linear solver properly installed in your machine by following this [tutorial](http://www.osemosys.org/uploads/1/8/5/0/18504136/glpk_installation_guide_for_windows10_-_201702.pdf)
* To get the CPLEX linear solver, follow this [tutorial](https://www.ibm.com/support/pages/downloading-ibm-ilog-cplex-optimization-studio-v1290)

---------------------------------------------------------------------------------------------------------------------------------------------------

## Running the model
The OSeMOSYS model file is named `pyomo-osemosys.py`

To run the model from the command line, simply copy and paste the following line: **pyomo solve --solver=`my_solver` pyomo-osemosys.py `my_data`.dat**

Where `my_solver` is your solver of choice (we recommend using GLPK) and `my_data` is the data file in AMPL data format.

Currently, the model is running by using [Pandas](https://pandas.pydata.org/) to read the model data into the model file, allowing you to run the application from the Python IDE

---------------------------------------------------------------------------------------------------------------------------------------------------

## Debugging and model resources
To help debug the model, some useful files have been created inside the model script

* A `variables` file with end values for model variables
* A `duals` file with the values of the dual solution to the model and constraint slack values
* A `model log` file with the values of the primal solution to the model
* A `model lp` file with the model problem written in lp format (readable by CPLEX)
* A `selected results` file with cherry-picked results from the model's primal solution

Additionaly, CPLEX can be used to produce similar files to assist us in debugging the model.

This is how you can obtain the following files from a model lp file with CPLEX:
1) Run CPLEX on the command line by typeing `CPLEX`
2) Read the lp file with the command `read my_model_lp_file.lp`
3) Solve the lp problem by typeing `optimize` in the command prompt (CPLEX's solution summary should appear)
4) To see the model's dual solution, use the command `display solution dual -` (the dash indicates that CPLEX should display all available outputs to the command)
5) To see the model's slack values, use the command `display solution slacks -`
6) To write the model duals to a separate file, type the command `write filename dua` (the file type "dua" indicates to CPLEX you are looking for information about model duals, but you can use the same command to get different model information into separate files by replacing the file type). To get a list of supported file types simply type `write filename` instead, and CPLEX will inform you of the types it can output

In order to get the lp file from GLPK to be used by CPLEX, simply write the following command when prompting to solve a model with GLPK from the command line: `--wlp glpklp_file.lp` 
