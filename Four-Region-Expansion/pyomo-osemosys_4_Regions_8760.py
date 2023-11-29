# Pyomo OSeMOSYS
# IESVic - 2021

# Import relevant Python modules

from __future__ import division
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
from Model_Sel_Res import *



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
sets_file = "./New_Changes/4_Regions_8760/Model_Sets_4_Regions_8760.xlsx"
parameters_file = "./New_Changes/4_Regions_8760/Model_Parameters_4_Regions_8760.xlsx"
#pyomodata_file =  "./Model-data/OSeMOSYS_Test_params.dat"
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

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


#CONVERSIONLH_df = pd.DataFrame(pd.read_excel(parameters_file, sheet_name="Conversionlh"))

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

##################################################################################################

# Data processing

rows = []
for a in range(1, 8761):
    for b in range(1, 8761):
        rows.append(['Yes', b, a, 0])

CONVERSIONLH_df = pd.DataFrame(rows, columns= ['Included','Timeslice', 'Daily_Timebracket', 'Conversionlh'])
#print(CONVERSIONLH_df)


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


#print("Created Sets")
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
model.SimultaneityTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, default=0)

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
model.ResidualStorageCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0,
                            initialize=Process_Data(RESIDUALSTORAGECAPACITY_df, component="parameter"))
# TN 2016 04 Added Storage Maximum:
model.StorageMaxCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0,
                        initialize=Process_Data(STORAGEMAXCAPACITY_df, component="parameter"))

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

model.StorageLevelStart = Var(model.REGION, model.STORAGE, bounds=(0, None), domain=Reals)

# Demands 

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# New
model.CapitalInvestment = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals)
model.RateOfUseByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None)) 
model.RateOfUseByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.FUEL, model.YEAR, bounds=(0, None)) 


# Storage

model.StorageLevelTSStart = Var(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, bounds = (0, None), domain=Reals)
model.NewStorageCapacity = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.SalvageValueStorage = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelYearStart = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals)
model.StorageLevelYearFinish = Var(model.REGION, model.STORAGE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelSeasonStart = Var(model.REGION, model.STORAGE, model.SEASON, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelDayTypeStart = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.StorageLevelDayTypeFinish = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR, bounds=(0, None), domain=Reals, initialize=rand_init)


#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Capacity Variables

model.NumberOfNewTechnologyUnits = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Integers, initialize=0)
model.NewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init) # This vaiable must be within Real numbers for feasible solution


#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Activity Variables

model.RateOfActivity = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, domain=Reals)  # Eliminated the >=0 constraint (PMT)
model.UseByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds=(0, None), domain=Reals, initialize=rand_init)
model.Trade = Var(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=Reals)
model.TradeAnnual = Var(model.REGION, model.REGION, model.FUEL, model.YEAR)
model.UseAnnual = Var(model.REGION, model.FUEL, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.Use = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, bounds=(0, None))
model.ProductionAnnual = Var(model.REGION, model.FUEL, model.YEAR, domain=NonNegativeReals, bounds=(0, None))
model.Production = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, bounds=(0, None))
model.Demand = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, bounds=(0, None))
model.DemandAnnual = Var(model.REGION, model.FUEL, model.YEAR, bounds=(0, None))

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Costing Variables

model.VariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, bounds=(0, None), domain=Reals, initialize=rand_init)
model.SalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals)
model.DiscountedSalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.OperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# RE Gen Target  


#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Emissions

model.DiscountedTechnologyEmissionsPenalty = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None), domain=Reals, initialize=rand_init)
model.ModelPeriodEmissions = Var(model.REGION, model.EMISSION, bounds = (0, None), domain=Reals, initialize=rand_init)

# New variables########################################################

model.ProductionByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None))
model.ProductionByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None))
model.RateOfProductionByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, bounds = (0, None))
model.RateOfProductionByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.FUEL, model.YEAR, bounds = (0, None))
model.TotalAnnualTechnologyActivityByMode = Var(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, bounds = (0, None))
model.AccumulatedNewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None))
model.TotalCapacityAnnual = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None))
model.AnnualVariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR)
model.TotalTechnologyAnnualActivity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, bounds = (0, None))
model.TotalTechnologyModelPeriodActivity = Var(model.REGION, model.TECHNOLOGY)

model.RateOfDemand = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalREProductionAnnual = Var(model.REGION, model.YEAR, initialize=0.0)
model.RETotalProductionOfTargetFuelAnnual = Var(model.REGION, model.YEAR, initialize=0.0)
model.RateOfProduction = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.UseByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfUse = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)

