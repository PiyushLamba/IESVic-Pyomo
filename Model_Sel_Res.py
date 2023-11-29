# IESVic Pyomo for OSeMOSYS:

from __future__ import division
from pyomo.environ import *
from pyomo.core import *
import os
import sys
import logging

# Functions for printing results

SelRes = open("./Model-Results/SelRes.csv", "w") # Create selected results file (now in csv format)

def Disc_Sys_Costs(model):
	return sum(
		(
			(
				(
					sum(model.NewCapacity[r, t, yy] for yy in model.YEAR if y-yy <
						model.OperationalLife[r, t] and y-yy >= 0) + model.ResidualCapacity[r, t, y]
				)
				* model.FixedCost[r, t, y] + sum(model.RateOfActivity[r, l, t, m, y] * model.YearSplit[l, y]*model.VariableCost[r, t, m, y] for m in model.MODE_OF_OPERATION for l in model.TIMESLICE)
			) / ((1 + model.DiscountRate[r])**(y - min(model.YEAR)+0.5)) + model.CapitalCost[r, t, y] * model.NewCapacity[r, t, y] / ((1 + model.DiscountRate[r])**(y - min(model.YEAR))) + model.DiscountedTechnologyEmissionsPenalty[r, t, y] - model.DiscountedSalvageValue[r, t, y]

		)
		for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)
	+ sum(model.CapitalCostStorage[r, s, y] * model.NewStorageCapacity[r, s, y] / ((1 + model.DiscountRate[r])**(min(model.YEAR)+1))
		for r in model.REGION for s in model.STORAGE for y in model.YEAR)


