# Pyomo OSeMOSYS
# IESVic - 2021

# Import relevant Python modules

from __future__ import division
from fileinput import filename
from pyomo.environ import *
from pyomo.core import *
from pyomo.opt import SolverFactory
import pandas as pd
import math
import random

# Importing Model modules

from Objective_Function import ObjectiveFunctionRule
from Model_Constraints import *
from Model_Debugging_Tools import Create_Log_Files
from Model_Sel_Res import Selected_Results
#from ResVisuals import *


model = AbstractModel(name="OSeMOSYS_IESVic") # Create model object and give it a name

#Notes:
'''
Pyomo is currently detecting: 

* 123 Set Declarations, but there are only 12 (Declaring which set indexes which constraint)
* 53 Parameter declarations, there are 53 parameters (Correct declarations)
* 21 Variable declarations, there are 21 Variables (Correct declaration)
* 1 Objective function declaration, there is 1 Objective Function (Correct declaration)
* 39 Constraints declarations, there are 39 Constraints (Correct declaration)
* 237 total component declarations (was 227 when Constraint.Feasible constraints were commented out)

'''
##################################################################################################
# Importing data from excel sheet to the model
# Data files:
# 1 region
sets_file = "./Four-Region-Expansion/1_Region/Model_Sets_1_Region.xlsx"
parameters_file = "./Four-Region-Expansion/1_Region/Model_Parameters_1_Region.xlsx"

# 2 regions
#sets_file = "./New_Changes/1_Region/Model_Sets_2_Regions.xlsx"
#parameters_file = "./New_Changes/1_Region/Model_Parameters_2_Regions.xlsx"

# 4 regions
#sets_file = "./Four-Region-Expansion/4_Regions/Model_Sets_4_Regions.xlsx"
#parameters_file = "./Four-Region-Expansion/4_Regions/Model_Parameters_4_Regions.xlsx"

pyomodata_file =  'Model-data\OSeMOSYS_Test_24h_params.dat' # Copy path to your data file (.dat) in this variable

##################################################################################################

# Flag to signal wheather the data is being given to the model through .dat file, or through Pandas data frames
    # True: Data being imported through  data file (.dat)
    # False: Data being imported from data frames
DATAFILE_FLAG = False

##################################################################################################

# Data processing
def Process_Data(data, component="set"):
    data = data.to_dict('list') # Transform dataframe into dictionary of lists
    #print(data)    
    included = data.pop('Included') # Get the 'Included' column as a separate list (alternative way of achieving this: list(data.values())[0] )
    value = list(data.values())[-1] # Get parameter values as a separate list
    if component == "set": # Initialize sets
        initializer = []
        for k in range(len(value)):
            if included[k] == "Yes":
                initializer.append(value[k])
    elif component == "parameter": # Initialize parameters
        initializer = {}
        sets = list(data.values())[0:-1]
        set_tuples = [tuple([i[j] for i in sets]) for j in range(len(sets[0]))] # Get sets indexing the parameter as tuples
        for k, i, j in zip(included, set_tuples, value):
            if(k == 'No'):
                continue
            if not math.isnan(j):
                initializer[i] = j
    return initializer

##################################################################################################

# Establishing the model:

if DATAFILE_FLAG is True:
    # Sets

    model.YEAR = Set()
    model.TECHNOLOGY = Set()
    model.TIMESLICE = Set()
    model.FUEL = Set()
    model.EMISSION = Set()
    model.MODE_OF_OPERATION = Set()
    model.REGION = Set()
    model.SEASON = Set()
    model.DAYTYPE = Set()
    model.DAILYTIMEBRACKET = Set()
    #model.FLEXIBLEDEMANDTYPE = Set()
    model.STORAGE = Set()

    ##################################################################################################

    # Parameters

    # Global parameters

    model.DiscountRate = Param(model.REGION, default=0.06)
                            
    model.YearSplit = Param(model.TIMESLICE, model.YEAR, default=0.000114155)
                            
    model.DaySplit = Param(model.DAILYTIMEBRACKET, model.YEAR, default=0.000114155)
                        
    model.Conversionls = Param(model.TIMESLICE, model.SEASON, default=1)
                         
    model.Conversionld = Param(model.TIMESLICE, model.DAYTYPE, default=0)
                         
    model.Conversionlh = Param(model.TIMESLICE, model.DAILYTIMEBRACKET, default=0)
                         
    model.DaysInDayType = Param(model.SEASON, model.DAYTYPE, model.YEAR, default=1)
                         
    model.TradeRoute = Param(model.REGION, model.REGION, model.FUEL, model.YEAR, default=0)
                         
    model.DepreciationMethod = Param(model.REGION, default=1)
                         
    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Demands

    model.AccumulatedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR, default=0)
                         
    model.SpecifiedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR, default=0)
                         
    model.SpecifiedDemandProfile = Param(model.REGION, model.FUEL, model.TIMESLICE, model.YEAR, default=0)
                         
    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Performance

    model.CapacityToActivityUnit = Param(model.REGION, model.TECHNOLOGY, default=8760)
                             
    model.TechWithCapacityNeededToMeetPeakTS = Param(model.REGION, model.TECHNOLOGY, default=1)
                             
    model.CapacityFactor = Param(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, default=1)
                             
    model.AvailabilityFactor = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=1) 
                             
    model.OperationalLife = Param(model.REGION, model.TECHNOLOGY, default=80)
                             
    model.ResidualCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                             
    model.InputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR, default=0)
                             
    model.OutputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR, default=0)
                             

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Technology Costs

    model.CapitalCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                             
    model.VariableCost = Param(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, default=0.0001)
                             
    model.FixedCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0) 
                             
    # Added parameter: SimultaneityTagTechnology (to run model with SILVER)
    model.SimultaneityTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, default=0)

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Storage

    model.TechnologyStorage = Param(model.REGION, model.TECHNOLOGY, model.STORAGE, model.MODE_OF_OPERATION, default=0)
                                
    model.StorageMaxChargeRate = Param(model.REGION, model.STORAGE, default=9999)
                                
    model.StorageMaxDischargeRate = Param(model.REGION, model.STORAGE, default=9999)
                                
    model.MinStorageCharge = Param(model.REGION, model.STORAGE, model.YEAR, default=0)
                                
    model.OperationalLifeStorage = Param(model.REGION, model.STORAGE, default=1) 
                                
    model.CapitalCostStorage = Param(model.REGION, model.STORAGE, model.YEAR, default=9999)
    
    
    model.ResidualStorageCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0) # default is usually 0
                                
    # TN 2016 04 Added Storage Maximum:
    model.StorageMaxCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0)
                            

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    #  Capacity Constraints

    model.CapacityOfOneTechnologyUnit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                                
    model.TotalAnnualMaxCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=9999)
                            
    model.TotalAnnualMinCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                                

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Investment Constraints  

    model.TotalAnnualMaxCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=99999)
                                
    model.TotalAnnualMinCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                                

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Activity Constraints

    model.TotalTechnologyAnnualActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=9999999)
                                
    model.TotalTechnologyAnnualActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                                
    model.TotalTechnologyModelPeriodActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, default=9999999)
                                
    model.TotalTechnologyModelPeriodActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, default=0)
                            
    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Reserve Margin

    model.ReserveMarginTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                                
    model.ReserveMarginTagFuel = Param(model.REGION, model.FUEL, model.YEAR, default=0)
                                
    model.ReserveMargin = Param(model.REGION, model.YEAR, default=0)
                                
    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # RE Generation Target

    model.RETagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
                               
    model.RETagFuel = Param(model.REGION, model.FUEL, model.YEAR, default=0)
                               
    model.REMinProductionTarget = Param(model.REGION, model.YEAR, default=0)
                        
    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Emissions & Penalties 

    model.EmissionActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.EMISSION, model.MODE_OF_OPERATION, model.YEAR, default=0)
                                    
    model.EmissionsPenalty = Param(model.REGION, model.EMISSION, model.YEAR, default=0)
                                
    model.AnnualExogenousEmission = Param(model.REGION, model.EMISSION, model.YEAR, default=0)
                                
    model.AnnualEmissionLimit = Param(model.REGION, model.EMISSION, model.YEAR, default=99999)
                                
    model.ModelPeriodExogenousEmission = Param(model.REGION, model.EMISSION, default=0)
                                
    model.ModelPeriodEmissionLimit = Param(model.REGION, model.EMISSION, default=99999)
                                
    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    model.StoredEnergyValue = Param(model.REGION, model.STORAGE, default= 0)

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#                               

