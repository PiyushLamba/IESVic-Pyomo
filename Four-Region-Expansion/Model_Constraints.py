from __future__ import division
import sys
from pyomo.environ import *
from pyomo.core import *
from pyomo.util.infeasible import log_infeasible_constraints
from pyomo.opt import SolverFactory

def CAa4_Constraint_Capacity_rule(model, r, l, t, y):
    if (not model.TechWithCapacityNeededToMeetPeakTS[r, t] != 0):
        return Constraint.Skip
    
    result1 = sum(
        model.RateOfActivity[r,l,t,m,y] 
        for m in model.MODE_OF_OPERATION
    )
    result2 = (
        sum(
            model.NewCapacity[r,t,yy] 
        
            for yy in model.YEAR 
            if y-yy < model.OperationalLife[r,t] and y-yy>=0
        ) + model.ResidualCapacity[r,t,y]
    ) * model.CapacityFactor[r,t,l,y] * model.CapacityToActivityUnit[r,t]
    
    return result1 <= result2

def CAa4b_Constraint_Capacity_rule(model, r, l, t, y):
    if not model.TechWithCapacityNeededToMeetPeakTS[r,t] != 0:
        return Constraint.Skip

    temp1 = sum(model.RateOfActivity[r, l, t, m, y] for m in model.MODE_OF_OPERATION)
    temp2 = (-1) * (sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y- yy < model.OperationalLife[r,t] and y - yy >= 0) + model.ResidualCapacity[r,t,y]) * model.CapacityFactor[r,t,l,y]*model.CapacityToActivityUnit[r,t]
    return temp1 >= temp2

def CAa5_TotalNewCapacity_rule(model, r, t, y):
    if (not model.CapacityOfOneTechnologyUnit[r,t,y] != 0):
        return Constraint.Skip
        
    ##result1 = model.CapacityOfOneTechnologyUnit[r,t,y] * \
     ##         model.NumberOfNewTechnologyUnits[r,t,y]
    result1 = model.CapacityOfOneTechnologyUnit[r,t,y] * model.NumberOfNewTechnologyUnits[r,t,y]
    result2 = model.NewCapacity[r,t,y]
    return result1 == result2

def CAb1_PlannedMaintenance_rule(model, r, t, y):
    result1 = sum(
                sum(model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y]
                    for m in model.MODE_OF_OPERATION )
                for l in model.TIMESLICE )

    result2 = sum(
        (
            (
                sum(
                    model.NewCapacity[r, t, yy] 
                    
                    for yy in model.YEAR 
                    if y - yy < model.OperationalLife[r, t] and y - yy >= 0
                ) + model.ResidualCapacity[r,t,y]
            ) * model.CapacityFactor[r, t, l, y] * model.YearSplit[l, y]

        ) for l in model.TIMESLICE
    ) * model.AvailabilityFactor[r,t,y] * model.CapacityToActivityUnit[r,t]
    
    return result1 <= result2

def CAb1_PlannedMaintenance_Negative_rule(model, r,t,y):
    result1 = sum(
        sum(
            model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] 
            for m in model.MODE_OF_OPERATION
        ) for l in model.TIMESLICE
    )
    
    result2 = sum(
        (-1) * 
        (
            ( 
                sum(
                    model.NewCapacity[r, t, yy] 
                    for yy in model.YEAR 
                    if y - yy < model.OperationalLife[r, t] and y - yy >= 0
                ) + model.ResidualCapacity[r,t,y]
            ) * model.CapacityFactor[r, t, l, y] * model.YearSplit[l, y]
        ) * model.AvailabilityFactor[r,t,y] * model.CapacityToActivityUnit[r,t]
        
        for l in model.TIMESLICE
    ) 
    
    return result1 >= result2


# No Shared Technology LTa1

###########################################################################################################################

def S1_StorageLevelYearStart_rule(model, r, s, y):
    if y == min(model.YEAR):
        result1 = model.StorageLevelYearStart[r, s, y]
    
    else:
        result1 = model.StorageLevelYearStart[r,s,y-1] + (-1) * sum(
                sum(
                    model.RateOfActivity[r,l,t,m,y-1] * 
                    model.TechnologyStorage[r,t,s,m]
                    for t in model.TECHNOLOGY 
                    for m in model.MODE_OF_OPERATION 
                    if model.TechnologyStorage[r,t,s,m] > 0
                ) * model.YearSplit[l,y-1]
            for l in model.TIMESLICE
        )
        
    return result1 == model.StorageLevelStart[r, s]

