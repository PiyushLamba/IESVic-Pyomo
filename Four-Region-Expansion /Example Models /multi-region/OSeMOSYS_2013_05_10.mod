# OSeMOSYS_2013_05_10_short
# 
# Open Source energy MOdeling SYStem
#
# Main changes to previous version OSeMOSYS_2013_05_10
#		- Significantly reduced the total number of equations by integrating them into the existing inequalities. This eliminates the need to calculate and store intermediate values. 
#		
#	The reduction in the number of equations translates into the generation of a smaller matrix to be solved. This significantly reduces the memory usage (~10x) 
#	and the processing time (~5x). This version of the OSeMOSYS code contains only the essential equations required for running the model. 
#	However, all the previous equations have been left as before, and "commented out" to better understand the methodology followed to shorten the code.
#	
#	It is important to note that the shortening of the code does not change any aspect of the functionality of OSeMOSYS. 
#	Furthermore, there are no special formatting requirements of data file required to run this version instead of the regular version. 
#	The short version of OSeMOSYS only serves to reduce the memory usage as well as the processing time for finding the model solution. 
#	In the future, both the regular and the short versions of OSeMOSYS will be developed and released simultaneously.
#
# ============================================================================
#
#    Copyright [2010-2013] [OSeMOSYS Forum steering committee see: www.osemosys.org]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ============================================================================
#
#  To run OSeMOSYS, enter the following line into your command prompt after replacing FILEPATH & YOURDATAFILE with your folder structure and data file name: 
#
#  C:\...FILEPATH...\glpsol -m C:\...FILEPATH...\OSeMOSYS_2013_05_10_short.mod -d C:\...FILEPATH...\YOURDATAFILE.dat -o C:\...FILEPATH...\Results.txt
#
#  Alternatively, install GUSEK (http://gusek.sourceforge.net/gusek.html) and run the model within this integrated development environment (IDE). 
#  To do so, open the .dat file and select "Use External .dat file" from the Options menu. Then change to the model file and select the "Go" icon or press F5.
#
#              			#########################################
######################			Model Definition				#############
#              			#########################################
#
###############
#    Sets     #
############### 
# 
set YEAR;
set TECHNOLOGY;
set TIMESLICE;
set FUEL;
set EMISSION;
set MODE_OF_OPERATION;
set REGION;
set SEASON;
set DAYTYPE;
set DAILYTIMEBRACKET;
set FLEXIBLEDEMANDTYPE; 
set STORAGE;
# Hydro Related Sets
set RESERVOIR;
#
#####################
#    Parameters     #
#####################
#	
########			Global 						#############
#
param YearSplit{l in TIMESLICE, y in YEAR};
param DiscountRate{r in REGION, t in TECHNOLOGY};
param DaySplit{lh in DAILYTIMEBRACKET, s in SEASON};
param Conversionls{l in TIMESLICE, ls in SEASON};
param Conversionld{l in TIMESLICE, ld in DAYTYPE};
param Conversionlh{l in TIMESLICE, lh in DAILYTIMEBRACKET};
param DaysInDayType{ls in SEASON, ld in DAYTYPE, y in YEAR};
param TradeRoute{r in REGION, rr in REGION, f in FUEL, y in YEAR};
param DepreciationMethod{r in REGION};
#
########			Demands 					#############
#
param SpecifiedAnnualDemand{r in REGION, f in FUEL, y in YEAR}; 
param SpecifiedDemandProfile{r in REGION, f in FUEL, l in TIMESLICE, y in YEAR};
param AccumulatedAnnualDemand{r in REGION, f in FUEL, y in YEAR};
#
#########			Performance					#############
#
param CapacityToActivityUnit{r in REGION, t in TECHNOLOGY};
param TechWithCapacityNeededToMeetPeakTS{r in REGION, t in TECHNOLOGY};
param CapacityFactor{r in REGION, t in TECHNOLOGY, l in TIMESLICE, y in YEAR};
param AvailabilityFactor{r in REGION, t in TECHNOLOGY, y in YEAR};
param OperationalLife{r in REGION, t in TECHNOLOGY};
param ResidualCapacity{r in REGION, t in TECHNOLOGY, y in YEAR};
param InputActivityRatio{r in REGION, t in TECHNOLOGY, f in FUEL, m in MODE_OF_OPERATION, y in YEAR};
param OutputActivityRatio{r in REGION, t in TECHNOLOGY, f in FUEL, m in MODE_OF_OPERATION, y in YEAR};
#
#########			Technology Costs			#############
#
param CapitalCost{r in REGION, t in TECHNOLOGY, y in YEAR};
param VariableCost{r in REGION, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR};
param FixedCost{r in REGION, t in TECHNOLOGY, y in YEAR};
#
#########           		Storage                 		#############
#
param TechnologyToStorage{r in REGION, t in TECHNOLOGY, s in STORAGE, m in MODE_OF_OPERATION};
param TechnologyFromStorage{r in REGION, t in TECHNOLOGY, s in STORAGE, m in MODE_OF_OPERATION};
param StorageLevelStart{r in REGION, s in STORAGE};
param StorageMaxChargeRate{r in REGION, s in STORAGE};
param StorageMaxDischargeRate{r in REGION, s in STORAGE};
param MinStorageCharge{r in REGION, s in STORAGE, y in YEAR};
param OperationalLifeStorage{r in REGION, s in STORAGE};
param CapitalCostStorage{r in REGION, s in STORAGE, y in YEAR};
param DiscountRateStorage{r in REGION, s in STORAGE};
param ResidualStorageCapacity{r in REGION, s in STORAGE, y in YEAR};
#
#########			Capacity Constraints		#############
#
param CapacityOfOneTechnologyUnit{r in REGION, t in TECHNOLOGY, y in YEAR};
param TotalAnnualMaxCapacity{r in REGION, t in TECHNOLOGY, y in YEAR};
param TotalAnnualMinCapacity{r in REGION, t in TECHNOLOGY, y in YEAR};
#
#########			Investment Constraints		#############
#
param TotalAnnualMaxCapacityInvestment{r in REGION, t in TECHNOLOGY, y in YEAR};
param TotalAnnualMinCapacityInvestment{r in REGION, t in TECHNOLOGY, y in YEAR};
#
#########			Activity Constraints		#############
#
param TotalTechnologyAnnualActivityUpperLimit{r in REGION, t in TECHNOLOGY, y in YEAR};
param TotalTechnologyAnnualActivityLowerLimit{r in REGION, t in TECHNOLOGY, y in YEAR};
param TotalTechnologyModelPeriodActivityUpperLimit{r in REGION, t in TECHNOLOGY};
param TotalTechnologyModelPeriodActivityLowerLimit{r in REGION, t in TECHNOLOGY};
#
#########			Reserve Margin				############# 
#
param ReserveMarginTagTechnology{r in REGION, t in TECHNOLOGY, y in YEAR}; 
param ReserveMarginTagFuel{r in REGION, f in FUEL, y in YEAR};
param ReserveMargin{r in REGION, y in YEAR};
param ReserveMarginMethod;
#
#########			RE Generation Target		############# 
#
param RETagTechnology{r in REGION, t in TECHNOLOGY, y in YEAR};
param RETagFuel{r in REGION, f in FUEL, y in YEAR}; 
param REMinProductionTarget{r in REGION, y in YEAR};
#
#########			Emissions & Penalties		#############
#
param EmissionActivityRatio{r in REGION, t in TECHNOLOGY, e in EMISSION, m in MODE_OF_OPERATION, y in YEAR};
param EmissionsPenalty{r in REGION, e in EMISSION, y in YEAR};
param AnnualExogenousEmission{r in REGION, e in EMISSION, y in YEAR};
param AnnualEmissionLimit{r in REGION, e in EMISSION, y in YEAR};
param ModelPeriodExogenousEmission{r in REGION, e in EMISSION};
param ModelPeriodEmissionLimit{r in REGION, e in EMISSION};
#########			Hydro System Specification 	############
#
param RhoWater;
param Gravity;
param FlowUnittoYearConversion;
param WattsToModelUnits;
param HydroTurbineEfficiency;
param TechnologyFromHydro{r in REGION, t in TECHNOLOGY, m in MODE_OF_OPERATION, v in RESERVOIR};
param ReservoirMaxDischargeRate{v in RESERVOIR};
param ReservoirMinDischargeRate{v in RESERVOIR};
param ReservoirHead{v in RESERVOIR};
param ReservoirExternalInflow{r in REGION, ls in SEASON, y in YEAR, v in RESERVOIR};
param ReservoirLevelStart{r in REGION, v in RESERVOIR};
param ReservoirLiveStorageVolume{v in RESERVOIR};
param DownstreamReservoirTag{v in RESERVOIR, vv in RESERVOIR};
#
#########			External Trade		#############
#
param MarketPrice{r in REGION, t in TECHNOLOGY, l in TIMESLICE, m in MODE_OF_OPERATION, y in YEAR};
param ExogenousProduction{r in REGION, f in FUEL, y in YEAR};

#########			Shared Technology		#############
#
param SharedTechnology{r in REGION, rr in REGION, t in TECHNOLOGY, y in YEAR};
#