###########################################################
#print("Created Variables")

##################################################################################################

# Objective Function

model.OBJ = Objective(rule=ObjectiveFunctionRule, sense= minimize)


##################################################################################################

# Model Constraints

model.CC1_UndiscountedCapitalInvestment_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CC1_UndiscountedCapitalInvestment_rule)

model.Acc3_AverageAnnualRateOfActivity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=Acc3_AverageAnnualRateOfActivity_rule)

model.CAa1_TotalNewCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAa1_TotalNewCapacity_rule)

model.CAa2_TotalAnnualCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAa2_TotalAnnualCapacity_rule)

model.OC1_OperatingCostsVariable_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=OC1_OperatingCostsVariable_rule)

model.TAC1_TotalModelHorizonTechnologyActivity_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule=TAC1_TotalModelHorizonTechnologyActivity_rule)

# Capacity Adequacy A	

model.CAa5_TotalNewCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAa5_TotalNewCapacity_rule)

model.CAa4_ConstraintCapacity_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.YEAR, rule=CAa4_Constraint_Capacity_rule,)

model.CAa4b_Constraint_Capacity_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.YEAR, rule=CAa4b_Constraint_Capacity_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Capacity Adequacy B

model.CAb1_PlannedMaintenance_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAb1_PlannedMaintenance_rule)

model.CAb1_PlannedMaintenance_Negative_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAb1_PlannedMaintenance_Negative_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Storage Equations

model.S1_StorageLevelYearStart_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=S1_StorageLevelYearStart_rule)

model.S2_StorageLevelTSStart_constraint = Constraint(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, rule=S2_StorageLevelTSStart_rule)
    
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

model.SI6_SalvageValueStorageAtEndOfPeriod1_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=SI6_SalvageValueStorageAtEndOfPeriod1_rule)

model.SI7_SalvageValueStorageAtEndOfPeriod2_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=SI7_SalvageValueStorageAtEndOfPeriod2_rule)

model.SI8_SalvageValueStorageAtEndOfPeriod3_constraint = Constraint(model.REGION, model.STORAGE, model.YEAR, rule=SI8_SalvageValueStorageAtEndOfPeriod3_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Salvage Value 

model.SV1_SalvageValueAtEndOfPeriod1_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV1_SalvageValueAtEndOfPeriod1_rule)

model.SV2_SalvageValueAtEndOfPeriod2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV2_SalvageValueAtEndOfPeriod2_rule)

model. SV3_SalvageValueAtEndOfPeriod3_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV3_SalvageValueAtEndOfPeriod3_rule)

model.SV4_SalvageValueDiscountedToStartYear_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV4_SalvageValueDiscountedToStartYear_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Total Capacity Constraints

model.TCC1_TotalAnnualMaxCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TCC1_TotalAnnualMaxCapacityConstraint_rule)
        
model.TCC2_TotalAnnualMinCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TCC2_TotalAnnualMinCapacityConstraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# New Capacity Constraints

model.NCC1_TotalAnnualMaxNewCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=NCC1_TotalAnnualMaxNewCapacityConstraint_rule)

model.NCC2_TotalAnnualMinNewCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=NCC2_TotalAnnualMinNewCapacityConstraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Annual Activity Constraints

model.AAC2_TotalAnnualTechnologyActivityUpperLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=AAC2_TotalAnnualTechnologyActivityUpperLimit_rule)

model.AAC3_TotalAnnualTechnologyActivityLowerLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=AAC3_TotalAnnualTechnologyActivityLowerLimit_rule)    

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Total Activity Constraints

model.TAC2_TotalModelHorizonTechnologyActivityUpperLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule= TAC2_TotalModelHorizonTechnologyActivityUpperLimit_rule)

model.TAC3_TotalModelHorizonTechnologyActivityLowerLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule= TAC3_TotalModelHorizenTechnologyActivityLowerLimit_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Reserve Margin Constraints

model.RM3_ReserveMargin_Constraint_constraint = Constraint(model.REGION, model.TIMESLICE, model.YEAR, rule= RM3_ReserveMargin_Constraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# RE Production Target

model.RE4_EnergyConstraint_constraint = Constraint(model.REGION, model.YEAR, rule= RE4_EnergyConstraint_rule)

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

# Emissions Accounting E8_AnnualEmissionsLimit_rule

model.E5_DiscountedEmissionsPenaltyByTechnology_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule = E5_DiscountedEmissionsPenaltyByTechnology_rule)