def S2_StorageLevelTSStart_rule(model, r, s, l, y):
    if (l == min(model.TIMESLICE)):
        return (model.StorageLevelYearStart[r, s, y], model.StorageLevelTSStart[r,s,l,y])

    result = model.StorageLevelTSStart[r,s,l-1,y] + (
        (-1) * 
        
        sum(
            model.RateOfActivity[r,l-1,t,m,y] * 
            model.TechnologyStorage[r,t,s,m] 
            for t in model.TECHNOLOGY 
            for m in model.MODE_OF_OPERATION 
            if model.TechnologyStorage[r,t,s,m] > 0
        ) * model.YearSplit[l-1,y]
    )
    
    return result == model.StorageLevelTSStart[r,s,l,y]

def SC8_StorageRefilling_rule(model, s, r):
    result = sum(
        (-1) * sum(
            model.RateOfActivity[r,l,t,m,y] * model.TechnologyStorage[r,t,s,m] 
            for y in model.YEAR for l in model.TIMESLICE 
            for t in model.TECHNOLOGY for m in model.MODE_OF_OPERATION 
            if model.TechnologyStorage[r,t,s,m] > 0
        ) * model.YearSplit[l,y] 
        
        for l in model.TIMESLICE for y in model.YEAR
    ) / max(model.TIMESLICE)
    
    return result == 0
    
def SC9_StopModeLeakage_rule(model,r,l,y,m,t,s):
    if (model.TechnologyStorage[r,t,s,1] == 1 and m != min(model.MODE_OF_OPERATION)):
        return model.RateOfActivity[r,l,t,m,y] == 0
    else:
        return Constraint.Skip

def NonStorageConstraint_rule(model,r,l,t,m,y): 
    if sum(model.TechnologyStorage[r,t,s,m] for s in model.STORAGE) == 0:
        return model.RateOfActivity[r,l,t,m,y] >= 0
    else:
        return Constraint.Skip

def SC1_LowerLimit_rule(model,r,s,l,y):
    result1 = (
        model.MinStorageCharge[r, s, y] * sum(
            model.NewStorageCapacity[r, s, yy] + 
            model.ResidualStorageCapacity[r, s, y] 
            
            for yy in model.YEAR 
            if y - yy < model.OperationalLifeStorage[r, s] and y - yy >= 0
        )
    ) 
    result2 = (model.StorageLevelTSStart[r, s, l, y])

    return result1 <= result2

def SC1a_LowerLimitEndofModelPeriod_rule(model, s,y,r):
    result1 = model.MinStorageCharge[r,s,y] * sum(
        model.NewStorageCapacity[r,s,yy] + 
        model.ResidualStorageCapacity[r,s,y] 
        for yy in model.YEAR 
        if (y -yy < model.OperationalLifeStorage[r,s] and y - yy >= 0)
    )

    result2 = model.StorageLevelTSStart[r,s,max(model.TIMESLICE),y] + (-1)* sum(model.RateOfActivity[r, max(model.TIMESLICE),t,m,y]*model.TechnologyStorage[r,t,s,m] * model.YearSplit[max(model.TIMESLICE), y] for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.TechnologyStorage[r,t,s,m] > 0)

    return result1 <= result2
        
def SC2_UpperLimit_rule(model, r, s, l, y):
    result = sum(
        model.NewStorageCapacity[r,s,yy] + model.ResidualStorageCapacity[r,s,y] 
        for yy in model.YEAR 
        if y-yy <= model.OperationalLifeStorage[r,s] and y - yy >= 0
    )
    
    return model.StorageLevelTSStart[r,s,l,y] <= result  