#########			Ramping Requirements		#############
#
param ElectricityForTransmissionTag{r in REGION, f in FUEL};
param MaxOnlineCapReduction{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MaxGenerationReduction{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MaxPrimReserveDown{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MaxPrimReserveUp{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MaxSecReserveDown{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MaxSecReserveUp{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MinStableOperation{r in REGION, t in TECHNOLOGY, Y in YEAR};
param MinPrimReserveUpOnline{r in REGION, Y in YEAR};
param MinSecReserveUpOnline{r in REGION, Y in YEAR};
param PrimReserveDownCapacityDemand{r in REGION, l in TIMESLICE, y in YEAR};
param PrimReserveUpCapacityDemand{r in REGION, l in TIMESLICE, y in YEAR};
param SecReserveDownCapacityDemand{r in REGION, l in TIMESLICE, y in YEAR};
param SecReserveUpCapacityDemand{r in REGION, l in TIMESLICE, y in YEAR};
param TimeSliceLinkTag{r in REGION, l in TIMESLICE, ll in TIMESLICE};

######################
#   Model Variables  #
######################
#
########			Demands 					#############
#
#var RateOfDemand{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}>= 0;
#var Demand{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}>= 0;
#
########     		Storage                 		#############
#
var NewStorageCapacity{r in REGION, s in STORAGE, y in YEAR} >=0;
var SalvageValueStorage{r in REGION, s in STORAGE, y in YEAR} >=0;
var StorageLevelYearStart{r in REGION, s in STORAGE, y in YEAR} >=0;
var StorageLevelYearFinish{r in REGION, s in STORAGE, y in YEAR} >=0;
var StorageLevelSeasonStart{r in REGION, s in STORAGE, ls in SEASON, y in YEAR} >=0;
var StorageLevelDayTypeStart{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, y in YEAR} >=0;
var StorageLevelDayTypeFinish{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, y in YEAR} >=0;
#var RateOfStorageCharge{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR};
#var RateOfStorageDischarge{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR};
#var NetChargeWithinYear{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR};
#var NetChargeWithinDay{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR};
#var StorageLowerLimit{r in REGION, s in STORAGE, y in YEAR}>=0;
#var StorageUpperLimit{r in REGION, s in STORAGE, y in YEAR} >=0;
#var AccumulatedNewStorageCapacity{r in REGION, s in STORAGE, y in YEAR} >=0;
#var CapitalInvestmentStorage{r in REGION, s in STORAGE, y in YEAR} >=0;
#var DiscountedCapitalInvestmentStorage{r in REGION, s in STORAGE, y in YEAR} >=0;
#var DiscountedSalvageValueStorage{r in REGION, s in STORAGE, y in YEAR} >=0;
#var TotalDiscountedStorageCost{r in REGION, s in STORAGE, y in YEAR} >=0;
#
#########		    Capacity Variables 			############# 
#
var NumberOfNewTechnologyUnits{r in REGION, t in TECHNOLOGY, y in YEAR} >= 0,integer;
var NewCapacity{r in REGION, t in TECHNOLOGY, y in YEAR} >= 0;
#var AccumulatedNewCapacity{r in REGION, t in TECHNOLOGY, y in YEAR} >= 0;
#var TotalCapacityAnnual{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#
#########		    Activity Variables 			#############
#
var RateOfActivity{r in REGION, l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR} >= 0; 
var UseByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL, y in YEAR}>= 0;
var Trade{r in REGION, rr in REGION, l in TIMESLICE, f in FUEL, y in YEAR};
var UseAnnual{r in REGION, f in FUEL, y in YEAR}>= 0;
#var RateOfTotalActivity{r in REGION, t in TECHNOLOGY, l in TIMESLICE, y in YEAR} >= 0;
#var TotalTechnologyAnnualActivity{r in REGION, t in TECHNOLOGY, y in YEAR} >= 0;
#var TotalAnnualTechnologyActivityByMode{r in REGION, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR}>=0;
#var RateOfProductionByTechnologyByMode{r in REGION, l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION, f in FUEL, y in YEAR}>= 0;
#var RateOfProductionByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL, y in YEAR}>= 0;
#var ProductionByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL, y in YEAR}>= 0;
#var ProductionByTechnologyAnnual{r in REGION, t in TECHNOLOGY, f in FUEL, y in YEAR}>= 0;
#var RateOfProduction{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR} >= 0;
#var Production{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR} >= 0;
#var RateOfUseByTechnologyByMode{r in REGION, l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION, f in FUEL, y in YEAR}>= 0;
#var RateOfUseByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL, y in YEAR} >= 0;
#var UseByTechnologyAnnual{r in REGION, t in TECHNOLOGY, f in FUEL, y in YEAR}>= 0;
#var RateOfUse{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}>= 0;
#var Use{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}>= 0;
#var TradeAnnual{r in REGION, rr in REGION, f in FUEL, y in YEAR};
#var ProductionAnnual{r in REGION, f in FUEL, y in YEAR}>= 0;
#
#########		    Costing Variables 			#############
#
#var CapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
####var DiscountedCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#
var VariableOperatingCost{r in REGION, t in TECHNOLOGY, l in TIMESLICE, y in YEAR}>= 0;
var SalvageValue{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
var DiscountedSalvageValue{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
var OperatingCost{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#var DiscountedOperatingCost{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#var AnnualVariableOperatingCost{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#var AnnualFixedOperatingCost{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#var TotalDiscountedCostByTechnology{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#var TotalDiscountedCost{r in REGION, y in YEAR}>= 0;
#var ModelPeriodCostByRegion{r in REGION} >= 0;
#
#########			Reserve Margin				#############
#
#var TotalCapacityInReserveMargin{r in REGION, y in YEAR}>= 0;
#var DemandNeedingReserveMargin{r in REGION,l in TIMESLICE, y in YEAR}>= 0;
#
#########			RE Gen Target				#############
#
#var TotalREProductionAnnual{r in REGION, y in YEAR};
#var RETotalDemandOfTargetFuelAnnual{r in REGION, y in YEAR};
#
#var TotalTechnologyModelPeriodActivity{r in REGION, t in TECHNOLOGY};
#
#########			Emissions					#############
#
var DiscountedTechnologyEmissionsPenalty{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
var ModelPeriodEmissions{r in REGION, e in EMISSION}>= 0;
#var AnnualTechnologyEmissionByMode{r in REGION, t in TECHNOLOGY, e in EMISSION, m in MODE_OF_OPERATION, y in YEAR}>= 0;
#var AnnualTechnologyEmission{r in REGION, t in TECHNOLOGY, e in EMISSION, y in YEAR}>= 0;
#var AnnualTechnologyEmissionPenaltyByEmission{r in REGION, t in TECHNOLOGY, e in EMISSION, y in YEAR}>= 0;
#var AnnualTechnologyEmissionsPenalty{r in REGION, t in TECHNOLOGY, y in YEAR}>= 0;
#var AnnualEmissions{r in REGION, e in EMISSION, y in YEAR}>= 0;
#
#	table data IN "CSV" "data.csv": s <- [FROM,TO], d~DISTANCE, c~COST;
#	table capacity IN "CSV" "SpecifiedAnnualDemand.csv": [YEAR, FUEL, REGION], SpecifiedAnnualDemand~ColumnNameInCSVSheet;
#
################## Hydro System Variables   ###############
#
var RateOfReservoirDischarge{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET ,r in REGION} >= 0;
var RateOfReservoirSpillage{y in YEAR, l in TIMESLICE, v in RESERVOIR, r in REGION} >= 0;
var RateOfReservoirSpillageExpanded{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET ,r in REGION} >= 0;
var RateOfExternalReservoirFilling{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET ,r in REGION} >= 0;
var FlowBetweenReservoirs{v in RESERVOIR, vv in RESERVOIR, y in YEAR, ls in SEASON,ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION};
var RateOfReservoirFilling{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET ,r in REGION} >= 0;
var RateOfReservoirEmptying{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET ,r in REGION} >= 0;
var NetReservoirWithinYear{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET ,r in REGION};
var NetReservoirWithinDay{v in RESERVOIR,y in YEAR,ls in SEASON,ld in DAYTYPE,lh in DAILYTIMEBRACKET,r in REGION};
var ReservoirLevelYearStart{v in RESERVOIR,y in YEAR,r in REGION} >= 0;
var ReservoirLevelYearFinish{v in RESERVOIR,y in YEAR,r in REGION} >= 0;
var ReservoirLevelSeasonStart{v in RESERVOIR,y in YEAR,ls in SEASON,r in REGION} >= 0;
var ReservoirLevelDayTypeStart{v in RESERVOIR,y in YEAR,ls in SEASON,ld in DAYTYPE,r in REGION} >= 0;
var ReservoirLevelDayTypeFinish{v in RESERVOIR,y in YEAR,ls in SEASON,ld in DAYTYPE,r in REGION} >= 0;
#
#########			Ramping					#############
#
var PrimReserveDownByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR} >= 0;
var SecReserveDownByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR} >= 0;
var SecReserveUpOnline{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR} >=0;
var PrimReserveUpOnline{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR} >=0;
var OnlineCapacity{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR};

#
######################
# Objective Function #
######################
#
minimize cost: sum{r in REGION, t in TECHNOLOGY, y in YEAR} (((((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*(VariableCost[r,t,m,y]+MarketPrice[r,t,l,m,y]))/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))+CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)))+DiscountedTechnologyEmissionsPenalty[r,t,y]-DiscountedSalvageValue[r,t,y]) + sum{s in STORAGE} (CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))-CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))));
#
#####################
# Constraints       #
#####################
#
#s.t. EQ_SpecifiedDemand{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: SpecifiedAnnualDemand[r,f,y]*SpecifiedDemandProfile[r,f,l,y] / YearSplit[l,y]=RateOfDemand[r,l,f,y];
#
#########       	Capacity Adequacy A	     	#############
#
s.t. CAa4_Constraint_Capacity{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: TechWithCapacityNeededToMeetPeakTS[r,t]<>0}: sum{m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y] <= ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*CapacityFactor[r,t,l,y]*CapacityToActivityUnit[r,t];
s.t. CAa5_TotalNewCapacity{r in REGION, t in TECHNOLOGY, y in YEAR: CapacityOfOneTechnologyUnit[r,t,y]<>0}: CapacityOfOneTechnologyUnit[r,t,y]*NumberOfNewTechnologyUnits[r,t,y] = NewCapacity[r,t,y];
#
# Note that the PlannedMaintenance equation below ensures that all other technologies have a capacity great enough to at least meet the annual average.
#
#########       	Capacity Adequacy B		 	#############
#
s.t. CAb1_PlannedMaintenance{r in REGION, t in TECHNOLOGY, y in YEAR}: sum{l in TIMESLICE} sum{m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y]*YearSplit[l,y] <= sum{l in TIMESLICE} (((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*CapacityFactor[r,t,l,y]*YearSplit[l,y])* AvailabilityFactor[r,t,y]*CapacityToActivityUnit[r,t];
#
#########	        Energy Balance A    	 	#############
#
s.t. EBa10_EnergyBalanceEachTS4{r in REGION, rr in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: Trade[r,rr,l,f,y] = -Trade[rr,r,l,f,y];
s.t. EBa11_EnergyBalanceEachTS5{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: sum{m in MODE_OF_OPERATION, t in TECHNOLOGY: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]*YearSplit[l,y] + ExogenousProduction[r,f,y]*YearSplit[l,y] >= SpecifiedAnnualDemand[r,f,y]*SpecifiedDemandProfile[r,f,l,y] + sum{m in MODE_OF_OPERATION, t in TECHNOLOGY: InputActivityRatio[r,t,f,m,y]<>0} RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y]*YearSplit[l,y] + sum{rr in REGION} Trade[r,rr,l,f,y]*TradeRoute[r,rr,f,y];
#
#########        	Shared Technology		 	#############
#
s.t. LTa1_SharedTechnology{r in REGION, rr in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: SharedTechnology[r,rr,t,y] = 1}: ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) = ((sum{yy in YEAR: y-yy < OperationalLife[rr,t] && y-yy>=0} NewCapacity[rr,t,yy])+ ResidualCapacity[rr,t,y]);
#
#########        	Energy Balance B		 	#############
#
s.t. EBb4_EnergyBalanceEachYear4{r in REGION, f in FUEL, y in YEAR}: sum{m in MODE_OF_OPERATION, t in TECHNOLOGY, l in TIMESLICE: OutputActivityRatio[r,t,f,m,y] <>0} (RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]*YearSplit[l,y]) + ExogenousProduction[r,f,y] >= sum{m in MODE_OF_OPERATION, t in TECHNOLOGY, l in TIMESLICE: InputActivityRatio[r,t,f,m,y]<>0} RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y]*YearSplit[l,y] + sum{l in TIMESLICE, rr in REGION} Trade[r,rr,l,f,y]*TradeRoute[r,rr,f,y] + AccumulatedAnnualDemand[r,f,y];
#
#########        	Storage Equations			#############
#
s.t. S5_and_S6_StorageLevelYearStart{r in REGION, s in STORAGE, y in YEAR}: if y = min{yy in YEAR} min(yy) then StorageLevelStart[r,s] 
																	else StorageLevelYearStart[r,s,y-1] + sum{ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET} sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0}  (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION:TechnologyToStorage[r,t,s,m]>0} (RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * YearSplit[l,y] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]
																	= StorageLevelYearStart[r,s,y];