def Disc_Gen_Capital_Costs(model):
	return sum((model.CapitalCost[r,t,y] * model.NewCapacity[r,t,y])
		/ ((1+ model.DiscountRate[r])** (y- min(model.YEAR)))
		for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Disc_Gen_Fixed_Costs(model):
	return sum(
		(
			sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y-yy >= 0) + model.ResidualCapacity[r,t,y] * model.FixedCost[r,t,y]
		) / ((1 + model.DiscountRate[r])** (y - min(model.YEAR) + 0.5))
	for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Disc_Gen_Variable_Costs(model):
	return sum(
		sum(model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.VariableCost[r,t,m,y] 
		for m in model.MODE_OF_OPERATION for l in model.TIMESLICE)
		/ ((1 + model.DiscountRate[r])**(y - min(model.YEAR) + 0.5))
	for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Disc_Gen_Emissions_Costs(model):
	return sum(model.DiscountedTechnologyEmissionsPenalty[r,t,y] for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Disc_Gen_SalvaValue_Costs(model):
	return sum(model.DiscountedSalvageValue[r, t, y] for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Disc_Storage_Capital_Costs(model):
	return sum(
		model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y] / ((1 + model.DiscountRate[r])**(y - min(model.YEAR)))
	for r in model.REGION for s in model.STORAGE for y in model.YEAR)

def Disc_Sto_SalvaValue_Costs(model):
	return sum(model.SalvageValueStorage[r,s,y] / ((1+ model.DiscountRate[r])**max(model.YEAR)+1) 
			   for r in model.REGION for s in model.STORAGE for y in model.YEAR)

def Non_Disc_Sys_Costs(model):
	return sum(
		(
			(
				(
					sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y -yy >= 0)
					+ model.ResidualCapacity[r,t,y]
				) 
				* model.FixedCost[r,t,y] + sum(model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.VariableCost[r,t,m,y] 
				for m in model.MODE_OF_OPERATION for l in model.TIMESLICE)
			) 
			+ model.CapitalCost[r,t,y] * model.NewCapacity[r,t,y]
			+ sum(model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.EmissionsPenalty[r,e,y]
			for e in model.EMISSION for l in model.TIMESLICE for m in model.MODE_OF_OPERATION)
			- model.SalvageValue[r,t,y]
		)
	for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)
	+ sum(
		model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y] - model.SalvageValueStorage[r,s,y]
	for r in model.REGION for s in model.STORAGE for y in model.YEAR)

def Non_Disc_Gen_Capital_Costs(model):
	return sum(model.CapitalCost[r,t,y] * model.NewCapacity[r,t,y]
		for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Non_Disc_Gen_Fixed_Costs(model):
	return sum(
		(
			sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y-yy >= 0) + model.ResidualCapacity[r,t,y] * model.FixedCost[r,t,y]
		)
	for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Non_Disc_Gen_Variable_Costs(model):
	return sum(
		sum(model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.VariableCost[r,t,m,y] 
		for m in model.MODE_OF_OPERATION for l in model.TIMESLICE)
	for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Non_Disc_Gen_Emissions_Costs(model):
	return sum(
		sum(
			model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.EmissionsPenalty[r,e,y]
		for e in model.EMISSION for l in model.TIMESLICE for m in model.MODE_OF_OPERATION)
	for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Non_Disc_Gen_SalvaValue_Costs(model):
	return sum(model.SalvageValue[r, t, y] for r in model.REGION for t in model.TECHNOLOGY for y in model.YEAR)

def Non_Disc_Storage_Capital_Costs(model):
	return sum(
		model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y]
	for r in model.REGION for s in model.STORAGE for y in model.YEAR)

def Non_Disc_Sto_SalvaValue_Costs(model):
	return sum(model.SalvageValueStorage[r,s,y] for r in model.REGION for s in model.STORAGE for y in model.YEAR)

def Model_Summary(model):
	for r in model.REGION:
		print("\nSummary for each region: \n", r,":", file=SelRes)
	
		print("Emissions:\n", file=SelRes)
		for e in model.EMISSION:
			print(e,",",value(sum(model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] + model.ModelPeriodExogenousEmission[r,e]
			for l in model.TIMESLICE for t in model.TECHNOLOGY for m in model.MODE_OF_OPERATION for y in model.YEAR
			if model.EmissionActivityRatio[r,t,e,m,y] != 0)), "\n", file=SelRes)
		
		print ("\nTotal Annual Power Capacity (GW)\n", file=SelRes)
		for y in model.YEAR:
			print("\n",y, "\t", file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",", value(sum(
					model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y - yy >= 0) + model.ResidualCapacity[r,t,y]),
					"\n", file=SelRes)
		
		print("\nTotal Annual Energy Storage Capacity (GWh)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, "\t", file=SelRes)
			for s in model.STORAGE:
				print(s,",", value(sum(model.NewStorageCapacity[r,s,yy] 
				for yy in model.YEAR if y - yy < model.OperationalLifeStorage[r,s] and y - yy >= 0)+ model.ResidualStorageCapacity[r,s,y]),
				"\n", file=SelRes)
		
		print("\nNew Annual Power Capacity (GW)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",", value(model.NewCapacity[r,t,y]),"\n", file=SelRes)
		
		print("\nAnnual Fuel Generation per fuel type (GWh)\n", file=SelRes)
		for f in model.FUEL:
			print("\n", f, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",", value(sum(
					model.RateOfActivity[r,l,t,m,2015] * model.OutputActivityRatio[r,t,f,m,2015] * model.YearSplit[l,2015]
				for m in model.MODE_OF_OPERATION for l in model.TIMESLICE if model.OutputActivityRatio[r,t,f,m,2015] != 0)), 
				"\n", file=SelRes)
		
		print("\nAnnual Electricity Generation for dELEC (GWh)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",", value(sum(
					model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,'dELEC',m,y] * model.YearSplit[l,y]
				for m in model.MODE_OF_OPERATION for l in model.TIMESLICE if model.OutputActivityRatio[r,t,'dELEC',m,y] != 0)),
				"\n",file=SelRes)
		
		print("\nAnnual Heat Generation for dHEAT (GWh)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",",
					value(sum(
						model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,'dHEAT',m,y] * model.YearSplit[l,y]
					for m in model.MODE_OF_OPERATION for l in model.TIMESLICE if model.OutputActivityRatio[r,t,'dHEAT', m,y] != 0)),
				"\n", file=SelRes)
		
		print("\nAnnual Capacity Factor for dELEC Production (fraction)\n",file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",", value(sum(
					model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.OutputActivityRatio[r,t,f,m,y]
				for m in model.MODE_OF_OPERATION for l in model.TIMESLICE for f in model.FUEL if model.OutputActivityRatio[r,t,'dELEC',m,y] != 0 and
				(value(sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y - yy >= 0)+ model.ResidualCapacity[r,t,y]) > 0)
				) 
				/ ((sum(model.NewCapacity[r,t,yy] 
				for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y - yy >= 0) + model.ResidualCapacity[r,t,y]) * 8760)), "\n", file=SelRes)
		
		print("\nAnnual Capacity Factor for dHEAT Production (fraction)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t,",", value(sum(
					model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.OutputActivityRatio[r,t,f,m,y]
				for m in model.MODE_OF_OPERATION for l in model.TIMESLICE for f in model.FUEL if model.OutputActivityRatio[r,t,'dHEAT',m,y] != 0 and
					(value(sum(model.NewCapacity[r, t, yy] for yy in model.YEAR if y - yy <
					 model.OperationalLife[r, t] and y - yy >= 0) + model.ResidualCapacity[r, t, y]) > 0)
				)
				/ ((sum(model.NewCapacity[r, t, yy]
				for yy in model.YEAR if y - yy < model.OperationalLife[r, t] and y - yy >= 0) + model.ResidualCapacity[r, t, y]) * 8760)), "\n", file=SelRes)
		
		print("\nAnnual Emissions (Mt)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for e in model.EMISSION:
				print(e,",", value(sum(
					model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y]
				for l in model.TIMESLICE for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY if model.EmissionActivityRatio[r,t,e,m,y] != 0)), "\n", file=SelRes)

		print("\nAnnual Emissions by Technology (Mt)\n", file=SelRes)
		for e in model.EMISSION:
			for t in model.TECHNOLOGY:
				print(t, file=SelRes)
			for y in model.YEAR:
				print("\n", y, file=SelRes)
				for t in model.TECHNOLOGY:
					print(e,",", value(sum(
						model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y]
					for l in model.TIMESLICE for m in model.MODE_OF_OPERATION if model.EmissionActivityRatio[r,t,e,m,y] != 0)), "\n", file=SelRes)
		
		print("\nEmission Intensity (gCO2/kWh)\n", file=SelRes)
		for y in model.YEAR:
			for e in model.EMISSION:
				print(y,",", value(sum(
					model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] / model.SpecifiedAnnualDemand[r,'dELEC',y] *1000000
				for l in model.TIMESLICE for t in model.TECHNOLOGY for m in model.MODE_OF_OPERATION if model.EmissionActivityRatio[r,t,e,m,y] != 0)), "\n", file=SelRes)
		
		print("\nExogenous demand for fuel type (GWh)\n", file=SelRes)
		for y in model.YEAR:
			for l in model.TIMESLICE:
				print(l,"\n", file=SelRes)
			for f in model.FUEL:
				print(f, file=SelRes)
				for l in model.TIMESLICE:
					print(y,",", value(
						model.SpecifiedAnnualDemand[r, f, y] * model.SpecifiedDemandProfile[r, f, l, y] / (model.YearSplit[l, y]*8760)), "\n", file=SelRes)
		
		print("\nElectricity Generation dELEC per Technology and Time Slice (GWh)\n", file=SelRes)
		for y in model.YEAR:
			print(y, file=SelRes)
			for t in model.TECHNOLOGY:
				for l in model.TIMESLICE:
					print(l, ",", value(sum(
						model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,'dELEC',m,y] * model.YearSplit[l,y]
					for m in model.MODE_OF_OPERATION if model.OutputActivityRatio[r,t,'dELEC',m,y] != 0)), "\n", file= SelRes)
		
		print("\nHeat Generation dHEAT per Technology and Time Slice (GWh)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print("\n", t, file=SelRes)
				for l in model.TIMESLICE:
					print(l, ",", value(sum(
						model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,'dHEAT', m,y] * model.YearSplit[l,y]
					for m in model.MODE_OF_OPERATION if model.OutputActivityRatio[r,t,'dHEAT', m,y] != 0)), "\n", file=SelRes)
		
		print("\nStorage Level at Start of Time Slice (GWh)\n", file=SelRes)
		for y in model.YEAR:
			print(y, file=SelRes)
			for s in model.STORAGE:
				print(s, file=SelRes)
				for l in model.TIMESLICE:
					print(l, ",", value(model.StorageLevelTSStart[r,s,l,y]),"\n",file=SelRes)
		
		print("\nStorage Level Start and End (GWh)\n", file=SelRes)
		for s in model.STORAGE:
			print(s,",", value(model.StorageLevelStart[r,s]), "\n", file=SelRes)

		print("\nCURTAILED Electricity Generation dELEC per Technology and Time Slice (GWh) (VRE ONLY!)\n", file=SelRes)
		for y in model.YEAR:
			print(y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t, file=SelRes)
				for l in model.TIMESLICE:
					print(l,",", value(sum(
						(sum(model.NewCapacity[r, t, yy] for yy in model.YEAR if y - yy <
						 model.OperationalLife[r, t] and y - yy >= 0) + model.ResidualCapacity[r, t, y])
						* (model.CapacityFactor[r, t, l, y] * model.CapacityToActivityUnit[r, t] * model.OutputActivityRatio[r, t, 'dELEC', m, y] * model.YearSplit[l, y])
						- (model.RateOfActivity[r, l, t, m, y] *
						   model.OutputActivityRatio[r, t, 'dELEC', m, y] * model.YearSplit[l, y])
						for m in model.MODE_OF_OPERATION if model.OutputActivityRatio[r, t, 'dELEC', m, y] != 0)), "\n", file=SelRes)
		
		print("\nCURTAILED Annual Electricity Generation for dELEC (GWh) (VRE ONLY!)\n", file=SelRes)       
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t, ",", value(sum(
					(sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y - yy >= 0) + model.ResidualCapacity[r,t,y])
					* (model.CapacityFactor[r,t,l,y] * model.CapacityToActivityUnit[r,t] * model.OutputActivityRatio[r,t,'dELEC', m,y] * model.YearSplit[l,y])
					- (model.RateOfActivity[r,l,t,m,y] * model.OutputActivityRatio[r,t,'dELEC', m,y] * model.YearSplit[l,y])
				for m in model.MODE_OF_OPERATION for l in model.TIMESLICE if model.OutputActivityRatio[r,t,'dELEC', m,y] != 0)), "\n", file=SelRes)
			
		print("\nDiscounted total TECHNOLOGY-specific costs (M$)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t, ",", value(
					(
						(
							(
								sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y - yy >= 0)
								+ model.ResidualCapacity[r,t,y]
							) * model.FixedCost[r,t,y]
						+ sum(model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.VariableCost[r,t,m,y] for m in model.MODE_OF_OPERATION for l in model.TIMESLICE)
						) / ((1 + model.DiscountRate[r])**(y - min(model.YEAR) + 0.5))
						+ model.CapitalCost[r,t,y] * model.NewCapacity[r,t,y] / ((1 + model.DiscountRate[r])**(y - min(model.YEAR)))
						+ model.DiscountedTechnologyEmissionsPenalty[r,t,y] - model.DiscountedSalvageValue[r,t,y]
					)
				), "\n", file=SelRes)
		
		print("\nNon-discounted total TECHNOLOGY-specific costs (M$)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for t in model.TECHNOLOGY:
				print(t, ",", value(
					(
						(
							(
								sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if y - yy < model.OperationalLife[r,t] and y - yy >= 0)
								+ model.ResidualCapacity[r,t,y]
							)  * model.FixedCost[r,t,y]
							+ sum(model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.VariableCost[r,t,m,y] for m in model.MODE_OF_OPERATION for l in model.TIMESLICE)
						)
						+ model.CapitalCost[r,t,y] * model.NewCapacity[r,t,y]
						+ sum(model.EmissionActivityRatio[r,t,e,m,y] * model.RateOfActivity[r,l,t,m,y] * model.YearSplit[l,y] * model.EmissionsPenalty[r,e,y] for e in model.EMISSION for l in model.TIMESLICE for m in model.MODE_OF_OPERATION)
						- model.SalvageValue[r,t,y]
					)
				), "\n", file=SelRes)
		
		print("\nDiscounted total STORAGE-specific costs (M$)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for s in model.STORAGE:
				print(s, ",", value(
					model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y]
					/ ((1 + model.DiscountRate[r])** (y - min(model.YEAR)))
					- model.SalvageValueStorage[r,s,y]
					/ ((1+model.DiscountRate[r])**(max(model.YEAR) - min(model.YEAR) + 1))
				), "\n", file=SelRes)
		
		print("\nNon-discounted total STORAGE-specific costs (M$)\n", file=SelRes)
		for y in model.YEAR:
			print("\n", y, file=SelRes)
			for s in model.STORAGE:
				print(s, ",", value(
					model.CapitalCostStorage[r,s,y] * model.NewStorageCapacity[r,s,y]
					- model.SalvageValueStorage[r,s,y]
				), "\n", file=SelRes)    