def SC2a_UpperLimitEndofModelPeriod_rule(model,s,y,r):
    result1 = model.StorageLevelTSStart[r, s, max(model.TIMESLICE), y] + -1 * sum(
        model.RateOfActivity[r, max(model.TIMESLICE), t, m, y] *
        model.TechnologyStorage[r, t, s, m]
        for m in model.MODE_OF_OPERATION
        for t in model.TECHNOLOGY
        if model.TechnologyStorage[r, t, s, m] > 0
    ) * model.YearSplit[max(model.TIMESLICE), y]
    
    result2 = sum(
        model.NewStorageCapacity[r, s, yy] + model.ResidualStorageCapacity[r, s, y]
        for yy in model.YEAR
        if y-yy < model.OperationalLifeStorage[r, s] and y-yy>=0
    )

    return result1 <= result2

def SC2a_UpperLimitEndofModelPeriod_Negative_rule(model,s,y,r):
    result1 = model.StorageLevelTSStart[r, s, max(model.TIMESLICE), y] + \
        (-1) * sum(
            model.RateOfActivity[r, max(model.TIMESLICE), t, m, y] * 
            model.TechnologyStorage[r, t, s, m] 
            
            for m in model.MODE_OF_OPERATION 
            for t in model.TECHNOLOGY 
            if model.TechnologyStorage[r, t, s, m] > 0
        ) * model.YearSplit[max(model.TIMESLICE),y]
    
    result2 = (-1) * sum(
        model.NewStorageCapacity[r, s, yy] + 
        model.ResidualStorageCapacity[r, s, y] 
        
        for yy in model.YEAR 
        if y - yy < model.OperationalLifeStorage[r, s] and y - yy >= 0
    ) 
    
    return result1 >= result2

def SC7_StorageMaxUpperLimit_rule(model,s,y,r):
    result = sum(
        model.NewStorageCapacity[r, s, yy] + 
        model.ResidualStorageCapacity[r, s, y]
        
        for yy in model.YEAR 
        if y - yy < model.OperationalLifeStorage[r, s] and y - yy >= 0
    )

    return result <= model.StorageMaxCapacity[r,s,y]

def SI6_SalvageValueStorageAtEndOfPeriod1_rule(model, r, s, y):
    if y + model.OperationalLifeStorage[r,s] - 1 <= max(model.YEAR):
        return model.SalvageValueStorage[r,s,y] == 0
    else:
        return Constraint.Skip

def SI7_SalvageValueStorageAtEndOfPeriod2_rule(model, r, s, y):
    if (model.DepreciationMethod[r] == 1 and (y + model.OperationalLifeStorage[r,s] - 1) > max(model.YEAR) and model.DiscountRate[r] == 0) or (model.DepreciationMethod[r] == 2 and (y + model.OperationalLifeStorage[r,s] - 1) > max(model.YEAR)):
        return model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y] * ((1 - max(model.YEAR) - y + 1)/model.OperationalLifeStorage[r,s]) == model.SalvageValueStorage[r,s,y]
    else:
        return Constraint.Skip

def SI8_SalvageValueStorageAtEndOfPeriod3_rule(model, r,s,y):
    if model.DepreciationMethod[r] == 1 and (y + model.OperationalLifeStorage[r,s] - 1) > max(model.YEAR) and model.DiscountRate[r] > 0:
        return model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y] * (1 - ((1 + model.DiscountRate[r])** (max(model.YEAR)- y + 1) - 1)/ ((1+model.DiscountRate[r])**model.OperationalLifeStorage[r,s] - 1)) == model.SalvageValueStorage [r,s,y]
    else:
        return Constraint.Skip

def SV1_SalvageValueAtEndOfPeriod1_rule(model, r, t, y):
    if (
        model.DepreciationMethod[r] == 1
        and ((y + model.OperationalLife[r, t] - 1) > max(model.YEAR))
        and model.DiscountRate[r] > 0
    ):
        result1 = model.SalvageValue[r, t, y]
        result2 = model.CapitalCost[r, t, y] * model.NewCapacity[r, t, y] * (1 - (
            ((1 + model.DiscountRate[r]) ** (max(model.YEAR) - y + 1) - 1) / 
            ((1 + model.DiscountRate[r]) ** model.OperationalLife[r, t] - 1)
            )
        )
        return result1 == result2
    return Constraint.Skip

