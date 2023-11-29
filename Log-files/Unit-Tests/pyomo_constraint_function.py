




from __future__ import division
import sys
from pyomo_model import ModelConstructor
from pyomo.environ import *
from pyomo.core import *
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
    
    return (result1, result2)

def CAa4b_Constraint_Capacity_rule(model, r, l, t, y):
    if not model.TechWithCapacityNeededToMeetPeakTS[r,t] != 0:
        return Constraint.Skip

    temp1 = sum(model.RateOfActivity[r, l, t, m, y] for m in model.MODE_OF_OPERATION)
    temp2 = (-1) * (sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y- yy < model.OperationalLife[r,t] and y - yy >= 0) + model.ResidualCapacity[r,t,y]) * model.CapacityFactor[r,t,l,y]*model.CapacityToActivityUnit[r,t]
    return (temp1, temp2) 

def CAa5_TotalNewCapacity_rule(model, r, t, y):
    if (not model.CapacityOfOneTechnologyUnit[r,t,y] != 0):
        return Constraint.Skip
        
    result1 = model.CapacityOfOneTechnologyUnit[r,t,y] * \
              model.NumberOfNewTechnologyUnits[r,t,y]
    result2 = model.NewCapacity[r,t,y]

    return (result1, result2)

def CAb1_PlannedMaintenance_rule(model, r, t, y):
    result1 = sum(
        sum(
            model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] 
            
            for m in model.MODE_OF_OPERATION
        )
        
        for l in model.TIMESLICE
    )

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
    
    return (result1, result2)
    
def CAb1_PlannedMaintenance_Negative_rule(model, r,t,y):
    result1 = sum(
        sum(
            model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] 
            for m in model.MODE_OF_OPERATION
        ) for l in model.TIMESLICE
    )
    result2 = sum(
        (
            ( 
                (-1) * sum(
                    model.NewCapacity[r, t, yy] 
                    for yy in model.YEAR 
                    if y - yy < model.OperationalLife[r, t] and y - yy >= 0
                ) + model.ResidualCapacity[r,t,y]
            ) * model.CapacityFactor[r, t, l, y] * model.YearSplit[l, y]
        ) 
        
        for l in model.TIMESLICE
    ) * model.AvailabilityFactor[r,t,y] * model.CapacityToActivityUnit[r,t]
    
    return (result1, result2)

def EBa10_EnergyBalanceEachTS4_rule(model, r, rr, l, f, y):
    return (model.Trade[r, rr, l, f, y], -model.Trade[rr, r, l, f, y])



def EBa11_EnergyBalanceEachTS5_rule(model, r, l, f, y):
    result1 = sum(model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,f,m,y] * model.YearSplit[l,y] for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.OutputActivityRatio[r,t,f,m,y] != 0)
    result2 = model.SpecifiedAnnualDemand[r, f, y] * model.SpecifiedDemandProfile[r, f, l, y] + sum(
        model.RateOfActivity[r, l, t, m, y] * model.InputActivityRatio[r, t, f, m, y] * model.YearSplit[l, y] for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.InputActivityRatio[r, t, f, m, y] != 0) + sum(model.Trade[r,rr,l,f,y] * model.TradeRoute[r,rr,f,y] for rr in model.REGION)
    
    return (result1, result2)


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

    return (result1, result2)


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
        
    return (result1, model.StorageLevelStart[r, s])



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
             

    return (result, model.StorageLevelTSStart[r,s,l,y])


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
    
    return (result, 0)
    

def SC9_StopModeLeakage_rule(model,r,l,y,m,t,s):
    if (model.TechnologyStorage[r,t,s,1] == 1 and m != min(model.MODE_OF_OPERATION)):
        return (model.RateOfActivity[r,l,t,m,y], 0)
    else:
        return Constraint.Skip


def NonStorageConstraint_rule(model,r,l,t,m,y): 
    if sum(model.TechnologyStorage[r,t,s,m] for s in model.STORAGE) == 0:
        return (model.RateOfActivity[r,l,t,m,y], 0)
    else:
        return (0, 0)


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

    return (result1, result2)


def SC1a_LowerLimitEndofModelPeriod_rule(model, s,y,r):
    result1 = model.MinStorageCharge[r,s,y] * sum(
        model.NewStorageCapacity[r,s,yy] + 
        model.ResidualStorageCapacity[r,s,y] 
        for yy in model.YEAR 
        if (y -yy < model.OperationalLifeStorage[r,s] and y - yy >= 0)
    )

    result2 = model.StorageLevelTSStart[r,s,max(model.TIMESLICE),y] + (-1)* sum(model.RateOfActivity[r, max(model.TIMESLICE),t,m,y]*model.TechnologyStorage[r,t,s,m] * model.YearSplit[max(model.TIMESLICE), y] for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.TechnologyStorage[r,t,s,m] > 0)

    return (result1, result2)
        