# Printing selected results

def Selected_Results(instance):

	print("Costs in M$: ", file=SelRes)
	print("Total Costs, Generator Capital Costs, Generator Fixed Costs, Generator Variable Costs, Emission Costs, Generator Salvage Value, Storage Capital Costs, Storage Salvage Value \n", file=SelRes)
	print("Discounted values: ", file=SelRes)

	discounted_system_costs = Disc_Sys_Costs(instance) # This value is the objective function value (too high at the moment)
	print("Discounted system costs (total costs), ", value(discounted_system_costs), file=SelRes)

	discounted_generator_capital_costs = Disc_Gen_Capital_Costs(instance) # Value is too high at the moment
	print("Disounted generator capital costs, ", value(discounted_generator_capital_costs), file=SelRes)

	discounted_generator_fixed_costs = Disc_Gen_Fixed_Costs(instance) # Value is too low at the moment
	print("Disounted generator fixed costs, ", value(discounted_generator_fixed_costs), file=SelRes)

	discounted_generator_variable_costs = Disc_Gen_Variable_Costs(instance) # Value is too high at the moment
	print("Disounted generator variable costs, ", value(discounted_generator_variable_costs), file=SelRes)

	discounted_generator_emissions_costs = Disc_Gen_Emissions_Costs(instance) # Value is correct
	print("Disounted generator emissions costs, ", value(discounted_generator_emissions_costs), file=SelRes)

	discounted_generator_salavage_value = Disc_Gen_SalvaValue_Costs(instance) # Value is correct
	print("Discounted generator salvage value, ", value(discounted_generator_salavage_value), file=SelRes)

	discounted_storage_capital_costs = Disc_Storage_Capital_Costs(instance) # Value is correct
	print("Disounted storage capital costs, ", value(discounted_storage_capital_costs), file=SelRes)

	discounted_storage_salavage_value = Disc_Sto_SalvaValue_Costs(instance) # Value is correct
	print("Discounted storage salvage value, ", value(discounted_storage_salavage_value), file=SelRes)

	print("\nNon-discounted values: ", file=SelRes)

	non_discounted_system_costs = Non_Disc_Sys_Costs(instance)
	print("Non-discounted system costs (total costs), ", value(non_discounted_system_costs), file=SelRes)

	non_discounted_generator_capital_costs = Non_Disc_Gen_Capital_Costs(instance)
	print("Non-disounted generator capital costs, ", value(non_discounted_generator_capital_costs), file=SelRes)

	non_discounted_generator_fixed_costs = Non_Disc_Gen_Fixed_Costs(instance)
	print("Non-disounted generator fixed costs, ", value(non_discounted_generator_fixed_costs), file=SelRes)

	non_discounted_generator_variable_costs = Non_Disc_Gen_Variable_Costs(instance)
	print("Non-disounted generator variable costs, ", value(non_discounted_generator_variable_costs), file=SelRes)

	non_discounted_generator_emissions_costs = Non_Disc_Gen_Emissions_Costs(instance)
	print("Non-disounted generator emissions costs, ", value(non_discounted_generator_emissions_costs), file=SelRes)

	non_discounted_generator_salavage_value = Non_Disc_Gen_SalvaValue_Costs(instance)
	print("Non-discounted generator salvage value, ", value(non_discounted_generator_salavage_value), file=SelRes)

	non_discounted_storage_capital_costs = Non_Disc_Storage_Capital_Costs(instance)
	print("Non-disounted storage capital costs, ", value(non_discounted_storage_capital_costs), file=SelRes)

	non_discounted_storage_salavage_value = Non_Disc_Sto_SalvaValue_Costs(instance)
	print("Non-discounted storage salvage value, ", value(non_discounted_storage_salavage_value), file=SelRes)
	
	Model_Summary(instance) # Print a summary of model results