def SV2_SalvageValueAtEndOfPeriod2_rule(model, r, t, y):
    if (
        model.DepreciationMethod[r] == 1 and 
        ((y + model.OperationalLife[r,t] - 1) > max(model.YEAR)) and 
        model.DiscountRate[r] == 0 or 
        (model.DepreciationMethod[r] == 2 and 
        (y + model.OperationalLife[r,t] -1) > max(model.YEAR))
    ):
        return model.SalvageValueStorage[r,t,y] == model.CapitalCost[r, t, y] * model.NewCapacity[r, t, y] * (1 - (max(model.YEAR) - y + 1) / model.OperationalLife[r, t])

    return Constraint.Skip

def SV3_SalvageValueAtEndOfPeriod3_rule(model, r, t, y):
    if (y + model.OperationalLife[r,t] - 1) <= max(model.YEAR):
        return model.SalvageValue[r,t,y] == 0
    else:
        return Constraint.Skip

def SV4_SalvageValueDiscountedToStartYear_rule(model, r, t, y):
    result1 = model.DiscountedSalvageValue[r, t, y]
    result2 = model.SalvageValue[r, t, y] / (
        (1 + model.DiscountRate[r]) ** (1 + max(model.YEAR) - min(model.YEAR))
    )

    return result1 == result2

def TCC1_TotalAnnualMaxCapacityConstraint_rule(model, r, t, y):
    result1 = sum(
        model.NewCapacity[r,t,yy] 
        for yy in model.YEAR 
        if y - yy < model.OperationalLife[r,t] and y -yy >= 0
    ) + model.ResidualCapacity[r,t,y]
    
    result2 = model.TotalAnnualMaxCapacity[r,t,y]
    
    return result1 <= result2

def TCC2_TotalAnnualMinCapacityConstraint_rule(model, r, t, y):
    if model.TotalAnnualMinCapacity[r, t, y] > 0:
        result1 = sum(
            model.NewCapacity[r, t, yy] 
            for yy in model.YEAR 
            if y - yy < model.OperationalLife[r,t] and y - yy >= 0
        ) + model.ResidualCapacity[r, t, y]
        
        result2 = model.TotalAnnualMinCapacity[r, t, y]

        return result1 >= result2
    
    return Constraint.Skip
         
def NCC1_TotalAnnualMaxNewCapacityConstraint_rule(model, r,t,y):
    result1 = model.NewCapacity[r, t, y]
    result2 = model.TotalAnnualMaxCapacityInvestment[r, t, y]
    
    return result1 <= result2

def NCC2_TotalAnnualMinNewCapacityConstraint_rule(model, r, t, y):
    # print(model.NewCapacity[r, t, y] >= model.TotalAnnualMinCapacityInvestment[r, t, y])
    if model.TotalAnnualMinCapacityInvestment[r,t,y] > 0:
        result1 = model.NewCapacity[r, t, y]
        result2 = model.TotalAnnualMinCapacityInvestment[r, t, y]
        return result1 >= result2

    return Constraint.Skip

def AAC2_TotalAnnualTechnologyActivityUpperLimit_rule(model, r,t,y):
    result1 = sum(
        model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION
    )
    
    result2 = model.TotalTechnologyAnnualActivityUpperLimit[r, t, y]
    
    return result1 <= result2

def AAC3_TotalAnnualTechnologyActivityLowerLimit_rule(model, r,t,y):
    result1 = sum(
        model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION
    )

    result2 = model.TotalTechnologyAnnualActivityLowerLimit[r, t, y]

    return result1 >= result2

def TAC2_TotalModelHorizonTechnologyActivityUpperLimit_rule(model,r,t):
    result1 = sum(
        model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION 
        for y in model.YEAR
    )
    result2 = model.TotalTechnologyModelPeriodActivityUpperLimit[r, t]

    return result1 <= result2