model.E8_AnnualEmissionsLimit_constraint = Constraint(model.REGION, model.EMISSION, model.YEAR, rule= E8_AnnualEmissionsLimit_rule)

model.E9_ModelPeriodEmissionsLimit_constraint = Constraint(model.REGION, model.EMISSION, rule= E9_ModelPeriodEmissionsLimit_rule)

#################################################### USE CONSTRAINTS #####################################################################################

model.EBa4_RateOfFuelUse1_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, model.FUEL, rule=EBa4_RateOfFuelUse1_rule)

model.EBa5_RateOfFuelUse2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, model.TIMESLICE, rule=EBa5_RateOfFuelUse2_rule)

model.Acc2_FuelUseByTechnology_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=Acc2_FuelUseByTechnology_rule)

model.RE5_FuelUseByTechnologyAnnual_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=RE5_FuelUseByTechnologyAnnual_rule)

model.EBa6_RateOfFuelUse3_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa6_RateOfFuelUse3_rule)

model.EBa8_EnergyBalanceEachTS2_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa8_EnergyBalanceEachTS2_rule)

model.EBb2_EnergyBalanceEachYear2_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EBb2_EnergyBalanceEachYear2_rule)

#################################################### PRODUCTION CONSTRAINT ###################################################################

model.EBa1_RateOfFuelProduction1_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, model.FUEL, rule=EBa1_RateOfFuelProduction1_rule) 

model.EBa2_RateOfFuelProduction2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, model.TIMESLICE, rule=EBa2_RateOfFuelProduction2_rule)

model.EBa3_RateOfFuelProduction3_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa3_RateOfFuelProduction3_rule)

model.EBa7_EnergyBalanceEachTS1_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa7_EnergyBalanceEachTS1_rule)

model.EBb1_EnergyBalanceEachYear1_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EBb1_EnergyBalanceEachYear1_rule)

#model.EBa11_EnergyBalanceEachTS5_constraint = Constraint( model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa11_EnergyBalanceEachTS5_rule)

model.EnergyBalanceEachYear4_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EnergyBalanceEachYear4_rule)

model.EnergyBalanceEachTS5_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EnergyBalanceEachTS5_rule)

model.RE3_FuelIncluded_constraint = Constraint(model.REGION, model.YEAR, rule=RE3_FuelIncluded_rule)

model.Acc1_FuelProductionByTechnology_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=Acc1_FuelProductionByTechnology_rule)

model.RE1_FuelProductionByTechnologyAnnual_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=RE1_FuelProductionByTechnologyAnnual_rule)

model.RE2_TechIncluded_constraint = Constraint(model.REGION, model.YEAR, rule=RE2_TechIncluded_rule)

model.EnergyConstraint_constraint = Constraint(model.REGION, model.YEAR, rule=EnergyConstraint_rule)

#################################################### DEMAND CONSTRAINT ##################################################################

model.EQ_SpecifiedDemand_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EQ_SpecifiedDemand_rule)

model.EBa9_EnergyBalanceEachTS3_constraint = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa9_EnergyBalanceEachTS3_rule)

#model.EBa9_EnergyBalanceEachTS3_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, model.TIMESLICE, rule=EBa9_EnergyBalanceEachTS3_rule)

model.Demand_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=Demand_rule)

#################################################### TRADE CONSTRAINT ####################################################################

model.EBa10_EnergyBalanceEachTS4_constraint = Constraint(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EBa10_EnergyBalanceEachTS4_rule)

model.EBb3_EnergyBalanceEachYear3_constraint = Constraint(model.REGION, model.REGION, model.FUEL, model.YEAR, rule=EBb3_EnergyBalanceEachYear3_rule)

#model.EBb4_EnergyBalanceEachYear4_constraint = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EBb4_EnergyBalanceEachYear4_rule)

# Get model dual

model.dual = Suffix(direction=Suffix.IMPORT_EXPORT)

##################################################################################################
# Not necessary when running script from the command line with "pyomo" command
# Comment this section of the code out if running the model from the command line
# Solver

#instance = model.create_instance(pyomodata_file)
instance = model.create_instance() # Casting abstract model into a concrete model instance

# Assert model instance was created and can receive data
print("Model instance created: ", instance.is_constructed())

opt = SolverFactory('glpk') # Choose solver to be used
final_result = opt.solve(instance, tee=True)

# Debugging: create log files
Create_Log_Files(instance, final_result)

# Printing selected results
Selected_Results(instance)
