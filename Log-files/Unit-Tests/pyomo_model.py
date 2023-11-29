from pyomo.environ import *
from pyomo.core import *

def ModelConstructor(filename = None):
    model = AbstractModel() # Create model object and give it a name

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
    model.FLEXIBLEDEMANDTYPE = Set()
    model.STORAGE = Set()

    model.YearSplit = Param(model.TIMESLICE, model.YEAR)
    model.DiscountRate = Param(model.REGION)
    model.DaySplit = Param(model.DAILYTIMEBRACKET, model.YEAR)
    model.Conversionls = Param(model.TIMESLICE, model.SEASON)
    model.Conversionld = Param(model.TIMESLICE, model.DAYTYPE)
    model.Conversionlh = Param(model.TIMESLICE, model.DAILYTIMEBRACKET)
    model.DaysInDayType = Param(model.SEASON, model.DAYTYPE, model.YEAR)
    model.TradeRoute = Param(model.REGION, model.REGION, model.FUEL, model.YEAR)
    model.DepreciationMethod = Param(model.REGION)
    model.SpecifiedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR)
    model.SpecifiedDemandProfile = Param(model.REGION, model.FUEL, model.TIMESLICE, model.YEAR)
    model.AccumulatedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR)
    model.CapacityToActivityUnit = Param(model.REGION, model.TECHNOLOGY)
    model.TechWithCapacityNeededToMeetPeakTS = Param(model.REGION, model.TECHNOLOGY)
    model.CapacityFactor = Param(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR)
    model.AvailabilityFactor = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.OperationalLife = Param(model.REGION, model.TECHNOLOGY)
    model.ResidualCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.InputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR)
    model.OutputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR)
    model.CapitalCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.VariableCost = Param(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR)
    model.FixedCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.TechnologyStorage = Param(model.REGION, model.TECHNOLOGY, model.STORAGE, model.MODE_OF_OPERATION)
    model.StorageMaxChargeRate = Param(model.REGION, model.STORAGE)
    model.StorageMaxDischargeRate = Param(model.REGION, model.STORAGE)
    model.MinStorageCharge = Param(model.REGION, model.STORAGE, model.YEAR)
    model.OperationalLifeStorage = Param(model.REGION, model.STORAGE)
    model.CapitalCostStorage = Param(model.REGION, model.STORAGE, model.YEAR)
    model.ResidualStorageCapacity = Param(model.REGION, model.STORAGE, model.YEAR)
    model.StorageMaxCapacity = Param(model.REGION, model.STORAGE, model.YEAR)


    model.CapacityOfOneTechnologyUnit = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.TotalAnnualMaxCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.TotalAnnualMinCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR)


    model.TotalAnnualMaxCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.TotalAnnualMinCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR)


    model.TotalTechnologyAnnualActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.TotalTechnologyAnnualActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.TotalTechnologyModelPeriodActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY)
    model.TotalTechnologyModelPeriodActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY)


    model.ReserveMarginTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.ReserveMarginTagFuel = Param(model.REGION, model.FUEL, model.YEAR)
    model.ReserveMargin = Param(model.REGION, model.YEAR)


    model.RETagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.RETagFuel = Param(model.REGION, model.FUEL, model.YEAR)
    model.REMinProductionTarget = Param(model.REGION, model.YEAR)


    model.EmissionActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.EMISSION, model.MODE_OF_OPERATION, model.YEAR)
    model.EmissionsPenalty = Param(model.REGION, model.EMISSION, model.YEAR)
    model.AnnualExogenousEmission = Param(model.REGION, model.EMISSION, model.YEAR)
    model.AnnualEmissionLimit = Param(model.REGION, model.EMISSION, model.YEAR)
    model.ModelPeriodExogenousEmission = Param(model.REGION, model.EMISSION)
    model.ModelPeriodEmissionLimit = Param(model.REGION, model.EMISSION)
    model.StoredEnergyValue = Param(model.REGION, model.STORAGE)
    model.StorageLevelStart = Param(model.REGION, model.STORAGE)
    model.StorageLevelTSStart = Param(model.REGION, model.STORAGE, model.TIMESLICE, model.YEAR)
    model.NewStorageCapacity = Param(model.REGION, model.STORAGE, model.YEAR)
    model.SalvageValueStorage = Param(model.REGION, model.STORAGE, model.YEAR)
    model.StorageLevelYearStart = Param(model.REGION, model.STORAGE, model.YEAR)
    model.StorageLevelYearFinish = Param(model.REGION, model.STORAGE, model.YEAR)
    model.StorageLevelSeasonStart = Param(model.REGION, model.STORAGE, model.SEASON, model.YEAR)
    model.StorageLevelDayTypeStart = Param(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR)
    model.StorageLevelDayTypeFinish = Param(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR)
    model.NumberOfNewTechnologyUnits = Param(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeIntegers )
    model.NewCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.RateOfActivity = Param(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR)
    model.UseByTechnology = Param(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals)
    model.Trade = Param(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR)
    model.UseAnnual = Param(model.REGION, model.FUEL, model.YEAR)
    model.VariableOperatingCost = Param(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR)
    model.SalvageValue = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.DiscountedSalvageValue = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.OperatingCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.DiscountedTechnologyEmissionsPenalty = Param(model.REGION, model.TECHNOLOGY, model.YEAR)
    model.ModelPeriodEmissions = Param(model.REGION, model.EMISSION)
    
    instance = model.create_instance(filename)

    return instance