s.t. S7_and_S8_StorageLevelYearFinish{r in REGION, s in STORAGE, y in YEAR}: if y < max{yy in YEAR} max(yy) then StorageLevelYearStart[r,s,y+1]
																	else StorageLevelYearStart[r,s,y] + sum{ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET} sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0}  (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION:TechnologyToStorage[r,t,s,m]>0} (RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * YearSplit[l,y] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] 
																	= StorageLevelYearFinish[r,s,y];	
s.t. S9_and_S10_StorageLevelSeasonStart{r in REGION, s in STORAGE, ls in SEASON, y in YEAR}: if ls = min{lsls in SEASON} min(lsls) then StorageLevelYearStart[r,s,y] 
																	else StorageLevelSeasonStart[r,s,ls-1,y] + sum{ld in DAYTYPE, lh in DAILYTIMEBRACKET} sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0}  (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION:TechnologyToStorage[r,t,s,m]>0} (RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * YearSplit[l,y] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] 
																	= StorageLevelSeasonStart[r,s,ls,y];
s.t. S11_and_S12_StorageLevelDayTypeStart{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, y in YEAR}: if ld = min{ldld in DAYTYPE} min(ldld) then StorageLevelSeasonStart[r,s,ls,y] 
																	else StorageLevelDayTypeStart[r,s,ls,ld-1,y] + sum{lh in DAILYTIMEBRACKET} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]) * DaysInDayType[ls,ld-1,y]
																	= StorageLevelDayTypeStart[r,s,ls,ld,y];
s.t. S13_and_S14_and_S15_StorageLevelDayTypeFinish{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, y in YEAR}:	if ls = max{lsls in SEASON} max(lsls) && ld = max{ldld in DAYTYPE} max(ldld) then StorageLevelYearFinish[r,s,y] 
																	else if ld = max{ldld in DAYTYPE} max(ldld) then StorageLevelSeasonStart[r,s,ls+1,y]
																	else StorageLevelDayTypeFinish[r,s,ls,ld+1,y] - sum{lh in DAILYTIMEBRACKET} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]) * DaysInDayType[ls,ld+1,y]
																	= StorageLevelDayTypeFinish[r,s,ls,ld,y];	