else:
    # Dataframes:

    FUEL_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="FUEL",  header=0))
    EMISSION_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="EMISSION"))
    YEAR_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="YEAR"))
    TIMESLICE_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="TIMESLICE"))
    MODE_OF_OPERATION_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="MODE_OF_OPERATION"))
    REGION_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="REGION"))
    SEASON_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="SEASON"))
    DAYTYPE_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="DAYTYPE"))
    DAILYTIMEBRACKET_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="DAILYTIMEBRACKET"))
    STORAGE_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="STORAGE"))
    TECHNOLOGY_df = pd.DataFrame(pd.read_excel(sets_file, sheet_name="TECHNOLOGY"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    DISCOUNTRATE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Discount_Rate"))
    DEPRECIATIONMETHOD_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Depreciation_Method"))
    TRADEROUTE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Trade_Route"))
    SPECIFIEDANNUALDEMAND_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Specified_Annual_Demand"))
    ACCUMULATEDANNUALDEMAND_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Accumulated_Annual_Demand"))
    YEARSPLIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Year_Split"))
    SPECIFIEDDEMANDPROFILE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Specified_Demand_Profile"))
    CONVERSIONLS_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Conversionls"))
    CONVERSIONLD_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Conversionld"))
    CONVERSIONLH_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Conversionlh"))
    DAYSPLIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Day_Split"))
    DAYSINDAYTYPE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Days_In_Day_Type"))    
    CAPACITYTOACTIVITYUNIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Capacity_To_Activity_Unit"))
    TECHNOLOGYWITHCAPACITYTOMEATPEAKTS_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Tech_Peak_TS"))
    OPERATIONALLIFE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Operational_Life"))
    RESIDUALCAPACITY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Residual_Capacity"))
    CAPACITYOFONETECHNOLOGYUNIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Capacity_1_Technology_Unit"))
    TOTALANNUALMAXCAPACITY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Total_Annual_Max_Capacity"))
    TOTALANNUALMINCAPACITY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Total_Annual_Min_Capacity"))
    TOTALANNUALMAXCAPACITYINVESTMENT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="T_AnnualMax_CapacityInvestment"))
    TOTALANNUALMINCAPACITYINVESTMENT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="T_AnnualMin_CapacityInvestment"))
    TOTALTECHNOLOGYANNUALACTIVITYUPPERLIMIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="TotalTechAnnualActivityUpLimit"))
    TOTALTECHNOLOGYANNUALACTIVITYLOWERLIMIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="TotalTechAnnualActivityLowLimit"))
    TOTALTECHNOLOGYMODELPERIODACTIVITYUPPERLIMIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="T_TechModelPeriodActivity_UL"))
    TOTALTECHNOLOGYMODELPERIODACTIVITYLOWERLIMIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="T_TechModelPeriodActivity_LL"))
    CAPITALCOST_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Capital_Cost"))
    FIXEDCOST_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Fixed_Cost"))
    VARIABLECOST_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Variable_Cost"))
    INPUTACTIVITYRATIO_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Input_Activity_Ratio"))
    OUTPUTACTIVITYRATIO_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Output_Activity_Ratio"))
    AVAILABILITYFACTOR_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Availability_Factor"))
    CAPACITYFACTOR_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Capacity_Factor"))
    RESERVEMARGINTAGFUEL_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Reserve_Margin_Tag_Fuel"))
    RESERVEMARGINTAGTECHNOLOGY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Reserve_Margin_Tag_Technology"))
    RESERVEMARGIN_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Reserve_Margin"))
    EMISSIONACTIVITYRATIO_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Emission_Activity_Ratio"))
    EMISSIONSPENALTY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Emissions_Penalty"))
    ANNUALEXOGENOUSEMISSION_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Annual_Exogenous_Emission"))
    ANNUALEMISSIONLIMIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Annual_Emission_Limit"))
    MODELPERIODEXOGENOUSEMISSION_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="ModelPeriod_Exogenous_Emission"))
    MODELPERIODEMISSIONLIMIT_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Model_Period_Emission_Limit"))
    TECHNOLOGYSTORAGE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Technology_Storage"))
    STORAGEMAXCHARGERATE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Storage_Max_Charge_Rate"))
    STORAGEMAXDISCHARGERATE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Storage_Max_Discharge_Rate"))
    MINSTORAGECHARGE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Min_Storage_Charge"))
    OPERATIONALLIFESTORAGE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="OperationalLife_Storage"))
    CAPITALCOSTSTORAGE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Capital_Cost_Storage"))
    RESIDUALSTORAGECAPACITY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Residual_Storage_Capacity"))
    STOREDENERGYVALUE_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Stored_Energy_Value"))
    STORAGEMAXCAPACITY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Storage_Max_Capacity"))
    RETAGTECHNOLOGY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="RE_Tag_Technology"))
    RETAGFUEL_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="RE_Tag_Fuel"))
    REMINPRODUCTIONTARGET_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="RE_Min_Production_Target"))
    SIMULTANEITY_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Simultaneity"))

    # Sets

    model.YEAR = Set(initialize=Process_Data(YEAR_df, component="set"))
    model.TECHNOLOGY = Set(initialize=Process_Data(TECHNOLOGY_df,component="set"))
    model.TIMESLICE = Set(initialize=Process_Data(TIMESLICE_df,component="set"))
    model.FUEL = Set(initialize=Process_Data(FUEL_df, component="set"))
    model.EMISSION = Set(initialize=Process_Data(EMISSION_df, component="set"))
    model.MODE_OF_OPERATION = Set(initialize=Process_Data(MODE_OF_OPERATION_df, component="set"))
    model.REGION = Set(initialize=Process_Data(REGION_df, component="set"))
    model.SEASON = Set(initialize=Process_Data(SEASON_df,component="set"))
    model.DAYTYPE = Set(initialize=Process_Data(DAYTYPE_df,component="set"))
    model.DAILYTIMEBRACKET = Set(initialize=Process_Data(DAILYTIMEBRACKET_df, component="set"))
    #model.FLEXIBLEDEMANDTYPE = Set(Process_Data(FLEXIBLEDEMANDTYPE_df,component="set"))
    model.STORAGE = Set(initialize=Process_Data(STORAGE_df, component="set"))

    ##################################################################################################

    # Parameters

    # Global parameters

    model.DiscountRate = Param(model.REGION, default=0.06,
                            initialize=Process_Data(DISCOUNTRATE_df, component="parameter"))
    model.YearSplit = Param(model.TIMESLICE, model.YEAR, default=0.000114155,
                            initialize=Process_Data(YEARSPLIT_df, component="parameter"))
    model.DaySplit = Param(model.DAILYTIMEBRACKET, model.YEAR, default=0.000114155,
                        initialize=Process_Data(DAYSPLIT_df, component="parameter"))
    model.Conversionls = Param(model.TIMESLICE, model.SEASON, default=1,
                            initialize=Process_Data(CONVERSIONLS_df, component="parameter"))
    model.Conversionld = Param(model.TIMESLICE, model.DAYTYPE, default=0,
                                initialize=Process_Data(CONVERSIONLD_df, component="parameter"))
    model.Conversionlh = Param(model.TIMESLICE, model.DAILYTIMEBRACKET, default=0,
                                initialize=Process_Data(CONVERSIONLH_df, component="parameter")) # Create a separate datafile for Conversionlh
    model.DaysInDayType = Param(model.SEASON, model.DAYTYPE, model.YEAR, default=1,
                                initialize=Process_Data(DAYSINDAYTYPE_df, component="parameter"))
    model.TradeRoute = Param(model.REGION, model.REGION, model.FUEL, model.YEAR, default=0,
                                initialize=Process_Data(TRADEROUTE_df, component="parameter"))
    model.DepreciationMethod = Param(model.REGION, default=1,
                                initialize=Process_Data(DEPRECIATIONMETHOD_df, component="parameter"))


    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Demands

    model.AccumulatedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR, default=0,
                                initialize=Process_Data(ACCUMULATEDANNUALDEMAND_df, component="parameter"))
    model.SpecifiedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR, default=0,
                                        initialize=Process_Data(SPECIFIEDANNUALDEMAND_df, component="parameter"))
    model.SpecifiedDemandProfile = Param(model.REGION, model.FUEL, model.TIMESLICE, model.YEAR, default=0,
                                        initialize=Process_Data(SPECIFIEDDEMANDPROFILE_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Performance

    model.CapacityToActivityUnit = Param(model.REGION, model.TECHNOLOGY, default=8760,
                                initialize=Process_Data(CAPACITYTOACTIVITYUNIT_df, component="parameter"))
    model.TechWithCapacityNeededToMeetPeakTS = Param(model.REGION, model.TECHNOLOGY, default=1,
                                initialize=Process_Data(TECHNOLOGYWITHCAPACITYTOMEATPEAKTS_df, component="parameter"))
    model.CapacityFactor = Param(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, default=1,
                                initialize=Process_Data(CAPACITYFACTOR_df, component="parameter"))
    model.AvailabilityFactor = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=1, 
                                initialize=Process_Data(AVAILABILITYFACTOR_df, component="parameter"))
    model.OperationalLife = Param(model.REGION, model.TECHNOLOGY, default=80,
                                initialize=Process_Data(OPERATIONALLIFE_df, component="parameter"))
    model.ResidualCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(RESIDUALCAPACITY_df, component="parameter"))
    model.InputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR, default=0,
                                initialize=Process_Data(INPUTACTIVITYRATIO_df, component="parameter")) # In expanded mode, the Input Activity Ratio is dependent on the Timeslice as well
    model.OutputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR, default=0,
                                initialize=Process_Data(OUTPUTACTIVITYRATIO_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Technology Costs

    model.CapitalCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(CAPITALCOST_df, component="parameter"))
    model.VariableCost = Param(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, default=0.0001,
                                initialize=Process_Data(VARIABLECOST_df, component="parameter"))
    model.FixedCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0, 
                                initialize=Process_Data(FIXEDCOST_df, component="parameter"))
    # Added parameter: SimultaneityTagTechnology (to run model with SILVER)
    model.SimultaneityTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, default=0,
                                initialize=Process_Data(SIMULTANEITY_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Storage

    model.TechnologyStorage = Param(model.REGION, model.TECHNOLOGY, model.STORAGE, model.MODE_OF_OPERATION, default=0,
                                initialize=Process_Data(TECHNOLOGYSTORAGE_df, component="parameter"))
    model.StorageMaxChargeRate = Param(model.REGION, model.STORAGE, default=9999,
                                initialize=Process_Data(STORAGEMAXCHARGERATE_df, component="parameter"))
    model.StorageMaxDischargeRate = Param(model.REGION, model.STORAGE, default=9999,
                                initialize=Process_Data(STORAGEMAXDISCHARGERATE_df, component="parameter"))
    model.MinStorageCharge = Param(model.REGION, model.STORAGE, model.YEAR, default=0,
                                initialize=Process_Data(MINSTORAGECHARGE_df, component="parameter"))
    model.OperationalLifeStorage = Param(model.REGION, model.STORAGE, default=1, 
                                initialize=Process_Data(OPERATIONALLIFESTORAGE_df, component="parameter"))
    model.CapitalCostStorage = Param(model.REGION, model.STORAGE, model.YEAR, default=9999,
                                initialize=Process_Data(CAPITALCOSTSTORAGE_df, component="parameter"))

    # Changing the Residual Storage Capacity default to see if any changes are made to storage variables in results file                             
    model.ResidualStorageCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0,
                                initialize=Process_Data(RESIDUALSTORAGECAPACITY_df, component="parameter"))
    # TN 2016 04 Added Storage Maximum:
    model.StorageMaxCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0)
                            #initialize=Process_Data(STORAGEMAXCAPACITY_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    #  Capacity Constraints

    model.CapacityOfOneTechnologyUnit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(CAPACITYOFONETECHNOLOGYUNIT_df, component="parameter"))
    model.TotalAnnualMaxCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=9999,
                            initialize=Process_Data(TOTALANNUALMAXCAPACITY_df, component="parameter"))
    model.TotalAnnualMinCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(TOTALANNUALMINCAPACITY_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Investment Constraints  

    model.TotalAnnualMaxCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=99999,
                                initialize=Process_Data(TOTALANNUALMAXCAPACITYINVESTMENT_df, component="parameter"))
    model.TotalAnnualMinCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(TOTALANNUALMINCAPACITYINVESTMENT_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Activity Constraints

    model.TotalTechnologyAnnualActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=9999999,
                                initialize=Process_Data(TOTALTECHNOLOGYANNUALACTIVITYUPPERLIMIT_df, component="parameter"))
    model.TotalTechnologyAnnualActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(TOTALTECHNOLOGYANNUALACTIVITYLOWERLIMIT_df, component="parameter"), within=Reals)
    model.TotalTechnologyModelPeriodActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, default=9999999,
                                initialize=Process_Data(TOTALTECHNOLOGYMODELPERIODACTIVITYUPPERLIMIT_df, component="parameter"))
    model.TotalTechnologyModelPeriodActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, default=0,
                                initialize=Process_Data(TOTALTECHNOLOGYMODELPERIODACTIVITYLOWERLIMIT_df, component="parameter"), within=Reals)

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Reserve Margin

    model.ReserveMarginTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(RESERVEMARGINTAGTECHNOLOGY_df, component="parameter"))
    model.ReserveMarginTagFuel = Param(model.REGION, model.FUEL, model.YEAR, default=0,
                                initialize=Process_Data(RESERVEMARGINTAGFUEL_df, component="parameter"))
    model.ReserveMargin = Param(model.REGION, model.YEAR, default=0,
                                initialize=Process_Data(RESERVEMARGIN_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # RE Generation Target

    model.RETagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0,
                                initialize=Process_Data(RETAGTECHNOLOGY_df, component="parameter"))
    model.RETagFuel = Param(model.REGION, model.FUEL, model.YEAR, default=0,
                                initialize=Process_Data(RETAGFUEL_df, component="parameter"))
    model.REMinProductionTarget = Param(model.REGION, model.YEAR, default=0,
                                initialize=Process_Data(REMINPRODUCTIONTARGET_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Synchronous Generation Parameters

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

    # Emissions & Penalties 

    model.EmissionActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.EMISSION, model.MODE_OF_OPERATION, model.YEAR, default=0,
                                    initialize=Process_Data(EMISSIONACTIVITYRATIO_df, component="parameter"))
    model.EmissionsPenalty = Param(model.REGION, model.EMISSION, model.YEAR, default=0,
                                initialize=Process_Data(EMISSIONSPENALTY_df, component="parameter"))
    model.AnnualExogenousEmission = Param(model.REGION, model.EMISSION, model.YEAR, default=0,
                                initialize=Process_Data(ANNUALEXOGENOUSEMISSION_df, component="parameter"))
    model.AnnualEmissionLimit = Param(model.REGION, model.EMISSION, model.YEAR, default=99999,
                                initialize=Process_Data(ANNUALEMISSIONLIMIT_df, component="parameter"))
    model.ModelPeriodExogenousEmission = Param(model.REGION, model.EMISSION, default=0,
                                initialize=Process_Data(MODELPERIODEXOGENOUSEMISSION_df, component="parameter"))
    model.ModelPeriodEmissionLimit = Param(model.REGION, model.EMISSION, default=99999,
                                initialize=Process_Data(MODELPERIODEMISSIONLIMIT_df, component="parameter"))

    #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#


    model.StoredEnergyValue = Param(model.REGION, model.STORAGE, default= 0,
                                    initialize=Process_Data(STOREDENERGYVALUE_df, component="parameter"))

    #print("Created Parameters")


##################################################################################################

# Model Variables

my_seed = random.seed(0) # Create a seed value to initialize variables with a random number
rand_init = random.random()

model.StorageLevelStart = Var(model.REGION, model.STORAGE, bounds=(0, None), domain=Reals, initialize=rand_init)

# Demands 

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# New
model.CapitalInvestment = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.RateOfUseByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None), initialize=rand_init) 
model.RateOfUseByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.FUEL, model.YEAR, bounds=(0, None), initialize=0) 


