import pandas as pd
import os

# Set up

timeslices = 24 # Give total number of timeslices for the model

# Read CSV / Add the file with demand data inside the read_cv command
input_file = pd.read_csv("./Provincial_SILVER_Demands_MW_2019.csv", sep=",", index_col=False)
date = pd.to_datetime(input_file['Date'])


xl_file = pd.ExcelWriter('XL_Demands_2015.xlsx')
input_file.to_excel(xl_file, index=False)
xl_file.save()


SAD = input_file['Total_Demand'].mean() # Get Specified Annual Demand
print('Specified Annual Demand: ', SAD)

#SDP = pd.DataFrame(SAD / input_file['Total_Demand'][:timeslices] / sum(SAD / input_file['Total_Demand'][:timeslices])) 

# Get Specified Demand Profile (value of demand for every timeslice)
if timeslices is 24 or timeslices is 48: # 1 Season (1 or 2 days)
    SDP = pd.DataFrame(SAD / input_file['Total_Demand'][:timeslices] / sum(SAD / input_file['Total_Demand'][:timeslices])) 
elif timeslices is 72: # 3 Seasons (1 day)
    SDP = pd.DataFrame(SAD / input_file['Total_Demand'][:24] / sum(SAD / input_file['Total_Demand'][:24]))
    x1 = pd.DataFrame(SAD / input_file['Total_Demand'][1920:1944] / sum(SAD / input_file['Total_Demand'][1920:1944]))
    x2 = pd.DataFrame(SAD / input_file['Total_Demand'][4128:4152] / sum(SAD / input_file['Total_Demand'][4128:4152]))
    #SDP.loc[24] = x1['Total_Demand'][:]
    SDP.append(x1, ignore_index=True)#,on='Total_Demand', how='right')
    SDP.append(x2, ignore_index=True)#, on='Total_Demand', how='right')
    #print(x1)
elif timeslices is 144: # 3 Seasons (2 days)
    SDP = pd.DataFrame(SAD / input_file['Total_Demand'][:48] / sum(SAD / input_file['Total_Demand'][:48]))
    x1 = pd.Series(list(SAD / input_file['Total_Demand'][1920:1968] / sum(SAD / input_file['Total_Demand'][1920:1968])))
    x2 = pd.Series(list(SAD / input_file['Total_Demand'][4128:4176] / sum(SAD / input_file['Total_Demand'][4128:4176])))
    SDP['Total_Demand'].append(x1,ignore_index=False)
    SDP['Total_Demand'].append(x2,ignore_index=False)
else:
    print("Unsupported number of timeslices")

#print(SDP)

# Write specified demand profile to file
demand_profile_file = pd.ExcelWriter('Specified_Demand_Profile.xlsx')
SDP['Total_Demand'].to_excel(demand_profile_file)
demand_profile_file.save()