#
##########		Storage Constraints				#############
#																	
s.t. SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 0 <= (StorageLevelDayTypeStart[r,s,ls,ld,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-MinStorageCharge[r,s,y]*(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]);								
s.t. SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: (StorageLevelDayTypeStart[r,s,ls,ld,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]) <= 0;								
s.t. SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 0 <= if ld > min{ldld in DAYTYPE} min(ldld) then (StorageLevelDayTypeStart[r,s,ls,ld,y]-sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-MinStorageCharge[r,s,y]*(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]);																										
s.t. SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: if ld > min{ldld in DAYTYPE} min(ldld) then (StorageLevelDayTypeStart[r,s,ls,ld+1,y]-sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]) <= 0;					
s.t. SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}:  0 <= (StorageLevelDayTypeFinish[r,s,ls,ld,y] - sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-MinStorageCharge[r,s,y]*(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]);																										
s.t. SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}:  (StorageLevelDayTypeFinish[r,s,ls,ld,y] - sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]) <= 0;
s.t. SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 	0 <= if ld > min{ldld in DAYTYPE} min(ldld) then (StorageLevelDayTypeFinish[r,s,ls,ld-1,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-MinStorageCharge[r,s,y]*(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]);
s.t. SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: if ld > min{ldld in DAYTYPE} min(ldld) then (StorageLevelDayTypeFinish[r,s,ls,ld-1,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} (((sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]) - (sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh])) * DaySplit[lh,ls]))-(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]) <= 0;										
s.t. SC5_MaxChargeConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyToStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] <= StorageMaxChargeRate[r,s];
s.t. SC6_MaxDischargeConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromStorage[r,t,s,m] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] <= StorageMaxDischargeRate[r,s];
#
#########		Storage Investments				#############
#
s.t. SI6_SalvageValueStorageAtEndOfPeriod1{r in REGION, s in STORAGE, y in YEAR: (y+OperationalLifeStorage[r,s]-1) <= (max{yy in YEAR} max(yy))}: 0 = SalvageValueStorage[r,s,y];
#s.t. SI7_SalvageValueStorageAtEndOfPeriod2{r in REGION, s in STORAGE, y in YEAR: (DepreciationMethod[r]=1 && (y+OperationalLifeStorage[r,s]-1) > (max{yy in YEAR} max(yy)) && DiscountRateStorage[r,s]=0) || (DepreciationMethod[r]=2 && (y+OperationalLifeStorage[r,s]-1) > (max{yy in YEAR} max(yy)))}: CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]*(1-(max{yy in YEAR} max(yy) - y+1)/OperationalLifeStorage[r,s]) = SalvageValueStorage[r,s,y];
#s.t. SI8_SalvageValueStorageAtEndOfPeriod3{r in REGION, s in STORAGE, y in YEAR: DepreciationMethod[r]=1 && (y+OperationalLifeStorage[r,s]-1) > (max{yy in YEAR} max(yy)) && DiscountRateStorage[r,s]>0}: CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]*(1-(((1+DiscountRateStorage[r,s])^(max{yy in YEAR} max(yy) - y+1)-1)/((1+DiscountRateStorage[r,s])^OperationalLifeStorage[r,s]-1))) = SalvageValueStorage[r,s,y];
#s.t. SI1_StorageUpperLimit{r in REGION, s in STORAGE, y in YEAR}: sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y] = StorageUpperLimit[r,s,y];
#s.t. SI2_StorageLowerLimit{r in REGION, s in STORAGE, y in YEAR}: MinStorageCharge[r,s,y]*(sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]+ResidualStorageCapacity[r,s,y]) = StorageLowerLimit[r,s,y];
#s.t. SI3_TotalNewStorage{r in REGION, s in STORAGE, y in YEAR}: sum{yy in YEAR: y-yy < OperationalLifeStorage[r,s] && y-yy>=0} NewStorageCapacity[r,s,yy]=AccumulatedNewStorageCapacity[r,s,y];
#s.t. SI4_UndiscountedCapitalInvestmentStorage{r in REGION, s in STORAGE, y in YEAR}: CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y] = CapitalInvestmentStorage[r,s,y];
#s.t. SI5_DiscountingCapitalInvestmentStorage{r in REGION, s in STORAGE, y in YEAR}: CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy))) = DiscountedCapitalInvestmentStorage[r,s,y];
#s.t. SI9_SalvageValueStorageDiscountedToStartYear{r in REGION, s in STORAGE, y in YEAR}: SalvageValueStorage[r,s,y]/((1+DiscountRateStorage[r,s])^(max{yy in YEAR} max(yy)-min{yy in YEAR} min(yy)+1)) = DiscountedSalvageValueStorage[r,s,y];
#s.t. SI10_TotalDiscountedCostByStorage{r in REGION, s in STORAGE, y in YEAR}: (CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))-CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))) = TotalDiscountedStorageCost[r,s,y];
#
#########       	Capital Costs 		     	#############
#
#s.t. CC1_UndiscountedCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}: CapitalCost[r,t,y] * NewCapacity[r,t,y] = CapitalInvestment[r,t,y];
####s.t. CC2_DiscountingCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}: CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy))) = DiscountedCapitalInvestment[r,t,y];
#
#########           Salvage Value            	#############
#
s.t. SV1_SalvageValueAtEndOfPeriod1{r in REGION, t in TECHNOLOGY, y in YEAR: (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)) && DiscountRate[r,t]>0}: SalvageValue[r,t,y] = CapitalCost[r,t,y]*NewCapacity[r,t,y]*(1-(((1+DiscountRate[r,t])^(max{yy in YEAR} max(yy) - y+1)-1)/((1+DiscountRate[r,t])^OperationalLife[r,t]-1)));
s.t. SV2_SalvageValueAtEndOfPeriod2{r in REGION, t in TECHNOLOGY, y in YEAR: (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)) && DiscountRate[r,t]=0}: SalvageValue[r,t,y] = CapitalCost[r,t,y]*NewCapacity[r,t,y]*(1-(max{yy in YEAR} max(yy) - y+1)/OperationalLife[r,t]);
s.t. SV3_SalvageValueAtEndOfPeriod3{r in REGION, t in TECHNOLOGY, y in YEAR: (y + OperationalLife[r,t]-1) <= (max{yy in YEAR} max(yy))}: SalvageValue[r,t,y] = 0;
s.t. SV4_SalvageValueDiscountedToStartYear{r in REGION, t in TECHNOLOGY, y in YEAR}: DiscountedSalvageValue[r,t,y] = SalvageValue[r,t,y]/((1+DiscountRate[r,t])^(1+max{yy in YEAR} max(yy)-min{yy in YEAR} min(yy)));
#
#########        	Operating Costs 		 	#############
#
####s.t. OC4_DiscountedOperatingCostsTotalAnnual{r in REGION, t in TECHNOLOGY, y in YEAR}: (((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*VariableCost[r,t,m,y])/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5)) = DiscountedOperatingCost[r,t,y];
#
#########       	Total Discounted Costs	 	#############
#
#s.t. TDC1_TotalDiscountedCostByTechnology{r in REGION, t in TECHNOLOGY, y in YEAR}: ((((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*VariableCost[r,t,m,y])/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))+CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)))+DiscountedTechnologyEmissionsPenalty[r,t,y]-DiscountedSalvageValue[r,t,y]) = TotalDiscountedCostByTechnology[r,t,y];
####s.t. TDC2_TotalDiscountedCost{r in REGION, y in YEAR}: sum{t in TECHNOLOGY}((((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*VariableCost[r,t,m,y])/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))+CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)))+DiscountedTechnologyEmissionsPenalty[r,t,y]-DiscountedSalvageValue[r,t,y]) + sum{s in STORAGE} (CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))-CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))) = TotalDiscountedCost[r,y];
#
#########      		Total Capacity Constraints 	##############
#
s.t. TCC1_TotalAnnualMaxCapacityConstraint{r in REGION, t in TECHNOLOGY, y in YEAR}: ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) <= TotalAnnualMaxCapacity[r,t,y];
s.t. TCC2_TotalAnnualMinCapacityConstraint{r in REGION, t in TECHNOLOGY, y in YEAR: TotalAnnualMinCapacity[r,t,y]>0}: ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) >= TotalAnnualMinCapacity[r,t,y];
#
#########    		New Capacity Constraints  	##############
#
s.t. NCC1_TotalAnnualMaxNewCapacityConstraint{r in REGION, t in TECHNOLOGY, y in YEAR}: NewCapacity[r,t,y] <= TotalAnnualMaxCapacityInvestment[r,t,y];
s.t. NCC2_TotalAnnualMinNewCapacityConstraint{r in REGION, t in TECHNOLOGY, y in YEAR: TotalAnnualMinCapacityInvestment[r,t,y]>0}: NewCapacity[r,t,y] >= TotalAnnualMinCapacityInvestment[r,t,y];
#
#########   		Annual Activity Constraints	##############
#
s.t. AAC2_TotalAnnualTechnologyActivityUpperLimit{r in REGION, t in TECHNOLOGY, y in YEAR}: sum{l in TIMESLICE, m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y]*YearSplit[l,y] <= TotalTechnologyAnnualActivityUpperLimit[r,t,y] ;
s.t. AAC3_TotalAnnualTechnologyActivityLowerLimit{r in REGION, t in TECHNOLOGY, y in YEAR: TotalTechnologyAnnualActivityLowerLimit[r,t,y]>0}: sum{l in TIMESLICE, m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y]*YearSplit[l,y] >= TotalTechnologyAnnualActivityLowerLimit[r,t,y] ;
#
#########    		Total Activity Constraints 	##############
#
s.t. TAC2_TotalModelHorizonTechnologyActivityUpperLimit{r in REGION, t in TECHNOLOGY}: sum{l in TIMESLICE, m in MODE_OF_OPERATION, y in YEAR} RateOfActivity[r,l,t,m,y]*YearSplit[l,y] <= TotalTechnologyModelPeriodActivityUpperLimit[r,t] ;
s.t. TAC3_TotalModelHorizenTechnologyActivityLowerLimit{r in REGION, t in TECHNOLOGY: TotalTechnologyModelPeriodActivityLowerLimit[r,t]>0}: sum{l in TIMESLICE, m in MODE_OF_OPERATION, y in YEAR} RateOfActivity[r,l,t,m,y]*YearSplit[l,y] >= TotalTechnologyModelPeriodActivityLowerLimit[r,t] ;
#
#########   		Reserve Margin Constraint	############## NTS: Should change demand for production
#
s.t. RM3a_ReserveMargin_Constraint{r in REGION, l in TIMESLICE, y in YEAR: ReserveMarginMethod = 1}: sum{m in MODE_OF_OPERATION, t in TECHNOLOGY, f in FUEL: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] * ReserveMarginTagFuel[r,f,y] * ReserveMargin[r,y]<= sum {t in TECHNOLOGY} ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) * ReserveMarginTagTechnology[r,t,y] * CapacityToActivityUnit[r,t];
s.t. RM3b_ReserveMargin_Constraints{r in REGION, l in TIMESLICE, y in YEAR: ReserveMarginMethod = 2}: sum{m in MODE_OF_OPERATION, t in TECHNOLOGY, f in FUEL} SpecifiedAnnualDemand[r,f,y] * SpecifiedDemandProfile[r,f,l,y] * ReserveMarginTagFuel[r,f,y] * ReserveMargin[r,y]<= sum {t in TECHNOLOGY} ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) * ReserveMarginTagTechnology[r,t,y] * CapacityToActivityUnit[r,t];
#
#########   		RE Production Target		############## NTS: Should change demand for production
#
s.t. RE4_EnergyConstraint{r in REGION, y in YEAR}:REMinProductionTarget[r,y]*sum{l in TIMESLICE, f in FUEL} SpecifiedAnnualDemand[r,f,y]*SpecifiedDemandProfile[r,f,l,y]*RETagFuel[r,f,y] <= sum{m in MODE_OF_OPERATION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] * YearSplit[l,y]*RETagTechnology[r,t,y];
#
#########   		Emissions Accounting		##############
#
s.t. E5_DiscountedEmissionsPenaltyByTechnology{r in REGION, t in TECHNOLOGY, y in YEAR}: sum{e in EMISSION, l in TIMESLICE, m in MODE_OF_OPERATION: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*EmissionsPenalty[r,e,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5)) = DiscountedTechnologyEmissionsPenalty[r,t,y];
s.t. E8_AnnualEmissionsLimit{r in REGION, e in EMISSION, y in YEAR}: sum{l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y]+AnnualExogenousEmission[r,e,y] <= AnnualEmissionLimit[r,e,y];
s.t. E9_ModelPeriodEmissionsLimit{r in REGION, e in EMISSION}:  sum{l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y] + ModelPeriodExogenousEmission[r,e] <= ModelPeriodEmissionLimit[r,e] ;
#
#
#########        	Hydro Facility Equations			#############
#