# Storage

model.StorageLevelTSStart = Var(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.NewStorageCapacity = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=0)
model.SalvageValueStorage = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelYearStart = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=0)
model.StorageLevelYearFinish = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelSeasonStart = Var(model.REGION, model.STORAGE, model.SEASON, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelDayTypeStart = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelDayTypeFinish = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR, bounds=(0, None), domain=Reals, initialize=rand_init)
model.RateOfStorageCharge = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, bounds=(0, None), domain=Reals, initialize=0)
model.RateOfStorageDischarge = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, bounds=(0, None), domain=Reals, initialize=0)
model.NetChargeWithinYear = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, bounds=(0, None), domain=Reals, initialize=0)
model.NetChargeWithinDay = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, bounds=(0, None), domain=Reals, initialize=0)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Capacity Variables

model.NumberOfNewTechnologyUnits = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Integers, initialize=0)
model.NewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init) # This vaiable must be within Real numbers for feasible solution


#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Activity Variables

model.RateOfActivity = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, domain=Reals, initialize=0)  # Eliminated the >=0 constraint (PMT)
model.UseByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds=(0, None), domain=Reals, initialize=rand_init)
model.Trade = Var(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=Reals, initialize=0)
model.TradeAnnual = Var(model.REGION, model.REGION, model.FUEL, model.YEAR, bounds=(0,None),initialize=0)
model.UseAnnual = Var(model.REGION, model.FUEL, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.Use = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, bounds=(0, None), initialize=0)
model.ProductionAnnual = Var(model.REGION, model.FUEL, model.YEAR, domain=NonNegativeReals, bounds=(0, None), initialize=rand_init)
model.Production = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, bounds=(0, None), initialize=0)
model.Demand = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, bounds=(0, None), initialize=0)
model.DemandAnnual = Var(model.REGION, model.FUEL, model.YEAR, bounds=(0, None), initialize=0)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Costing Variables