def TAC3_TotalModelHorizenTechnologyActivityLowerLimit_rule(model, r, t):
    result1 = sum(
        model.RateOfActivity[r,l,t,m,y]* model.YearSplit[l,y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION 
        for y in model.YEAR
    )
    
    result2 = model.TotalTechnologyModelPeriodActivityLowerLimit[r,t]
    
    return result1 >= result2

def RM3_ReserveMargin_Constraint_rule(model, r,l,y):
    result1 = sum(
        model.RateOfActivity[r,l,t,m,y] * 
        model.OutputActivityRatio[r,t,f,m,y] * 
        model.ReserveMarginTagFuel[r,f,y] * 
        model.ReserveMargin[r,y]
        for m in model.MODE_OF_OPERATION 
        for t in model.TECHNOLOGY 
        for f in model.FUEL 
        if model.OutputActivityRatio[r,t,f,m,y] != 0
    )

    result2 = sum(
        (
            sum(
                model.NewCapacity[r, t, yy] 
                
                for yy in model.YEAR 
                if y - yy < model.OperationalLife[r, t] and y - yy >= 0
            ) + model.ResidualCapacity[r, t, y]
        ) * model.ReserveMarginTagTechnology[r, t, y] * 
        model.CapacityToActivityUnit[r, t] 
        
        for t in model.TECHNOLOGY
    )
    
    if (type(result1) == int or type(result2) == int):
        if result1 <= result2:
            return Constraint.Feasible
        else:
            return Constraint.Infeasible

    return result1 <= result2

def RE4_EnergyConstraint_rule(model, r,y):  
    result1 = model.REMinProductionTarget[r,y] * sum(
        sum(
            model.RateOfActivity[r,l,t,m,y] * 
            model.OutputActivityRatio[r,t,f,m,y] * 
            model.YearSplit[l,y] * 
            model.RETagFuel[r,f,y] 
            
            for m in model.MODE_OF_OPERATION 
            for t in model.TECHNOLOGY 
            if model.OutputActivityRatio[r,t,f,m,y] != 0
        ) 
        
        for l in model.TIMESLICE 
        for f in model.FUEL
    )

    result2 = sum(
        model.RateOfActivity[r,l,t,m,y] *
        model.OutputActivityRatio[r,t,f,m,y] * 
        model.YearSplit[l,y] * model.RETagTechnology[r,t,y] 
        
        for m in model.MODE_OF_OPERATION 
        for l in model.TIMESLICE 
        for t in model.TECHNOLOGY
        for f in model.FUEL 
        if model.OutputActivityRatio[r,t,f,m,y] != 0
    )
    
    if (type(result1) == int or type(result2) == int):
        if result1 <= result2:
            return Constraint.Feasible
        else:
            return Constraint.Infeasible
            
    return result1 <= result2

def E5_DiscountedEmissionsPenaltyByTechnology_rule(model, r, t, y):
    result1 = sum(
        model.EmissionActivityRatio[r,t,e,m,y] * 
        model.RateOfActivity[r,l,t,m,y] * 
        model.YearSplit[l,y] * model.EmissionsPenalty[r,e,y] / 
        (
            (1 + model.DiscountRate[r]) ** (y - min(model.YEAR) + 0.5)
        ) 
        
        for e in model.EMISSION 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION 
        if model.EmissionActivityRatio[r,t,e,m,y] != 0
    )
    
    result2 = model.DiscountedTechnologyEmissionsPenalty[r,t,y]
    
    return result1 == result2

def E8_AnnualEmissionsLimit_rule(model, r,e,y):
    result1 = sum(
        model.EmissionActivityRatio[r,t,e,m,y] * 
        model.RateOfActivity[r,l,t,m,y] * 
        model.YearSplit[l,y] 
        
        for l in model.TIMESLICE 
        for t in model.TECHNOLOGY 
        for m in model.MODE_OF_OPERATION 
        if model.EmissionActivityRatio[r,t,e,m,y] != 0
    ) + model.AnnualExogenousEmission[r,e,y]
    
    result2 = model.AnnualEmissionLimit[r, e, y]

    return result1 <= result2

def E9_ModelPeriodEmissionsLimit_rule(model, r,e):
    result1 = sum(
        model.EmissionActivityRatio[r,t,e,m,y] * 
        model.RateOfActivity[r,l,t,m,y] * 
        model.YearSplit[l,y] + 
        model.ModelPeriodExogenousEmission[r,e] 
        
        for l in model.TIMESLICE 
        for t in model.TECHNOLOGY 
        for m in model.MODE_OF_OPERATION 
        for y in model.YEAR 
        if model.EmissionActivityRatio[r,t,e,m,y] != 0
    )

    result2 = model.ModelPeriodEmissionLimit[r, e]
    
    return result1 <= result2

def Acc3_AverageAnnualRateOfActivity_rule(model, r, t, m, y): 
    result1 = sum( model.RateOfActivity[r, l, t, m, y] * model.YearSplit [l, y] for l in model.TIMESLICE)
    result2 = model.TotalAnnualTechnologyActivityByMode [r, t, m, y]
    return result1 == result2

def CAa1_TotalNewCapacity_rule(model, r, t, y):
    result1 = model.AccumulatedNewCapacity [r, t, y] 
    result2 = sum(model.NewCapacity [r, t, yy]
                for yy in model.YEAR if y -yy < model.OperationalLife[r, t] and y - yy >= 0)
    return result1 == result2

def CAa2_TotalAnnualCapacity_rule(model, r, t, y):
    result1 = model.AccumulatedNewCapacity[r, t, y] + model.ResidualCapacity[r, t, y] 
    result2 = model.TotalCapacityAnnual[r, t, y]
    return result1 == result2

def CC1_UndiscountedCapitalInvestment_rule(model, r, t, y):
    result1 =  model.CapitalCost[r, t, y] * model.NewCapacity[r, t, y]
    result2 = model.CapitalInvestment[r, t, y]
    return result1 == result2

def OC1_OperatingCostsVariable_rule(model, r, t, y):
    result1 = sum(model.TotalAnnualTechnologyActivityByMode[r, t, m, y] * model.VariableCost[r, t, m, y]
                for m in model.MODE_OF_OPERATION)
    result2 = model.AnnualVariableOperatingCost[r, t, y]
    return result1 == result2

def TAC1_TotalModelHorizonTechnologyActivity_rule(model, r, t):
    result1 = sum(model.TotalTechnologyAnnualActivity[r, t, y] for y in model.YEAR)
    result2 = model.TotalTechnologyModelPeriodActivity[r, t]
    return result1 == result2

############################################### USE ###############################################################################

def EBa4_RateOfFuelUse1_rule(model, r, l, t, m, y, f):
    if(model.InputActivityRatio[r, t, f, m, y] != 0):
        result1 = model.RateOfActivity[r, l, t, m, y] * model.InputActivityRatio[r, t, f, m, y] 
        result2 = model.RateOfUseByTechnologyByMode [r, l, t, m, f, y]
        return result1 == result2
    else:
        return Constraint.Skip    

def EBa5_RateOfFuelUse2_rule(model, r, t, f, y, l):
    result1 = sum(model.RateOfUseByTechnologyByMode [r, l, t, m, f, y] 
                for m in model.MODE_OF_OPERATION
                if model.InputActivityRatio [r, t, f, m, y] != 0)
    result2 = model.RateOfUseByTechnology [r, l, t, f, y]
    return result1 == result2

def Acc2_FuelUseByTechnology_rule(model, r, l, t, f, y):
    result1 = model.RateOfUseByTechnology[r, l, t, f, y] * model.YearSplit [l, y] 
    result2 = model.UseByTechnology [r, l, t, f, y]
    return result1 == result2

def RE5_FuelUseByTechnologyAnnual_rule(model, r, t, f, y):
	result1 = sum(model.RateOfUseByTechnology[r, l, t, f, y] * model.YearSplit[l, y]
			    for l in model.TIMESLICE)
	result2 = model.UseByTechnologyAnnual[r, t, f, y]
	return result1 == result2

def EBa6_RateOfFuelUse3_rule(model, r, l, f, y):
    result1 = sum(model.RateOfUseByTechnology[r, l, t, f, y] for t in model.TECHNOLOGY)
    result2 = model.RateOfUse[r, l, f, y]
    return result1 == result2

def EBa8_EnergyBalanceEachTS2_rule(model, r, l, f, y):
	result1 = model.RateOfUse[r, l, f, y] * model.YearSplit[l, y]
	result2 = model.Use[r, l, f, y]
	return result1 == result2

def EBb2_EnergyBalanceEachYear2_rule(model, r, f, y): 
    result1 = sum(model.Use[r, l, f, y] 
                for l in model.TIMESLICE)
    result2 = model.UseAnnual[r, f, y]
    return result1 == result2

############################################# PRODUCTION ###########################################################################    

def EBa1_RateOfFuelProduction1_rule(model, r, l, t, m, y, f):
    if (model.OutputActivityRatio[r, t, f, m, y] != 0): 
        result1 = model.RateOfActivity[r, l, t, m, y] * model.OutputActivityRatio[r, t, f, m, y] 
        result2 = model.RateOfProductionByTechnologyByMode[r, l, t, m, f, y]
        return result1 == result2
    else:
        return Constraint.Skip 

def EBa2_RateOfFuelProduction2_rule(model, r, t, f, y, l):
    result1 = sum(model.RateOfProductionByTechnologyByMode[r, l, t, m, f, y] 
                for m in model.MODE_OF_OPERATION if model.OutputActivityRatio[r, t, f, m, y] != 0)
    result2 = model.RateOfProductionByTechnology[r, l, t, f, y]
    return result1 == result2

def EBa3_RateOfFuelProduction3_rule(model, r, l, f, y):
    result1 = sum(model.RateOfProductionByTechnology[r, l, t, f, y] for t in model.TECHNOLOGY)
    result2 = model.RateOfProduction[r, l, f, y]
    return result1 == result2

def EBa7_EnergyBalanceEachTS1_rule(model, r, l, f, y):
    result1 = model.RateOfProduction[r, l, f, y] * model.YearSplit[l, y]
    result2 = model.Production[r, l, f, y]
    return result1 == result2

def EBb1_EnergyBalanceEachYear1_rule(model, r , f , y):
    result1 = sum(model.Production[r, l, f, y] for l in model.TIMESLICE)
    result2 = model.ProductionAnnual[r, f, y]
    return result1 == result2
'''
def EBa11_EnergyBalanceEachTS5_rule(model, r, l, f, y):
    result1 = sum(model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,f,m,y] * model.YearSplit[l,y] 
               for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.OutputActivityRatio[r,t,f,m,y] != 0)          
    #result1 = model.Production[r, l, f, y]
    result2 = model.SpecifiedAnnualDemand[r, f, y] * model.SpecifiedDemandProfile[r, f, l, y] + sum(
                model.RateOfActivity[r, l, t, m, y] * model.InputActivityRatio[r, t, f, m, y] * model.YearSplit[l, y] 
                for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.InputActivityRatio[r, t, f, m, y] != 0) + sum(
                    model.Trade[r,rr,l,f,y] * model.TradeRoute[r,rr,f,y] for rr in model.REGION)
    #result2 = model.Demand[r, l, f, y] + model.Use[r, l, f, y] + sum(
    #           model.Trade[r, rr, l, f, y] * model.TradeRoute [r, rr, f, y] for rr in model.REGION)
    return result1 >= result2
'''
def EnergyBalanceEachTS5_rule(model, r, l, f, y):
	result1 = model.Production[r, l, f, y] 
	result2 = model.Demand[r, l, f, y] + model.Use[r, l, f, y] + sum(model.Trade[r, rr, l, f, y] * model.TradeRoute[r, rr, f, y]
                                                                       for rr in model.REGION)
	return result1 == result2

def EnergyBalanceEachYear4_rule(model, r, f, y):
    #result1 = sum(model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,f,m,y] * model.YearSplit[l,y] 
    #              for l in model.TIMESLICE for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY 
    #             if model.OutputActivityRatio[r,t,f,m,y] != 0)
    result1 = model.ProductionAnnual[r, f, y]
    result2 = model.UseAnnual[r,f,y] + sum( 
                model.TradeAnnual[r, rr, f, y] * model.TradeRoute[r, rr, f, y] 
                for rr in model.REGION) + model.AccumulatedAnnualDemand[r, f, y]
    
    return result1 >= result2

def RE3_FuelIncluded_rule(model, r, y):
	result1 = sum(model.RateOfProduction[r, l, f, y] * model.RETagFuel[r, f, y] * model.YearSplit[l, y]
			    for f in model.FUEL for l in model.TIMESLICE)
	result2 = model.RETotalProductionOfTargetFuelAnnual[r, y]
	return result1 == result2

def Acc1_FuelProductionByTechnology_rule(model, r, l, t, f, y):
    result1 = model.RateOfProductionByTechnology[r, l, t, f, y] * model.YearSplit[l, y] 
    result2 = model.ProductionByTechnology[r, l, t, f, y]
    return result1 == result2

def RE1_FuelProductionByTechnologyAnnual_rule(model, r, t, f, y):
    #result1 =  sum(model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,f,m,y] * model.YearSplit [l,y] for l in model.TIMESLICE
    #                for m in model.MODE_OF_OPERATION if model.OutputActivityRatio [r,t,f,m,y] != 0)
    result1 = sum(model.ProductionByTechnology[r, l, t, f, y] for l in model.TIMESLICE)
    result2 = model.ProductionByTechnologyAnnual[r, t, f, y]
    return result1 == result2

def RE2_TechIncluded_rule(model, r, y):
	result1 = sum(model.ProductionByTechnologyAnnual[r, t, f, y] * model.RETagTechnology[r, t, y]
			    for t in model.TECHNOLOGY for f in model.FUEL)
	result2 = model.TotalREProductionAnnual[r, y]
	return result1 == result2

def EnergyConstraint_rule(model, r, y):
	result1 = model.REMinProductionTarget[r, y] * model.RETotalProductionOfTargetFuelAnnual[r, y]
	result2 = model.TotalREProductionAnnual[r, y]
	return result1 <= result2

################################################## DEMAND ##########################################################################

def EQ_SpecifiedDemand_rule(model, r, l, f, y):
    result1 = model.SpecifiedAnnualDemand[r, f, y] * model.SpecifiedDemandProfile[r, f, l, y] / model.YearSplit[l, y]
    result2 = model.RateOfDemand[r, l, f, y]
    return result1 == result2

def EBa9_EnergyBalanceEachTS3_rule(model, r, l, f, y):
    result1 = model.RateOfDemand[r, l, f, y] * model.YearSplit[l, y]
    result2 = model.Demand[r, l, f, y]
    return result1 == result2

#def EBa9_EnergyBalanceEachTS3_rule(model, r, f, y, l):
#    result1 =  model.SpecifiedAnnualDemand[r, f, y] * model.SpecifiedDemandProfile[r, f, l, y] 
#    result2 = model.Demand[r, l, f, y]
#    return result1 == result2

def Demand_rule(model, r, f, y):
    result1 = sum(model.Demand[r, l, f, y] for l in model.TIMESLICE)
    result2 = model.DemandAnnual[r, f, y]
    return result1 == result2

################################################# TRADE ###########################################################################

def EBa10_EnergyBalanceEachTS4_rule(model, r, rr, l, f, y):
    result1 = model.Trade[r, rr, l, f, y]
    result2 = -model.Trade[rr, r, l, f, y]
    return result1 == result2

def EBb3_EnergyBalanceEachYear3_rule(model, r, rr, f , y):
    result1 = sum(model.Trade[r,rr,l,f,y] 
                for l in model.TIMESLICE)
    return result1 == model.TradeAnnual[r,rr,f,y] 

'''
def EBb4_EnergyBalanceEachYear4_rule(model, r, f, y):
    result1 = sum(
        model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,f,m,y] * 
        model.YearSplit[l,y] 
        
        for m in model.MODE_OF_OPERATION 
        for t in model.TECHNOLOGY 
        for l in model.TIMESLICE 
        if model.OutputActivityRatio[r,t,f,m,y] != 0
    )
    
    result2 = sum(
        model.RateOfActivity[r, l, t, m, y] * 
        model.InputActivityRatio[r, t, f, m, y] * 
        model.YearSplit[l, y] 
        
        for m in model.MODE_OF_OPERATION 
        for t in model.TECHNOLOGY 
        for l in model.TIMESLICE 
        if model.InputActivityRatio[r, t, f, m, y] != 0
    ) + sum(
        model.Trade[r,rr,l,f,y] * model.TradeRoute[r,rr,f,y] 
        
        for l in model.TIMESLICE 
        for rr in model.REGION
    ) + model.AccumulatedAnnualDemand[r,f,y]

    return result1 >= result2
'''

'''
def OC4_DiscountedOperatingCostsTotalAnnual_rule(model, r, t, y):
    if (sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0}:
        result1 = model.NewCapacity[r,t,yy] + model.ResidualCapacity[r,t,y] * model.FixedCost[r,t,y] + 
                    sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*VariableCost[r,t,m,y])/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))
        result2 = model.DiscountedOperatingCost[r,t,y]
        return result1 == result2
    else:
        return Constraint.Skip
'''