s.t. Hy1_RateOfReservoirDischarge{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromHydro[r,t,m,v]>0} RateOfActivity[r,l,t,m,y] * TechnologyFromHydro[r,t,m,v] * Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] / RhoWater / Gravity / HydroTurbineEfficiency / ReservoirHead[v] / WattsToModelUnits / CapacityToActivityUnit[r, t] = RateOfReservoirDischarge[v,y,ls,ld,lh,r];
	# * 8.76 converts between W and Wh (with m^3 to L conversion also taken into account).
	# THIS HAS BEEN CONFIRMED WITH THE OUTPUT.  NEED TO FORMALIZE THIS INTO THE MODEL LOGICALLY.

#Rate of Activity:  If we ran for a full year at this rate, we would produce this much power.  i.e. GWh/annum
# Watts vs. Wh/a.

s.t. Hy2a_RateOfExternalReservoirFilling{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: 
	sum{l in TIMESLICE} ReservoirExternalInflow[r, ls ,y, v] *Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh]
	= RateOfExternalReservoirFilling[v,y,ls,ld,lh,r];

s.t. Hy2b_FlowBetweenReservoirs{v in RESERVOIR, vv in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}:  FlowBetweenReservoirs[v,vv,y,ls,ld,lh,r] = -FlowBetweenReservoirs[vv,v,y,ls,ld,lh,r];

s.t. Hy2v_RateOfReservoirFilling{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: RateOfReservoirFilling[v,y,ls,ld,lh,r] = RateOfExternalReservoirFilling[v,y,ls,ld,lh,r] + sum{vv in RESERVOIR} FlowBetweenReservoirs[v,vv,y,ls,ld,lh,r]*DownstreamReservoirTag[v,vv];

s.t. Hy2d_RateOfReservoirEmptying{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: RateOfReservoirEmptying[v,y,ls,ld,lh,r] = RateOfReservoirDischarge[v,y,ls,ld,lh,r] + RateOfReservoirSpillageExpanded[v,y,ls,ld,lh,r];

s.t. Hy2d2_Spillage{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0} RateOfReservoirSpillage[y, l, v, r] *Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] = RateOfReservoirSpillageExpanded[v,y,ls,ld,lh,r];

s.t. Hy2e_EmptyingFlowCriteria{v in RESERVOIR, vv in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}:
	if DownstreamReservoirTag[vv,v] = 1 then FlowBetweenReservoirs[vv,v,y,ls,ld,lh,r]*DownstreamReservoirTag[vv,v]
	else RateOfReservoirEmptying[v,y,ls,ld,lh,r]
	= RateOfReservoirEmptying[v,y,ls,ld,lh,r];

s.t. Hy3_NetReservoirWithinYear{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0}  (RateOfReservoirFilling[v,y,ls,ld,lh,r] - RateOfReservoirEmptying[v,y,ls,ld,lh,r]) * FlowUnittoYearConversion * YearSplit[l,y] *Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] = NetReservoirWithinYear[v,y,ls,ld,lh,r];

s.t. Hy4_NetReservoirWithinDay{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: (RateOfReservoirFilling[v,y,ls,ld,lh,r] - RateOfReservoirEmptying[v,y,ls,ld,lh,r]) * FlowUnittoYearConversion * DaySplit[lh,ls] = NetReservoirWithinDay[v,y,ls,ld,lh,r];


# Discharge, Ext Filling, Spillage are all in units of m^3/s
# Net Reservoir/Year is in units of m^3
# 


s.t. Hy5_and_Hy6_ReservoirLevelYearStart{v in RESERVOIR, y in YEAR, r in REGION}: if y = min{yy in YEAR} min(yy) then ReservoirLevelStart[r,v] 
	else ReservoirLevelYearStart[v,y-1,r] + sum{ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET} NetReservoirWithinYear[v,y-1,ls,ld,lh,r]
	= ReservoirLevelYearStart[v,y,r];

s.t. Hy7_and_Hy8_ReservoirLevelYearFinish{v in RESERVOIR, y in YEAR, r in REGION}:  if y < max{yy in YEAR} max(yy) then ReservoirLevelYearStart[v,y+1,r]
	else ReservoirLevelYearStart[v,y,r] + sum{ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET} NetReservoirWithinYear[v,y,ls,ld,lh,r] 
	= ReservoirLevelYearFinish[v,y,r];

s.t. Hy9_and_Hy10_ReservoirLevelSeasonStart{v in RESERVOIR, y in YEAR, ls in SEASON, r in REGION}: if ls = min{lsls in SEASON} min(lsls) then ReservoirLevelYearStart[v,y,r] 
	else ReservoirLevelSeasonStart[v,y,ls-1,r] + sum{ld in DAYTYPE, lh in DAILYTIMEBRACKET} NetReservoirWithinYear[v,y,ls-1,ld,lh,r] 
	= ReservoirLevelSeasonStart[v,y,ls,r];

s.t. Hy11_and_Hy12_ReservoirLevelDayTypeStart{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, r in REGION}: if ld = min{ldld in DAYTYPE} min(ldld) then ReservoirLevelSeasonStart[v,y,ls,r] 
	else ReservoirLevelDayTypeStart[v,y,ls,ld-1,r] + sum{lh in DAILYTIMEBRACKET} NetReservoirWithinDay[v,y,ls,ld-1,lh,r] * DaysInDayType[ls,ld-1,y]
	= ReservoirLevelDayTypeStart[v,y,ls,ld,r];

s.t. Hy13_and_Hy14_and_Hy15_ReservoirLevelDayTypeFinish{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, r in REGION}:	if ls = max{lsls in SEASON} max(lsls) && ld = max{ldld in DAYTYPE} max(ldld) then ReservoirLevelYearFinish[v,y,r] 
	else if ld = max{ldld in DAYTYPE} max(ldld) then ReservoirLevelSeasonStart[v,y,ls+1,r]
	else ReservoirLevelDayTypeFinish[v,y,ls,ld+1,r] - sum{lh in DAILYTIMEBRACKET} NetReservoirWithinDay[v,y,ls,ld+1,lh,r] * DaysInDayType[ls,ld+1,y]
	= ReservoirLevelDayTypeFinish[v,y,ls,ld,r];


#########		Hydro Facility Constraints		#############


s.t. HyC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: 0 <= (ReservoirLevelDayTypeStart[v,y,ls,ld,r]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetReservoirWithinDay[v,y,ls,ld,lhlh,r]);

s.t. HyC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: (ReservoirLevelDayTypeStart[v,y,ls,ld,r]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetReservoirWithinDay[v,y,ls,ld,lhlh,r])-ReservoirLiveStorageVolume[v] <= 0;

s.t. HyC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: 0 <= if ld > min{ldld in DAYTYPE} min(ldld) then (ReservoirLevelDayTypeStart[v,y,ls,ld,r]-sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} NetReservoirWithinDay[v,y,ls,ld-1,lhlh,r]);


s.t. HyC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: if ld > min{ldld in DAYTYPE} min(ldld) then (ReservoirLevelDayTypeStart[v,y,ls,ld,r]-sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} NetReservoirWithinDay[v,y,ls,ld-1,lhlh,r])-ReservoirLiveStorageVolume[v] <= 0;

s.t. HyC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}:  0 <= (ReservoirLevelDayTypeFinish[v,y,ls,ld,r] - sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} NetReservoirWithinDay[v,y,ls,ld,lhlh,r]);

s.t. HyC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}:  (ReservoirLevelDayTypeFinish[v,y,ls,ld,r] - sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} NetReservoirWithinDay[v,y,ls,ld,lhlh,r])-ReservoirLiveStorageVolume[v] <= 0;

s.t. HyC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: 	0 <= if ld > min{ldld in DAYTYPE} min(ldld) then (ReservoirLevelDayTypeFinish[v,y,ls,ld-1,r]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetReservoirWithinDay[v,y,ls,ld,lhlh,r]);

s.t. HyC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: if ld > min{ldld in DAYTYPE} min(ldld) then (ReservoirLevelDayTypeFinish[v,y,ls,ld-1,r]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetReservoirWithinDay[v,y,ls,ld,lhlh,r])-ReservoirLiveStorageVolume[v] <= 0;

# # Reservoir Discharge Requirements (fisheries, etc.)
s.t. HyC5_MaxReservoirEmptyingConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0} RateOfReservoirEmptying[v,y,ls,ld,lh,r] *Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] <= ReservoirMaxDischargeRate[v];

s.t. HyC6_MinReservoirEmptyingConstraint{v in RESERVOIR, y in YEAR, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, r in REGION}: sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0} ReservoirMinDischargeRate[v] *Conversionls[l,ls] * Conversionld[l,ld] * Conversionlh[l,lh] <= RateOfReservoirEmptying[v,y,ls,ld,lh,r];