model.VariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, bounds=(0, None), domain=Reals, initialize=rand_init)
model.SalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=0)
model.DiscountedSalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.OperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Emissions

model.DiscountedTechnologyEmissionsPenalty = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.ModelPeriodEmissions = Var(model.REGION, model.EMISSION, bounds = (0, None), domain=Reals, initialize=rand_init)

# New variables

model.ProductionByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None),initialize=0)
model.ProductionByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None), initialize=0)
model.RateOfProductionByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None), initialize=rand_init)
model.RateOfProductionByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.FUEL, model.YEAR, bounds = (0, None), initialize=0)
model.TotalAnnualTechnologyActivityByMode = Var(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, bounds = (0, None), initialize=rand_init)
model.AccumulatedNewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), initialize=0)
model.TotalCapacityAnnual = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), initialize=0)
model.AnnualVariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds=(0, None), initialize=0)
model.TotalTechnologyAnnualActivity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), initialize=0)
model.TotalTechnologyModelPeriodActivity = Var(model.REGION, model.TECHNOLOGY, bounds=(0, None), initialize=0)

model.RateOfDemand = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalREProductionAnnual = Var(model.REGION, model.YEAR, initialize=0.0)
model.RETotalProductionOfTargetFuelAnnual = Var(model.REGION, model.YEAR, initialize=0.0)
model.RateOfProduction = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.UseByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfUse = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)