def SC2_UpperLimit_rule(model, r, s, l, y):
    result = sum(
        model.NewStorageCapacity[r,s,yy] + model.ResidualStorageCapacity[r,s,y] 
        for yy in model.YEAR 
        if y-yy <= model.OperationalLifeStorage[r,s] and y - yy >= 0
    )
    
    return (model.StorageLevelTSStart[r,s,l,y], result)   

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

    return (result1, result2)


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
    
    return (result1, result2)


def SC7_StorageMaxUpperLimit_rule(model,s,y,r):
    result = sum(
        model.NewStorageCapacity[r, s, yy] + 
        model.ResidualStorageCapacity[r, s, y]
        
        for yy in model.YEAR 
        if y - yy < model.OperationalLifeStorage[r, s] and y - yy >= 0
    )

    return (result, model.StorageMaxCapacity[r,s,y])

def SI6_SalvageValueStorageAtEndOfPeriod1_rule(model, r, s, y):
    if y + model.OperationalLifeStorage[r,s] - 1 <= max(model.YEAR):
        return (model.SalvageValueStorage[r,s,y], 0)
    else:
        return Constraint.Skip


def SI7_SalvageValueStorageAtEndOfPeriod2_rule(model, r, s, y):
    if (model.DepreciationMethod[r] == 1 and (y + model.OperationalLifeStorage[r,s] - 1) > max(model.YEAR) and model.DiscountRate[r] == 0) or (model.DepreciationMethod[r] == 2 and (y + model.OperationalLifeStorage[r,s] - 1) > max(model.YEAR)):
        return (model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y] * ((1 - max(model.YEAR) - y + 1)/model.OperationalLifeStorage[r,s]), model.SalvageValueStorage[r,s,y])
    else:
        return Constraint.Skip


def SI8_SalvageValueStorageAtEndOfPeriod3_rule(model, r,s,y):
    if model.DepreciationMethod[r] == 1 and (y + model.OperationalLifeStorage[r,s] - 1) > max(model.YEAR) and model.DiscountRate[r] > 0:
        return (model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y] * (1 - ((1 + model.DiscountRate[r])** (max(model.YEAR)- y + 1) - 1)/ ((1+model.DiscountRate[r])**model.OperationalLifeStorage[r,s] - 1)), model. SalvageValueStorage [r,s,y])
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

        return (result1, result2)

    return Constraint.Skip

def SV2_SalvageValueAtEndOfPeriod2_rule(model, r, t, y):
    if (
        model.DepreciationMethod[r] == 1 and 
        ((y + model.OperationalLife[r,t] - 1) > max(model.YEAR)) and 
        model.DiscountRate[r] == 0 or 
        (model.DepreciationMethod[r] == 2 and 
        (y + model.OperationalLife[r,t] -1) > max(model.YEAR))
    ):
        return (model.SalvageValueStorage[r,t,y], model.CapitalCost[r, t, y] * model.NewCapacity[r, t, y] * (1 - (max(model.YEAR) - y + 1) / model.OperationalLife[r, t]))

    return Constraint.Skip

def SV3_SalvageValueAtEndOfPeriod3_rule(model, r, t, y):
    if (y + model.OperationalLife[r,t] - 1) <= max(model.YEAR):
        return (model.SalvageValue[r,t,y], 0)
    else:
        return Constraint.Skip

def SV4_SalvageValueDiscountedToStartYear_rule(model, r, t, y):
    result1 = model.DiscountedSalvageValue[r, t, y]
    result2 = model.SalvageValue[r, t, y] / (
        (1 + model.DiscountRate[r]) ** (1 + max(model.YEAR) - min(model.YEAR))
    )

    return (result1, result2)

def TCC1_TotalAnnualMaxCapacityConstraint_rule(model, r, t, y):
    result1 = sum(
        model.NewCapacity[r,t,yy] 
        for yy in model.YEAR 
        if y - yy < model.OperationalLife[r,t] and y -yy >= 0
    ) + model.ResidualCapacity[r,t,y]
    
    result2 = model.TotalAnnualMaxCapacity[r,t,y]
    
    return (result1, result2)

def TCC2_TotalAnnualMinCapacityConstraint_rule(model, r, t, y):
    if model.TotalAnnualMinCapacity[r, t, y] > 0:
        result1 = sum(
            model.NewCapacity[r, t, yy] 
            for yy in model.YEAR 
            if y - yy < model.OperationalLife[r,t] and y - yy >= 0
        ) + model.ResidualCapacity[r, t, y]
        
        result2 = model.TotalAnnualMinCapacity[r, t, y]

        return (result1, result2)
    
    return Constraint.Skip
         