#
#########   		Ramping		##############
#
#Reserve requirements
#
s.t. R1_PrimReserveUp{r in REGION, f in FUEL, l in TIMESLICE, y in YEAR: f="PrimReserveUp"}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] >= PrimReserveUpCapacityDemand[r,l,y] + sum{t in TECHNOLOGY, m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t]; 
s.t. R2_SecReserveUp{r in REGION, f in FUEL, l in TIMESLICE, y in YEAR: f="SecReserveUp"}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] >= SecReserveUpCapacityDemand[r,l,y] + sum{t in TECHNOLOGY, m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t]; 
s.t. R3_PrimReserveDown{r in REGION, f in FUEL, l in TIMESLICE, y in YEAR}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION} PrimReserveDownByTechnology[r,l,t,y]/CapacityToActivityUnit[r,t] >= PrimReserveDownCapacityDemand[r,l,y]; 
s.t. R4_SecReserveDown{r in REGION, f in FUEL, l in TIMESLICE, y in YEAR}: sum{t in TECHNOLOGY, m in MODE_OF_OPERATION} SecReserveDownByTechnology[r,l,t,y]/CapacityToActivityUnit[r,t] >= SecReserveDownCapacityDemand[r,l,y]; 
#
#Ramping characteristics
#
s.t. R5_MaxOnlineCapacity{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR}: OnlineCapacity[r,l,t,y] <= ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]);
s.t. R6_MaxPrimCapacityDown{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR}: PrimReserveDownByTechnology[r,l,t,y] <= OnlineCapacity[r,l,t,y]*MaxPrimReserveDown[r,t,y]*CapacityToActivityUnit[r,t];
s.t. R7_MaxSecCapacityDown{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR}: SecReserveDownByTechnology[r,l,t,y] <= OnlineCapacity[r,l,t,y]*MaxPrimReserveDown[r,t,y]*CapacityToActivityUnit[r,t];
s.t. R8_MaxPrimCapacityUp{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "PrimReserveUp" && MaxPrimReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxPrimReserveUp[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y]}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] <= ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*CapacityFactor[r,t,l,y]*MaxPrimReserveUp[r,t,y]*CapacityToActivityUnit[r,t];
s.t. R9_MaxSecCapacityUp{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "SecReserveUp" && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y]}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] <= ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) * CapacityFactor[r,t,l,y] * MaxPrimReserveUp[r,t,y] * CapacityToActivityUnit[r,t];
s.t. R10_MinElecGeneration1{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y] && (MaxPrimReserveDown[r,t,y]>0 || MaxPrimReserveUp[r,t,y]>0 || MaxSecReserveDown[r,t,y]>0 || MaxSecReserveUp[r,t,y]>0)}: PrimReserveDownByTechnology[r,l,t,y] + SecReserveDownByTechnology[r,l,t,y] <= sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y];
s.t. R11_MinOnlineCapacity{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && MaxPrimReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxPrimReserveUp[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y]}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] <= OnlineCapacity[r,l,t,y]*CapacityToActivityUnit[r,t];
s.t. R12_MinElecGeneration2{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y]}: OnlineCapacity[r,l,t,y]*MinStableOperation[r,t,y]*CapacityToActivityUnit[r,t] <= sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y];
s.t. R13_MaxPrimCapacityUp{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "PrimReserveUp" && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y])}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] <= OnlineCapacity[r,l,t,y]*MaxPrimReserveUp[r,t,y]*CapacityToActivityUnit[r,t];
s.t. R14_MaxSecCapacityUp{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "SecReserveUp" && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y]) && (MaxSecReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxSecReserveUp[r,t,y] < MinStableOperation[r,t,y])}:sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] <= OnlineCapacity[r,l,t,y]*MaxSecReserveUp[r,t,y]*CapacityToActivityUnit[r,t];
s.t. R15_MinElecGeneration{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y]) && (MaxSecReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxSecReserveUp[r,t,y] < MinStableOperation[r,t,y]) && (MaxPrimReserveDown[r,t,y]>0 || MaxPrimReserveUp[r,t,y]>0 || MaxSecReserveDown[r,t,y]>0 || MaxSecReserveUp[r,t,y]>0)}: OnlineCapacity[r,l,t,y]*MinStableOperation[r,t,y]*CapacityToActivityUnit[r,t] + PrimReserveDownByTechnology[r,l,t,y] + SecReserveDownByTechnology[r,l,t,y] <= sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y];
s.t. R16_MinOnlineCapacity{r in REGION, f in FUEL, ff in FUEL, fff in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ff = "PrimReserveUp" && fff = "SecReserveUp" && ElectricityForTransmissionTag[r,f]=1 && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y]) && (MaxSecReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxSecReserveUp[r,t,y] < MinStableOperation[r,t,y])}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] + sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,ff,m,y] + sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,fff,m,y] <= OnlineCapacity[r,l,t,y]*CapacityToActivityUnit[r,t];
s.t. R17_MinOnlineCapacity{r in REGION, f in FUEL, ff in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ff = "PrimReserveUp" && ElectricityForTransmissionTag[r,f]=1 && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y]) && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y] && (MaxPrimReserveDown[r,t,y]>0 || MaxSecReserveDown[r,t,y]>0 || MaxPrimReserveUp[r,t,y]>0 || MaxSecReserveUp[r,t,y]>0)}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] + sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,ff,m,y] <= OnlineCapacity[r,l,t,y]*CapacityToActivityUnit[r,t];
s.t. R18_MinElecGeneration{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y]) && MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y] && MaxPrimReserveDown[r,t,y] > 0}:PrimReserveDownByTechnology[r,l,t,y]*(MinStableOperation[r,t,y] + MaxPrimReserveDown[r,t,y])/MaxPrimReserveDown[r,t,y] + SecReserveDownByTechnology[r,l,t,y] <= sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y];
s.t. R19_MinPrimReserveUpOnline{r in REGION, l in TIMESLICE, y in YEAR}: PrimReserveUpCapacityDemand[r,l,y]*MinPrimReserveUpOnline[r,y] <= sum{t in TECHNOLOGY} PrimReserveUpOnline[r,l,t,y];
s.t. R20_MinSecReserveUpOnline{r in REGION, l in TIMESLICE, y in YEAR}: SecReserveUpCapacityDemand[r,l,y]*MinSecReserveUpOnline[r,y] <= sum{t in TECHNOLOGY} SecReserveUpOnline[r,l,t,y];
s.t. R21_MaxPrimReserveUpOnline1{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "PrimReserveUp" && (MaxPrimReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxPrimReserveUp[r,t,y] < MinStableOperation[r,t,y])}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] = PrimReserveUpOnline[r,l,t,y];
s.t. R22_MaxSecReserveUpOnline1{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "SecReserveUp" && (MaxSecReserveDown[r,t,y] < MinStableOperation[r,t,y] || MaxSecReserveUp[r,t,y] < MinStableOperation[r,t,y])}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] = SecReserveUpOnline[r,l,t,y];
s.t. R23_MaxPrimReserveUpOnline1{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "PrimReserveUp" && (MaxPrimReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxPrimReserveUp[r,t,y] >= MinStableOperation[r,t,y])}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] >= PrimReserveUpOnline[r,l,t,y];
s.t. R24_MaxSecReserveUpOnline1{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: f = "SecReserveUp" && (MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y])}: sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] >= SecReserveUpOnline[r,l,t,y];
s.t. R25_MaxReserveUpOnline{r in REGION, f in FUEL, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && (MaxPrimReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxPrimReserveUp[r,t,y] >= MinStableOperation[r,t,y] || MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y])}: OnlineCapacity[r,l,t,y] - sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]/CapacityToActivityUnit[r,t] >= PrimReserveUpOnline[r,l,t,y] + SecReserveUpOnline[r,l,t,y];
s.t. R26_MaxPrimReserveUpOnline2{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: MaxPrimReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxPrimReserveUp[r,t,y] >= MinStableOperation[r,t,y]}: OnlineCapacity[r,l,t,y]*MaxPrimReserveUp[r,t,y] >= PrimReserveUpOnline[r,l,t,y];
s.t. R27_MaxSecReserveUpOnline2{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR: MaxSecReserveDown[r,t,y] >= MinStableOperation[r,t,y] && MaxSecReserveUp[r,t,y] >= MinStableOperation[r,t,y]}: OnlineCapacity[r,l,t,y]*MaxSecReserveUp[r,t,y] >= SecReserveUpOnline[r,l,t,y];
s.t. R28_MaxCycling{r in REGION, f in FUEL, l in TIMESLICE, ll in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && TimeSliceLinkTag[r,l,ll]<>0}: OnlineCapacity[r,ll,t,y]*(1-MaxOnlineCapReduction[r,t,y])*TimeSliceLinkTag[r,l,ll] <= OnlineCapacity[r,l,t,y];
s.t. R29_MaxGenerationChange{r in REGION, f in FUEL, l in TIMESLICE, ll in TIMESLICE, t in TECHNOLOGY, y in YEAR: ElectricityForTransmissionTag[r,f]=1 && TimeSliceLinkTag[r,l,ll]<>0}: (sum{m in MODE_OF_OPERATION}RateOfActivity[r,ll,t,m,y]*OutputActivityRatio[r,t,f,m,y] - OnlineCapacity[r,ll,t,y]*MaxGenerationReduction[r,t,y]*CapacityToActivityUnit[r,t])*TimeSliceLinkTag[r,l,ll] <= sum{m in MODE_OF_OPERATION}RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y];

#
###########################################################################################
#
solve;
#
#########################################################################################################
#																										#
# 	Summary results tables below are printed to a comma-separated file called "SelectedResults.csv"		#
#	For a full set of results please see "Results.txt"													#
#	If you don't want these printed, please comment-out or delete them.									#
#																										#
#########################################################################################################
#
#	table result{(f,t) in s} OUT "...": f~FROM, t~TO, x[f,t]~FLOW;
#	table result{y in YEAR, r in REGION} OUT "CSV" "Output.csv": y~YEARS, r~REGION, TotalDiscountedCost[y,r];
#
####	Summary results 	###
#
###		Total costs and emissions by region	###
#
printf "\n" > "SelectedResults.csv";
printf "Summary" >> "SelectedResults.csv";
for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";
					}