##################################################################################################

# Objective Function

model.OBJ = Objective(rule=ObjectiveFunctionRule, sense= minimize)


##################################################################################################

# Model Constraints

# Capital Costs

'''
Calculates the total discounted capital cost expenditure for each technology in each year.
'''

model.CC1_UndiscountedCapitalInvestment_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CC1_UndiscountedCapitalInvestment_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Operating Costs

'''
Calculates the total variable and fixed operating costs for each technology, in each year.
'''

model.OC1_OperatingCostsVariable_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=OC1_OperatingCostsVariable_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#


# Capacity Adequacy A	

'''
Used to first calculate total capacity of each technology for each year based on existing capacity 
from before the model period (ResidualCapacity), AccumulatedNewCapacity during the modelling period, and NewCapacity 
installed in each year. It is then ensured that this Capacity is sufficient to meet the RateOfTotalActivity in each 
TimeSlice and Year. An additional constraint based on the size, or capacity, of each unit of a Technology is included 
(CapacityOfOneTechnologyUnit). This stipulates that the capacity of certain Technology can only be a multiple of the 
user-defined CapacityOfOneTechnologyUnit.
'''

model.CAa1_TotalNewCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAa1_TotalNewCapacity_rule)

model.CAa2_TotalAnnualCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAa2_TotalAnnualCapacity_rule)

model.CAa5_TotalNewCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAa5_TotalNewCapacity_rule)

model.CAa4_ConstraintCapacity_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.YEAR, rule=CAa4_Constraint_Capacity_rule,)

model.CAa4b_Constraint_Capacity_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.YEAR, rule=CAa4b_Constraint_Capacity_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Capacity Adequacy B

'''
Ensures that adequate capacity of technologies is present to at least meet the average annual demand.
'''

model.CAb1_PlannedMaintenance_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAb1_PlannedMaintenance_rule)

model.CAb1_PlannedMaintenance_Negative_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAb1_PlannedMaintenance_Negative_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Storage Equations

model.S1_StorageLevelYearStart_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=S1_StorageLevelYearStart_rule)

model.S2_StorageLevelTSStart_constraint = Constraint(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, rule=S2_StorageLevelTSStart_rule)

# New Storage Equations and Constraints

model.S1_RateofStorageCharge_constraint = Constraint(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, rule=S1_RateofStorageCharge_rule)

model.S2_RateofStorageDischarge_constraint = Constraint(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, rule=S2_RateofStorageDischarge_rule)

model.S3_NetChargeWithinYear_constraint = Constraint(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, rule=S3_NetChargeWithinYear_rule)

model.S4_NetChargeWithinDay_constraint = Constraint(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, rule=S4_NetChargeWithinDay_rule)

model.S5_S6_StorageLevelYearStart_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=S5_S6_StorageLevelYearStart_rule)

model.S7_S8_StorageLevelYearFinish_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=S7_S8_StorageLevelYearFinish_rule)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

model.SC8_StorageRefilling_constraint = Constraint(model.STORAGE, model.REGION, rule= SC8_StorageRefilling_rule)