def NCC1_TotalAnnualMaxNewCapacityConstraint_rule(model, r,t,y):
    result1 = model.NewCapacity[r, t, y]
    result2 = model.TotalAnnualMaxCapacityInvestment[r, t, y]
    
    return (result1, result2)

def NCC2_TotalAnnualMinNewCapacityConstraint_rule(model, r, t, y):
    # print(model.NewCapacity[r, t, y] >= model.TotalAnnualMinCapacityInvestment[r, t, y])
    if model.TotalAnnualMinCapacityInvestment[r,t,y] > 0:
        result1 = model.NewCapacity[r, t, y]
        result2 = model.TotalAnnualMinCapacityInvestment[r, t, y]
        return (result1, result2)

    return Constraint.Skip

def AAC2_TotalAnnualTechnologyActivityUpperLimit_rule(model, r,t,y):
    result1 = sum(
        model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION
    )
    
    result2 = model.TotalTechnologyAnnualActivityUpperLimit[r, t, y]
    
    return (result1, result2)

def AAC3_TotalAnnualTechnologyActivityLowerLimit_rule(model, r,t,y):
    result1 = sum(
        model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION
    )
    result2 = model.TotalTechnologyAnnualActivityLowerLimit[r, t, y]

    return (result1, result2)

def TAC2_TotalModelHorizonTechnologyActivityUpperLimit_rule(model,r,t):
    result1 = sum(
        model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION 
        for y in model.YEAR
    )
    result2 = model.TotalTechnologyModelPeriodActivityUpperLimit[r, t]

    return (result1, result2)

def TAC3_TotalModelHorizenTechnologyActivityLowerLimit_rule(model, r, t):
    result1 = sum(
        model.RateOfActivity[r,l,t,m,y]* model.YearSplit[l,y] 
        for l in model.TIMESLICE 
        for m in model.MODE_OF_OPERATION 
        for y in model.YEAR
    )
    
    result2 = model.TotalTechnologyModelPeriodActivityLowerLimit[r,t]
    
    return (result1, result2)

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
    
    return (result1, result2)

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
    
    return (result1, result2)

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
    
    return (result1, result2)

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

    return (result1, result2)

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
    
    return (result1, result2)