printf "\n" >> "SelectedResults.csv";
printf "Emissions" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
for {r in REGION} 	{
					for {e in EMISSION} 	{
											printf ",%s", e >> "SelectedResults.csv";
											printf ",%g", sum{l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y] + ModelPeriodExogenousEmission[r,e] >> "SelectedResults.csv";
											printf "\n" >> "SelectedResults.csv";
											}
					}
printf "\n" >> "SelectedResults.csv";
printf "Cost" >> "SelectedResults.csv";
for {r in REGION} {printf ",%g", sum{t in TECHNOLOGY, y in YEAR}(((((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*(VariableCost[r,t,m,y]+MarketPrice[r,t,l,m,y]))/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))+CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)))+DiscountedTechnologyEmissionsPenalty[r,t,y]-DiscountedSalvageValue[r,t,y]) + sum{s in STORAGE} (CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))-CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy))))) >> "SelectedResults.csv";
}
printf "\n" >> "SelectedResults.csv";
for {r in REGION} {printf ",%g", sum{t in TECHNOLOGY, y in YEAR}(((DiscountedTechnologyEmissionsPenalty[r,t,y]))) >> "SelectedResults.csv";
}
printf "\n" >> "SelectedResults.csv";

#
####	Total Annual Capacity	###
#
printf "\n" >> "SelectedResults.csv";
printf "TotalAnnualCapacity (Capacity Units)" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
for {t in TECHNOLOGY} {printf ",%s", t >> "SelectedResults.csv";}
printf "\n" >> "SelectedResults.csv";
for {r in REGION}	{
		for { y in YEAR } {
							printf "%g", y >> "SelectedResults.csv";
							for { t in TECHNOLOGY } {
													printf ",%g", ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) >> "SelectedResults.csv";
													}
							printf "\n" >> "SelectedResults.csv";
							}
					}

####	New Annual Capacity	###																			
#																					
printf "\n" >> "SelectedResults.csv";																					
printf "NewCapacity (Capacity Units )" >> "SelectedResults.csv";																					
printf "\n" >> "SelectedResults.csv";																					
printf "\n" >> "SelectedResults.csv";																					
for {t in TECHNOLOGY} 	{printf ",%s", t >> "SelectedResults.csv";}																				
printf "\n" >> "SelectedResults.csv";																					
for {r in REGION}	{																				
					for { y in YEAR } 	{															
										printf "%g", y >> "SelectedResults.csv";											
										for { t in TECHNOLOGY } 	{										
																	printf ",%g", NewCapacity[r,t,y] >> "SelectedResults.csv";				
																	}				
										printf "\n" >> "SelectedResults.csv";											
										}																	}	

#
### Annual Production ###
#
printf "\n" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
printf "Annual Production (Energy Units)" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
for {t in TECHNOLOGY} {printf ",%s", t >> "SelectedResults.csv";}
printf "\n" >> "SelectedResults.csv";
for {r in REGION}	{
		for {f in FUEL}{printf",%s",f >> "SelectedResults.csv";
		printf "\n" >> "SelectedResults.csv";
			for { y in YEAR } {
							printf "%g", y >> "SelectedResults.csv";

							for { t in TECHNOLOGY } {
													printf ",%g", sum{m in MODE_OF_OPERATION, l in TIMESLICE: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] * YearSplit[l,y] >> "SelectedResults.csv";
													}
							printf "\n" >> "SelectedResults.csv";
								}
						}
				}

#
###		Technology Production in each TS ###
#
printf "\n" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
printf "Production in Each TS (Power Units)" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";
	printf "\n" >> "SelectedResults.csv";
	for {t in TECHNOLOGY} {printf "%s", t >> "SelectedResults.csv";
					for {f in FUEL}{printf",%s",f >> "SelectedResults.csv";
					
						for {l in TIMESLICE}{
							printf ",%s", l >> "SelectedResults.csv";
						}
					}
					printf "\n" >> "SelectedResults.csv";
					for {y in YEAR } {
						printf "%g", y >> "SelectedResults.csv";
						for {f in FUEL}{printf "," >> "SelectedResults.csv";
							for { l in TIMESLICE} {
										printf ",%g", sum{m in MODE_OF_OPERATION: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] * YearSplit[l,y] / (YearSplit[l,y]*CapacityToActivityUnit[r,t]) >> "SelectedResults.csv";
								}
						}
						printf "\n" >> "SelectedResults.csv";
					}
	}
}

#
###		Total Annual  Cost & Emissions	###
#
printf "\n" >> "SelectedResults.csv";
printf "Annual Emissions (Emissions Units)" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
	for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";
						printf "\n" >> "SelectedResults.csv";
						for {e in EMISSION} 	{printf ",%s", e >> "SelectedResults.csv";
												printf "\n" >> "SelectedResults.csv";
												printf "\n" >> "SelectedResults.csv";
												for {y in YEAR } 	{
																	printf "%g", y >> "SelectedResults.csv";
																	printf ",%g", sum{l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y] >> "SelectedResults.csv";
																	printf "\n" >> "SelectedResults.csv";
																	}
												}
						}
						
printf "\n" >> "SelectedResults.csv";
printf "Cost (discounted)" >> "SelectedResults.csv";
printf "\n" >> "SelectedResults.csv";
	for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";
						printf "\n" >> "SelectedResults.csv";
							for {y in YEAR} 	{
									printf "%g", y >> "SelectedResults.csv";
									printf ",%g", sum{t in TECHNOLOGY}(((((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*(VariableCost[r,t,m,y]+MarketPrice[r,t,l,m,y]))/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))+CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)))+DiscountedTechnologyEmissionsPenalty[r,t,y]-DiscountedSalvageValue[r,t,y]) + sum{s in STORAGE} (CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))-CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy))))) >> "SelectedResults.csv";
									printf "\n" >> "SelectedResults.csv";
									}
								}
												#				