model.SC9_StopModeLeakage_constraint = Constraint(model.REGION, model.TIMESLICE, model.YEAR, model.MODE_OF_OPERATION, model.TECHNOLOGY, model.STORAGE, rule= SC9_StopModeLeakage_rule) 

model.NonStorageConstraint_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=NonStorageConstraint_rule)

model.SC1_LowerLimit_constraint = Constraint(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, rule= SC1_LowerLimit_rule) 
        
model.SC1a_LowerLimitEndofModelPeriod_constraint = Constraint(model.STORAGE, model.YEAR, model.REGION, rule=SC1a_LowerLimitEndofModelPeriod_rule)

model.SC2_UpperLimit_constraint = Constraint(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, rule=SC2_UpperLimit_rule)

model.SC2a_UpperLimitEndofModelPeriod_constraint = Constraint(model.STORAGE,model.YEAR,model.REGION, rule=SC2a_UpperLimitEndofModelPeriod_rule)

model.SC2a_UpperLimitEndofModelPeriod_Negative_constraint = Constraint(model.STORAGE, model.YEAR, model.REGION, rule= SC2a_UpperLimitEndofModelPeriod_Negative_rule)

model.SC7_StorageMaxUpperLimit_constraint = Constraint(model.STORAGE, model.YEAR, model.REGION, rule= SC7_StorageMaxUpperLimit_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Storage Investments

'''
Calculates the total discounted capital costs expenditure for each storage technology in each year.
'''

model.SI6_SalvageValueStorageAtEndOfPeriod1_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=SI6_SalvageValueStorageAtEndOfPeriod1_rule)

model.SI7_SalvageValueStorageAtEndOfPeriod2_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=SI7_SalvageValueStorageAtEndOfPeriod2_rule)

model.SI8_SalvageValueStorageAtEndOfPeriod3_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=SI8_SalvageValueStorageAtEndOfPeriod3_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Salvage Value 

'''
Calculates the fraction of the initial capital cost that can be recouped at the end of a technologies operational life. 
The salvage value can be calculated using one of two depreciation methods: straight line and sinking fund.
'''

model.SV1_SalvageValueAtEndOfPeriod1_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV1_SalvageValueAtEndOfPeriod1_rule)

model.SV2_SalvageValueAtEndOfPeriod2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV2_SalvageValueAtEndOfPeriod2_rule)

model. SV3_SalvageValueAtEndOfPeriod3_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV3_SalvageValueAtEndOfPeriod3_rule)

model.SV4_SalvageValueDiscountedToStartYear_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV4_SalvageValueDiscountedToStartYear_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Total Capacity Constraints

'''
Ensures that the total capacity of each technology in each year is greater than and less 
than the user-defined parameters TotalAnnualMinCapacityInvestment and TotalAnnualMaxCapacityInvestment respectively.
'''

model.TCC1_TotalAnnualMaxCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TCC1_TotalAnnualMaxCapacityConstraint_rule)
        
model.TCC2_TotalAnnualMinCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TCC2_TotalAnnualMinCapacityConstraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# New Capacity Constraints

'''
Ensures that the new capacity of each technology installed in each year is greater than and less than the 
user-defined parameters TotalAnnualMinCapacityInvestment and TotalAnnualMaxCapacityInvestment respectively.
'''

model.NCC1_TotalAnnualMaxNewCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=NCC1_TotalAnnualMaxNewCapacityConstraint_rule)

model.NCC2_TotalAnnualMinNewCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=NCC2_TotalAnnualMinNewCapacityConstraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Annual Activity Constraints

'''
Ensures that the total activity of each technology over each year is greater than and less than the user-defined parameters 
TotalTechnologyAnnualActivityLowerLimit and TotalTechnologyAnnualActivityUpperLimit respectively.
'''

model.AAC2_TotalAnnualTechnologyActivityUpperLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=AAC2_TotalAnnualTechnologyActivityUpperLimit_rule)

model.AAC3_TotalAnnualTechnologyActivityLowerLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=AAC3_TotalAnnualTechnologyActivityLowerLimit_rule)    

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Total Activity Constraints

'''
Ensures that the total activity of each technology over the entire model period is greater than and less than the
user-defined parameters TotalTechnologyModelPeriodActivityLowerLimit and TotalTechnologyModelPeriodActivityUpperLimit respectively.
'''

model.TAC1_TotalModelHorizonTechnologyActivity_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule=TAC1_TotalModelHorizonTechnologyActivity_rule)

model.TAC2_TotalModelHorizonTechnologyActivityUpperLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule= TAC2_TotalModelHorizonTechnologyActivityUpperLimit_rule)

model.TAC3_TotalModelHorizonTechnologyActivityLowerLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule= TAC3_TotalModelHorizenTechnologyActivityLowerLimit_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Reserve Margin Constraints

'''
Ensures that sufficient reserve capacity of specific technologies 
(ReserveMarginTagTechnology = 1) is installed such that the user-defined ReserveMargin is maintained.
'''

model.RM3_ReserveMargin_Constraint_constraint = Constraint(model.REGION, model.TIMESLICE, model.YEAR, rule= RM3_ReserveMargin_Constraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# RE Production Target

'''
Ensures that production from technologies tagged as renewable energy technologies 
(RETagTechnology = 1) is at least equal to the user-defined renewable energy (RE) target.
'''
model.RE1_FuelProductionByTechnologyAnnual_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=RE1_FuelProductionByTechnologyAnnual_rule)