def main():
    filename = input("Please enter the data file path")
    model = ModelConstructor("./")

    model.CAa4_ConstraintCapacity_constraint = Constraint(
        model.REGION, model.TIMESLICE, 
        model.TECHNOLOGY, model.YEAR,
        rule=CAa4_Constraint_Capacity_rule,
    )
    model.CAa4b_Constraint_Capacity_constraint = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.YEAR, rule=CAa4b_Constraint_Capacity_rule)

    model.CAa5_TotalNewCapacity_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, 
        rule=CAa5_TotalNewCapacity_rule
    )
    model.PlannedMaintenance_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, rule=CAb1_PlannedMaintenance_rule
    )
    model.PlannedMaintenance_Negative_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, 
        rule=CAb1_PlannedMaintenance_Negative_rule
    )


    model.EBa10_EnergyBalanceEachTS4_constraint = Constraint(
        model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR,
        rule=EBa10_EnergyBalanceEachTS4_rule
    )
    model.EBa11_EnergyBalanceEachTS5_constraint = Constraint(
        model.REGION, model.TIMESLICE, model.FUEL, model.YEAR,
        rule=EBa11_EnergyBalanceEachTS5_rule
    )
    model.EBb4_EnergyBalanceEachYear4_constraint = Constraint(
        model.REGION, model.FUEL, model.YEAR, rule=EBb4_EnergyBalanceEachYear4_rule
    )
    model.S1_StorageLevelYearStart_constraint = Constraint(
        model.REGION, model.STORAGE, model.YEAR, rule=S1_StorageLevelYearStart_rule
    )
    model.S2_StorageLevelTSStart_constraint = Constraint(
        model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, 
        rule=S2_StorageLevelTSStart_rule
    )
    model.SC8_StorageRefilling_constraint = Constraint(
        model.STORAGE, model.REGION, 
        rule= SC8_StorageRefilling_rule
    )
    model.SC9_StopModeLeakage_constraint = Constraint(
        model.REGION, model.TIMESLICE, model.YEAR, 
        model.MODE_OF_OPERATION, model.TECHNOLOGY, model.STORAGE, 
        rule= SC9_StopModeLeakage_rule
    ) 
    model.NonStorageConstraint_constraint = Constraint(
        model.REGION, model.TIMESLICE, model.TECHNOLOGY, 
        model.MODE_OF_OPERATION, model.YEAR, 
        rule=NonStorageConstraint_rule
    )
    model.SC1_LowerLimit_constraint = Constraint(
        model.REGION, model.STORAGE, model.TIMESLICE, 
        model.YEAR, 
        rule= SC1_LowerLimit_rule
    ) 
    model.SC1a_LowerLimitEndofModelPeriod_constraint = Constraint(
        model.STORAGE, model.YEAR, model.REGION, 
        rule=SC1a_LowerLimitEndofModelPeriod_rule
    )
    model.SC2_UpperLimit_constraint = Constraint(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR, rule=SC2_UpperLimit_rule)

    model.SC2a_UpperLimitEndofModelPeriod_constraint = Constraint(
        model.STORAGE,model.YEAR,model.REGION, 
        rule=SC2a_UpperLimitEndofModelPeriod_rule
    )
    model.SC2a_UpperLimitEndofModelPeriod_Negative_constraint = Constraint(
        model.STORAGE, model.YEAR, model.REGION, 
        rule= SC2a_UpperLimitEndofModelPeriod_Negative_rule
    )
    model.SC7_StorageMaxUpperLimit_constraint = Constraint(
        model.STORAGE, model.YEAR, model.REGION, 
        rule= SC7_StorageMaxUpperLimit_rule
    )
    model.SI6_SalvageValueStorageAtEndOfPeriod1_constraint = Constraint(
        model.REGION, model.STORAGE, model.YEAR, 
        rule=SI6_SalvageValueStorageAtEndOfPeriod1_rule
    )
    model.SI7_SalvageValueStorageAtEndOfPeriod2_constraint = Constraint(
        model.REGION, model.STORAGE, model.YEAR, 
        rule=SI7_SalvageValueStorageAtEndOfPeriod2_rule
    )
    model.SI8_SalvageValueStorageAtEndOfPeriod3_constraint = Constraint(
        model.REGION, model.STORAGE, model.YEAR, 
        rule=SI8_SalvageValueStorageAtEndOfPeriod3_rule
    )
    model.SV1_SalvageValueAtEndOfPeriod1_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV1_SalvageValueAtEndOfPeriod1_rule

    )
    model.SV2_SalvageValueAtEndOfPeriod2_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV2_SalvageValueAtEndOfPeriod2_rule)

    model. SV3_SalvageValueAtEndOfPeriod3_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SV3_SalvageValueAtEndOfPeriod3_rule)

    model.SV4_SalvageValueDiscountedToStartYear_constraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule=SV4_SalvageValueDiscountedToStartYear_rule,
    )
    model.TCC1_TotalAnnualMaxCapacityConstraint_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TCC1_TotalAnnualMaxCapacityConstraint_rule)

    model.TCC2_TotalAnnualMinCapacityConstraint_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, 
        rule=TCC2_TotalAnnualMinCapacityConstraint_rule
    )

    model.NCC1_TotalAnnualMaxNewCapacityConstraint_constraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule=NCC1_TotalAnnualMaxNewCapacityConstraint_rule,
    )

    model.NCC2_TotalAnnualMinNewCapacityConstraint_constraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule=NCC2_TotalAnnualMinNewCapacityConstraint_rule,
    )

    model.AAC2_TotalAnnualTechnologyActivityUpperLimit_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, 
        rule=AAC2_TotalAnnualTechnologyActivityUpperLimit_rule
    )
    model.AAC3_TotalAnnualTechnologyActivityLowerLimit_constraint = Constraint(
        model.REGION, model.TECHNOLOGY, model.YEAR, 
        rule=AAC3_TotalAnnualTechnologyActivityLowerLimit_rule
    )
    model.TAC2_TotalModelHorizonTechnologyActivityUpperLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule= TAC2_TotalModelHorizonTechnologyActivityUpperLimit_rule)
    model.TAC3_TotalModelHorizonTechnologyActivityLowerLimit_constraint = Constraint(model.REGION, model.TECHNOLOGY, rule= TAC3_TotalModelHorizenTechnologyActivityLowerLimit_rule)
    model.RE4_EnergyConstraint_constraint = Constraint(model.REGION, model.YEAR, rule= RE4_EnergyConstraint_rule)
    model.RM3_ReserveMargin_Constraint_constraint = Constraint(
        model.REGION, model.TIMESLICE, model.YEAR, 
        rule= RM3_ReserveMargin_Constraint_rule
    )

if __name__ == "__main__":
    main()