#### Reservoir Data
#
for {v in RESERVOIR} 
	{
		printf "\n" >> "SelectedResults.csv";
		printf ",%s", v >> "SelectedResults.csv";
		printf ", S, DT, DTB, Discharge, Ext Filling, Filling, Net w/in Y, Net w/in D, Spillage, RateOfEmptying" >> "SelectedResults.csv";
		
		printf "\n" >> "SelectedResults.csv";

			for {r in REGION : r = "BC"}
			{	
				printf " %s", r >> "SelectedResults.csv";
				for {y in YEAR}
				{
					printf "%s", y >> "SelectedResults.csv";
					for {ls in SEASON}
					{
						for {ld in DAYTYPE}
						{
							for {lh in DAILYTIMEBRACKET}
							{
								printf ",%s", r >> "SelectedResults.csv";
								printf ",%s", ls >> "SelectedResults.csv";
								printf ",%s", ld >> "SelectedResults.csv";
								printf ",%s", lh >> "SelectedResults.csv";
								printf ",%g", RateOfReservoirDischarge[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", RateOfExternalReservoirFilling[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", RateOfReservoirFilling[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", NetReservoirWithinYear[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", NetReservoirWithinDay[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", RateOfReservoirSpillageExpanded[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", RateOfReservoirEmptying[v,y,ls,ld,lh,r] >> "SelectedResults.csv";
								printf ",%g", ReservoirLevelSeasonStart[v,y,ls,r]  >> "SelectedResults.csv";
								printf ", , \n" >> "SelectedResults.csv";
							}
						}
					}
				
				printf "\n" >> "SelectedResults.csv";
			}
			printf "\n" >> "SelectedResults.csv";
		}
	}

########### ORIGINAL OUTPUT #######
#	####	Summary results 	###																			
#	#																					
#	###		Total costs and emissions by region	###																		
#	#																					
#	printf "\n" > "SelectedResults.csv";																					
#	printf "Summary" >> "SelectedResults.csv";																					
#	for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";																				
#						}																
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Emissions" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION} 	{																				
#						for {e in EMISSION} 	{															
#												printf ",%s", e >> "SelectedResults.csv";										
#												printf ",%g", sum{l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y] + ModelPeriodExogenousEmission[r,e] >> "SelectedResults.csv";										
#												printf "\n" >> "SelectedResults.csv";										
#												}										
#						}																
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Cost" >> "SelectedResults.csv";																					
#	for {r in REGION} {printf ",%g", sum{t in TECHNOLOGY, y in YEAR}(((((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y])*FixedCost[r,t,y] + sum{m in MODE_OF_OPERATION, l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y]*VariableCost[r,t,m,y])/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)+0.5))+CapitalCost[r,t,y] * NewCapacity[r,t,y]/((1+DiscountRate[r,t])^(y-min{yy in YEAR} min(yy)))+DiscountedTechnologyEmissionsPenalty[r,t,y]-DiscountedSalvageValue[r,t,y]) + sum{s in STORAGE} (CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy)))-CapitalCostStorage[r,s,y] * NewStorageCapacity[r,s,y]/((1+DiscountRateStorage[r,s])^(y-min{yy in YEAR} min(yy))))) >> "SelectedResults.csv";																					
#	}																					
#	printf "\n" >> "SelectedResults.csv";																					
#	#																					
#	### 	Time Independent demand	###																			
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "TID Demand" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#		for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";																			
#							printf "\n" >> "SelectedResults.csv";															
#							for {f in FUEL} {printf "\n" >> "SelectedResults.csv";															
#											printf ",%s", f >> "SelectedResults.csv";											
#											printf "\n" >> "SelectedResults.csv";											
#											for {y in YEAR } 	{										
#																printf "%g", y >> "SelectedResults.csv";						
#																printf ",%g", AccumulatedAnnualDemand[r,f,y] >> "SelectedResults.csv";						
#																printf "\n" >> "SelectedResults.csv";						
#																}						
#												}										
#							}															
#	#																					
#	### 	Time Dependent demand	###																			
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Time Dependent Demand (Energy Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#		for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";																				
#							printf "\n" >> "SelectedResults.csv";															
#							for {f in FUEL} {printf ",%s", f >> "SelectedResults.csv";															
#											printf "\n" >> "SelectedResults.csv";											
#											for {l in TIMESLICE}	{										
#																	printf ",%s", l >> "SelectedResults.csv";					
#																	}					
#											printf "\n" >> "SelectedResults.csv";											
#											for {y in YEAR } 	{										
#																printf "%g", y >> "SelectedResults.csv";						
#																for { l in TIMESLICE} 	{					
#																						printf ",%g", SpecifiedAnnualDemand[r,f,y]*SpecifiedDemandProfile[r,f,l,y] >> "SelectedResults.csv";
#																						}
#																printf "\n" >> "SelectedResults.csv";						
#																}						
#											}											
#							}															
#	#																					
#	### 	Time Dependent production ###																				
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Time Dependent Production (Energy Units) Test" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#		for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";																				
#							printf "\n" >> "SelectedResults.csv";															
#							for {f in FUEL} {printf ",%s", f >> "SelectedResults.csv";															
#											printf "\n" >> "SelectedResults.csv";											
#											for {l in TIMESLICE}	{										
#																	printf ",%s", l >> "SelectedResults.csv";					
#																	}					
#											printf "\n" >> "SelectedResults.csv";											
#											for {y in YEAR } 	{										
#																printf "%g", y >> "SelectedResults.csv";						
#																for { l in TIMESLICE} 	{					
#																						printf ",%g", sum{m in MODE_OF_OPERATION, t in TECHNOLOGY: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]*YearSplit[l,y] >> "SelectedResults.csv";
#																						}
#																printf "\n" >> "SelectedResults.csv";						
#																}						
#											}											
#							}															
#	#																					
#	####	Total Annual Capacity	###																			
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "TotalAnnualCapacity (Capacity Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {t in TECHNOLOGY} {printf ",%s", t >> "SelectedResults.csv";}																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION}	{																				
#			for { y in YEAR } {																			
#								printf "%g", y >> "SelectedResults.csv";														
#								for { t in TECHNOLOGY } {														
#														printf ",%g", ((sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy])+ ResidualCapacity[r,t,y]) >> "SelectedResults.csv";								
#														}								
#								printf "\n" >> "SelectedResults.csv";														
#								}														
#						}																
#	#																					
#	####	New Annual Capacity	###																			
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "NewCapacity (Capacity Units )" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {t in TECHNOLOGY} 	{printf ",%s", t >> "SelectedResults.csv";}																				
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION}	{																				
#						for { y in YEAR } 	{															
#											printf "%g", y >> "SelectedResults.csv";											
#											for { t in TECHNOLOGY } 	{										
#																		printf ",%g", CapacityOfOneTechnologyUnit[r,t,y]*NumberOfNewTechnologyUnits[r,t,y] >> "SelectedResults.csv";				
#																		}				
#											printf "\n" >> "SelectedResults.csv";											
#											}											
#						}																
#	#																					
#	### Annual Production ###																					
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Annual Production (Energy Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";																				
#						printf "\n" >> "SelectedResults.csv";																
#						for {t in TECHNOLOGY} 	{printf "%s", t >> "SelectedResults.csv";															
#												for {f in FUEL}{printf",%s",f >> "SelectedResults.csv";										
#																}						
#												printf "\n" >> "SelectedResults.csv";										
#												for {y in YEAR } 	{									
#																	printf "%g", y >> "SelectedResults.csv";					
#																	for {f in FUEL}{					
#																					printf ",%g", sum{m in MODE_OF_OPERATION, l in TIMESLICE: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] * YearSplit[l,y] >> "SelectedResults.csv";	
#																					}	
#																	printf "\n" >> "SelectedResults.csv";					
#																	}					
#							printf "\n" >> "SelectedResults.csv";															
#												}										
#						}																
#	#																					
#	### Annual Use ###																					
#	#																					
#	printf "Annual Use (Energy Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";																					
#						printf "\n" >> "SelectedResults.csv";																
#						for {t in TECHNOLOGY} 	{printf "%s", t >> "SelectedResults.csv";															
#												for {f in FUEL}{printf",%s",f >> "SelectedResults.csv";										
#																}						
#												printf "\n" >> "SelectedResults.csv";										
#												for {y in YEAR } 	{									
#																	printf "%g", y >> "SelectedResults.csv";					
#																	for {f in FUEL}{					
#																					printf ",%g", sum{m in MODE_OF_OPERATION, l in TIMESLICE: InputActivityRatio[r,t,f,m,y]<>0} RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y]*YearSplit[l,y] >> "SelectedResults.csv";	
#																					}	
#																	printf "\n" >> "SelectedResults.csv";					
#																	}					
#							printf "\n" >> "SelectedResults.csv";															
#												}										
#						}																
#	#																					
#	###		Technology Production in each TS ###																			
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "ProductionByTechnology (Energy Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";																					
#		printf "\n" >> "SelectedResults.csv";																				
#		for {t in TECHNOLOGY} {printf "%s", t >> "SelectedResults.csv";																				
#						for {f in FUEL}{printf",%s",f >> "SelectedResults.csv";																
#							for {l in TIMESLICE}{															
#								printf ",%s", l >> "SelectedResults.csv";														
#							}															
#						}																
#						printf "\n" >> "SelectedResults.csv";																
#						for {y in YEAR } {																
#							printf "%g", y >> "SelectedResults.csv";															
#							for {f in FUEL}{printf "," >> "SelectedResults.csv";															
#								for { l in TIMESLICE} {														
#											printf ",%g", sum{m in MODE_OF_OPERATION: OutputActivityRatio[r,t,f,m,y] <>0} RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y] * YearSplit[l,y] >> "SelectedResults.csv";											
#									}													
#							}															
#							printf "\n" >> "SelectedResults.csv";															
#						}																
#		}																				
#	}																					
#	#																					
#	###		Technology Use in each TS	###																		
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Use By Technology (Energy Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";																					
#		printf "\n" >> "SelectedResults.csv";																				
#		for {t in TECHNOLOGY} {printf "%s", t >> "SelectedResults.csv";																				
#						for {f in FUEL}{printf",%s",f >> "SelectedResults.csv";																
#							for {l in TIMESLICE}{															
#								printf ",%s", l >> "SelectedResults.csv";														
#							}															
#						}																
#						printf "\n" >> "SelectedResults.csv";																
#						for {y in YEAR } {																
#							printf "%g", y >> "SelectedResults.csv";															
#							for {f in FUEL}{printf "," >> "SelectedResults.csv";															
#								for { l in TIMESLICE} {														
#											printf ",%g", sum{m in MODE_OF_OPERATION: InputActivityRatio[r,t,f,m,y]<>0} RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y] * YearSplit[l,y] >> "SelectedResults.csv";											
#									}													
#							}															
#							printf "\n" >> "SelectedResults.csv";															
#						}																
#		}																				
#	}																					
#	#																					
#	###		Total Annual Emissions	###																		
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Annual Emissions (Emissions Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#		for {r in REGION} 	{printf ",%s", r >> "SelectedResults.csv";																			
#							printf "\n" >> "SelectedResults.csv";															
#							for {e in EMISSION} 	{printf ",%s", e >> "SelectedResults.csv";														
#													printf "\n" >> "SelectedResults.csv";									
#													printf "\n" >> "SelectedResults.csv";									
#													for {y in YEAR } 	{								
#																		printf "%g", y >> "SelectedResults.csv";				
#																		printf ",%g", sum{l in TIMESLICE, t in TECHNOLOGY, m in MODE_OF_OPERATION: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y] >> "SelectedResults.csv";				
#																		printf "\n" >> "SelectedResults.csv";				
#																		}				
#													}									
#							}															
#	#																					
#	### Annual Emissions by Technology ###																					
#	#																					
#	printf "\n" >> "SelectedResults.csv";																					
#	printf "Annual Emissions by Technology (Emissions Units)" >> "SelectedResults.csv";																					
#	printf "\n" >> "SelectedResults.csv";																					
#	for {r in REGION} {printf ",%s", r >> "SelectedResults.csv";																					
#						printf "\n" >> "SelectedResults.csv";																
#						for {t in TECHNOLOGY} 	{printf "%s", t >> "SelectedResults.csv";															
#												for {e in EMISSION}{printf",%s",e >> "SelectedResults.csv";										
#																}						
#												printf "\n" >> "SelectedResults.csv";										
#												for {y in YEAR } 	{									
#																	printf "%g", y >> "SelectedResults.csv";					
#																	for {e in EMISSION}{					
#																					printf ",%g", sum{l in TIMESLICE, m in MODE_OF_OPERATION: EmissionActivityRatio[r,t,e,m,y]<>0} EmissionActivityRatio[r,t,e,m,y]*RateOfActivity[r,l,t,m,y]*YearSplit[l,y] >> "SelectedResults.csv";	
#																					}	
#																	printf "\n" >> "SelectedResults.csv";					
#																	}					
#							printf "\n" >> "SelectedResults.csv";															
#												}										
#						}																
					
end;