model.RE2_TechIncluded_constraint = Constraint(model.REGION, model.YEAR, rule=RE2_TechIncluded_rule)

model.RE3_FuelIncluded_constraint = Constraint(model.REGION, model.YEAR, rule=RE3_FuelIncluded_rule)

model.RE4_EnergyConstraint_constraint = Constraint(model.REGION, model.YEAR, rule= RE4_EnergyConstraint_rule)

model.RE5_FuelUseByTechnologyAnnual_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=RE5_FuelUseByTechnologyAnnual_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Emissions Accounting

'''
Calculates the annual and model period emissions from each technology, for each type of emission. 
It also calculates the total associated emission penalties, if any. Finally, it ensures that emissions are maintained before 
stipulated limits that may be defined for each year and/or the entire model period.
'''

model.E5_DiscountedEmissionsPenaltyByTechnology_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule = E5_DiscountedEmissionsPenaltyByTechnology_rule)

model.E8_AnnualEmissionsLimit_constraint = Constraint(model.REGION, model.EMISSION, model.YEAR, rule= E8_AnnualEmissionsLimit_rule)

model.E9_ModelPeriodEmissionsLimit_constraint = Constraint(model.REGION, model.EMISSION, rule= E9_ModelPeriodEmissionsLimit_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Energy Balance A

'''
Ensures that demand for each commodity is met in each TimeSlice.
'''

model.EBa1_RateOfFuelProduction1_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, model.FUEL, rule=EBa1_RateOfFuelProduction1_rule) 

model.EBa2_RateOfFuelProduction2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, model.TIMESLICE, rule=EBa2_RateOfFuelProduction2_rule)

model.EBa3_RateOfFuelProduction3_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa3_RateOfFuelProduction3_rule)

model.EBa4_RateOfFuelUse1_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, model.FUEL, rule=EBa4_RateOfFuelUse1_rule)

model.EBa5_RateOfFuelUse2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, model.TIMESLICE, rule=EBa5_RateOfFuelUse2_rule)

model.EBa9_EnergyBalanceEachTS3_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa9_EnergyBalanceEachTS3_rule)

model.EBa7_EnergyBalanceEachTS1_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa7_EnergyBalanceEachTS1_rule)

model.EBa8_EnergyBalanceEachTS2_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa8_EnergyBalanceEachTS2_rule)

model.EBa9_EnergyBalanceEachTS3_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa9_EnergyBalanceEachTS3_rule)

model.EBa10_EnergyBalanceEachTS4_constraint = Constraint(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa10_EnergyBalanceEachTS4_rule)

#model.EBa11_EnergyBalanceEachTS5_constraint = Constraint( model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa11_EnergyBalanceEachTS5_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Energy Balance B

'''
Ensures that demand for each commodity is met in each Year.
'''

model.EBb3_EnergyBalanceEachYear3_constraint = Constraint(model.REGION, model.REGION, model.FUEL, model.YEAR, rule=EBb3_EnergyBalanceEachYear3_rule)

model.EBb2_EnergyBalanceEachYear2_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EBb2_EnergyBalanceEachYear2_rule)

model.EBb3_EnergyBalanceEachYear3_constraint = Constraint(model.REGION, model.REGION, model.FUEL, model.YEAR, rule=EBb3_EnergyBalanceEachYear3_rule)

#model.EBb4_EnergyBalanceEachYear4_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EBb4_EnergyBalanceEachYear4_rule)

model.EnergyBalanceEachYear4_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EnergyBalanceEachYear4_rule)

model.EnergyBalanceEachTS5_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EnergyBalanceEachTS5_rule)

model.EnergyConstraint_constraint = Constraint(model.REGION, model.YEAR, rule=EnergyConstraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Accounting Technology Production/Use

'''
Accounting equations used to generate specific intermediate variables
'''

model.Acc1_FuelProductionByTechnology_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=Acc1_FuelProductionByTechnology_rule)

model.Acc2_FuelUseByTechnology_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=Acc2_FuelUseByTechnology_rule)

model.Acc3_AverageAnnualRateOfActivity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=Acc3_AverageAnnualRateOfActivity_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Demand Constraints

model.EQ_SpecifiedDemand_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EQ_SpecifiedDemand_rule)

model.Demand_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=Demand_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Get model dual

model.dual = Suffix(direction=Suffix.IMPORT_EXPORT)

##################################################################################################
# Not necessary when running script from the command line with "pyomo" command
# Comment this section of the code out if running the model from the command line and leave the DATAFILE_FLAG as True
# Solver
if DATAFILE_FLAG is True:
    instance = model.create_instance(pyomodata_file)
else:
    instance = model.create_instance() # Casting abstract model into a concrete model instance

# Assert model instance was created and can receive data
print("Model instance created: ", instance.is_constructed())

opt = SolverFactory('glpk') # Choose solver to be used
final_result = opt.solve(instance, tee=True, load_solutions=True)

#instance.solutions.load_from(final_result) 

# Printing selected results
Selected_Results(instance)

# Debugging: create log files
Create_Log_Files(instance, final_result)