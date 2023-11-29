import csv
import pandas as pd

def data_formatting(input_file):
    capacity, new_capacity, dELEC = False, False, False
    capacity_rows, new_capacity_rows, dELEC_rows = [],[],[]
    cap_columns, new_capacity_columns, dELEC_columns  = None, None, None
    region = None
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for row in csv_reader:

            if capacity:
                if len(row) == 0:
                    capacity = False
                    continue
                if not row[0]:
                    cap_columns = row
                else:
                    capacity_rows.append(row)

            if dELEC:
                if len(row) == 0:
                    dELEC = False
                elif row[1] == "dELEC":
                    continue
                elif not row[0]:
                    dELEC_columns = row
                else:
                    dELEC_rows.append(row)

            if new_capacity:
                if len(row) == 0:
                    continue
                if not row[0]:
                    new_capacity_columns = row
                else:
                    new_capacity_rows.append(row)

                if row[0] == "2065":
                    new_capacity = False
                    break

            if len(row) != 0:
                if row[0] == "Summary":
                    region = row[1]
                if row[0] == "TotalAnnualCapacity (GW)":
                    capacity = True
                if row[0] == "New Annual Capacity (GW)":
                    new_capacity = True
                if row[0] == "Annual Electricity Generation for dELEC(GWh)":
                    dELEC = True
            
    # columns = ["Model", "Scenario", "Region", "Variable", "Unit"]
    # capacity_df = pd.DataFrame([], columns=cap_columns)
    # dELEC_df = pd.DataFrame([], columns=emission_columns)
    years = []
    entries = []
    for i,gen_type in enumerate(cap_columns[20:36]):
        got_years = False
        scenario = None
    
        if gen_type[0] == 'g':
            if "WIND" in gen_type:
                scenario = 'g'
                gen_type = "WIND"
            elif "gen" in gen_type:
                scenario = 'g'
                gen_type = gen_type[3:]
            else:
                scenario = 'g'
                gen_type = gen_type[1:]
        elif gen_type[0] == 'p':
            scenario = 'Pellet'
            gen_type = gen_type[1:]
        elif gen_type[0] == 'r':
            scenario = 'Residue'
            gen_type = gen_type[1:]

        variable = f"Total Capacity|{gen_type}"
        capacity_values = []
        for j,row in enumerate(capacity_rows):
            if i != 0:
                got_years = True
            if not got_years:
                year = row[0]
                years.append(year)
            
            capacity_at_year = float(row[i+20])
            capacity_values.append(capacity_at_year)

        values = ["OSMOSIS", scenario, region, variable, "GW"]
        values += capacity_values   
        entries.append(values)
        
    columns = ["Model", "Scenario", "Region", "Variable", "Unit"]
    columns += years

    capacity_df = pd.DataFrame([], columns=columns)
    for i,row in enumerate(entries):
        new_row = pd.DataFrame([row], columns=columns)
        capacity_df = pd.concat([capacity_df,new_row], ignore_index=True)

    entries = []

    for i,gen_type in enumerate(dELEC_columns[20:36]):
        scenario = None
    
        if gen_type[0] == 'g':
            if "WIND" in gen_type:
                scenario = 'g'
                gen_type = "WIND"
            elif "gen" in gen_type:
                scenario = 'g'
                gen_type = gen_type[3:]
            else:
                scenario = 'g'
                gen_type = gen_type[1:]
        elif gen_type[0] == 'p':
            scenario = 'p'
            gen_type = gen_type[1:]
        elif gen_type[0] == 'r':
            scenario = 'r'
            gen_type = gen_type[1:]
        
        variable = f"Electricity Generation|{gen_type}"
        got_years = False
        dELEC_values = []
        for j,row in enumerate(dELEC_rows):
            if i != 0:
                got_years = True
            if not got_years:
                years.append(row[0])
            dELEC_at_year = float(row[i+20])
            dELEC_values.append(dELEC_at_year)
    

        values = ["OSMOSIS", scenario, region, variable, "GWh"]
        values += dELEC_values
        entries.append(values)
        
    dELEC_df = pd.DataFrame([], columns=columns)
    for i,row in enumerate(entries):
        new_row = pd.DataFrame([row], columns=columns)
        dELEC_df = pd.concat([dELEC_df,new_row], ignore_index=True)
    entries = []
    for i,gen_type in enumerate(new_capacity_columns[20:36]):
        scenario = "None"

        if gen_type[0] == 'g':
            if "WIND" in gen_type:
                scenario = 'g'
                gen_type = "WIND"
            elif "gen" in gen_type:
                scenario = 'g'
                gen_type = gen_type[3:]
            else:
                scenario = 'g'
                gen_type = gen_type[1:]
        elif gen_type[0] == 'p':
            scenario = 'p'
            gen_type = gen_type[1:]
        elif gen_type[0] == 'r':
            scenario = 'r'
            gen_type = gen_type[1:]
        
        variable = f"New Capacity|{gen_type}"
        got_years = False
        new_capacity_values = []
        for j,row in enumerate(new_capacity_rows):
            if i != 0:
                got_years = True
            if not got_years:
                years.append(row[0])
            new_capacity_at_year = float(row[i+20])
            new_capacity_values.append(new_capacity_at_year)
    

        values = ["OSMOSIS", scenario, region, variable, "GW"]
        values += new_capacity_values
        entries.append(values)
        
    new_capacity_df = pd.DataFrame([], columns=columns)
    for i,row in enumerate(entries):
        new_row = pd.DataFrame([row], columns=columns)
        new_capacity_df = pd.concat([new_capacity_df,new_row], ignore_index=True)


    total_df = pd.concat([capacity_df,dELEC_df], ignore_index=True)
    total_df = pd.concat([total_df,new_capacity_df], ignore_index=True)

    emissions_df = annual_emissions(input_file)
    total_df = pd.concat([total_df, emissions_df], ignore_index = True)
    total_df = total_df.groupby(["Model", "Scenario", "Region", "Variable", "Unit"], sort = False).sum().reset_index()
    total_df.to_csv(f"{input_file.split('.')[0]}-formatted.csv")
    return region

def annual_emissions(input_file):
    emissions = False
    rows = []
    columns = []
    region = None
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:

            if emissions:
                if len(row) == 0:
                    emissions = False
                elif row[1] == region:
                    continue
                elif not row[0]:
                    columns = row
                else:
                    rows.append(row)

            if len(row) == 0:
                continue
            else:
                if row[0] == "Summary":
                    region = row[1]
                if row[0] == "Annual Emissions (Emissions Units)":
                    emissions = True

    years = []  
    entries = []
    got_years = False
    for i,emission in enumerate(columns[1:2]):
        variable = f"Annual Emissions|{emission}"
        values = []
        
        for j,row in enumerate(rows):
            if i != 0:
                got_years = True
            if not got_years:
                year = row[0]
                years.append(year)

            values.append(row[i+1])

        entry = ["OSMOSIS", "g", region, variable, "Emission Units"]
        entry += values
        entries.append(entry)
    columns = ["Model", "Scenario", "Region", "Variable", "Unit"]
    columns += years

    emissions_df = pd.DataFrame([], columns=columns)
    for row in entries:
        new_row = pd.DataFrame([row], columns=columns)
        emissions_df = pd.concat([emissions_df,new_row], ignore_index=True)

    return emissions_df
