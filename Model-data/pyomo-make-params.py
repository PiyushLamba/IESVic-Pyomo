#This script converts OSeMOSYS Base Parameters from Excel to Data file format
#04.05.2020 Kevin Palmer-Wilson // modifyed to run with pyomo models by: Cristiao Curi Fernandes (16/09/2021)

from os import getcwd, path
import csv
import xlrd

########
#Define file names and input/output paths
########
version = 'Test_24h_3_Seasons'

#name of OSeMOSYS Base Parameter EXCEL file
param_file = 'OSeMOSYS_'+version+'_Base_Parameters.xlsx'
#Name of the parameter TEXT file
param_out = 'OSeMOSYS_' + version + '_params.dat'

#path to the OSeMOSYS Base Parameter EXCEL file
param_path = path.normpath(path.join(getcwd()))
#path to the parameter TEXT file
param_output_path = path.normpath(path.join(getcwd()))
 
#Define the name of the SelRes output file, so that we can apend it as a parameter
selRes = ['\n param SelRes := \''+version+'_SelRes.csv\';\n']


#######################
#This section reads the excel parameters file and turns it into a text file
#######################
# Create the parameters.dat file from the parameters excel file to make it readable for OSeMOSYS
# open the output dat file
with open(path.join(param_output_path,param_out), 'wt') as myDatfile:

    # define a writer
    wr = csv.writer(myDatfile, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\t')

    #First, run through the entire base parameter file (the excel file) and write it to the custom parameters file
    #We will add the LandValue parameter at the end
    # open the xlsx file 
    myfile = xlrd.open_workbook(path.join(param_path,param_file))

    #count the number of sheets - we want to skip the first two
    sheetcount = len(myfile.sheet_names())

    for sheetindex in range(2,sheetcount):
        # get a sheet
        mysheet = myfile.sheet_by_index(sheetindex)

        #Cycle through rows
        for rownum in range(mysheet.nrows):
            #Check if data in a cell is int or float. If it is int, make sure it stays int
            rowdata = []
            for colnum in range(mysheet.ncols):

                #Select the cell to process
                cell = mysheet.cell(rownum,colnum)
                celldata = cell.value

                #If the cell was of type int, convert the float data to int data
                #Explanation: all numbers are stored as float in excel
                #excel formats cells as int if the cell type is 2 according to 
                #http://www.lexicon.net/sjmachin/xlrd.html#xlrd.Cell-class
                if cell.ctype == 2 and int(celldata) == celldata:
                    celldata = int(celldata)

                #Add the processed cell data to the row
                rowdata.append(celldata)

            # write the rows    
            wr.writerow(rowdata)
    #######################
    #This section appends appends our scenario specific parameters like land costs, total annual demand and demand profiles
    #######################
    #now write the custom names of the SelRes output files
    wr.writerow(selRes)

print('Successfully created OSeMOSYS parameter data file:')
print(path.join(param_output_path,param_out))
print('\nAll done!')
    
