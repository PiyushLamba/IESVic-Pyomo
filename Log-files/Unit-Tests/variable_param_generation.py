import random;

YEAR = ["2015"]
TECHNOLOGY = ["rWASTE", "rNGAS_WELL", "rH2_ELECTRO", "gWASTEu", "gSOLARu", \
              "gHYDRO_FLEXr", "gHYDRO_MUSTRUNr", "gWINDr", "gSOLARr", "hBASEBOARDe", \
                "hHEATPUMPe", "hFURNACEg", "gPUMPED_HYDROr1", "gGAS_STOR", "gDUMMY", "hDUMMY"]
TIMESLICE = [str(i + 1) for i in range(48)]
FUEL = ["dELEC", "dHEAT", "fWASTE", "fGAS"]
EMISSION = ["CO2"]
MODE_OF_OPERATION = ["1"]
REGION = ["Vancouver"]
SEASON = ["1"]
DAYTYPE = ["1"]
DAILYTIMEBRACKET = [str(i + 1) for i in range(48)]
STORAGE = ["sPUMPED_HYDROr1", "sGAS_STOR"]

var_keys = dict()
var_keys["StorageLevelStart"] = [(r, s) for r in REGION for s in STORAGE]
var_keys["StorageLevelTSStart"] = [(r, s, l, y) for r in REGION for s in STORAGE for l in TIMESLICE for y in YEAR]
var_keys["NewStorageCapacity"] = [(r, s, y) for r in REGION for s in STORAGE for y in YEAR]
var_keys["SalvageValueStorage"] = [(r, s, y) for r in REGION for s in STORAGE for y in YEAR]
var_keys["StorageLevelYearStart"] = [(r, s, y) for r in REGION for s in STORAGE for y in YEAR]
var_keys["StorageLevelYearFinish"] = [(r, s, y) for r in REGION for s in STORAGE for y in YEAR]
var_keys["StorageLevelSeasonStart"] = [(r, s, ls, y) for r in REGION for s in STORAGE for ls in SEASON for y in YEAR]
var_keys["StorageLevelDayTypeStart"] = [(r, s, ls, ld, y) for r in REGION for s in STORAGE for ls in SEASON for ld in DAYTYPE for y in YEAR]
var_keys["StorageLevelDayTypeFinish"] = [(r, s, ls, ld, y) for r in REGION for s in STORAGE for ls in SEASON for ld in DAYTYPE for y in YEAR]
var_keys["NumberOfNewTechnologyUnits"] = [(r, t, y) for r in REGION for t in TECHNOLOGY for y in YEAR]
var_keys["NewCapacity"] = [(r, t, y) for r in REGION for t in TECHNOLOGY for y in YEAR]
var_keys["RateOfActivity"] = [(r, l, t, m, y) for r in REGION for l in TIMESLICE for t in TECHNOLOGY for m in MODE_OF_OPERATION for y in YEAR]
var_keys["UseByTechnology"] = [(r, l, t, f, y) for r in REGION for l in TIMESLICE for t in TECHNOLOGY for f in FUEL for y in YEAR]
var_keys["Trade"] = [(r, rr, l, f, y) for r in REGION for rr in REGION for l in TIMESLICE for f in FUEL for y in YEAR]
var_keys["UseAnnual"] = [(r, f, y) for r in REGION for f in FUEL for y in YEAR]
var_keys["VariableOperatingCost"] = [(r, t, l, y) for r in REGION for t in TECHNOLOGY for l in TIMESLICE for y in YEAR]
var_keys["SalvageValue"]  = [(r, t, y) for r in REGION for t in TECHNOLOGY for y in YEAR]
var_keys["DiscountedSalvageValue"] = [(r, t, y) for r in REGION for t in TECHNOLOGY for y in YEAR]
var_keys["OperatingCost"] = [(r, t, y) for r in REGION for t in TECHNOLOGY for y in YEAR]
var_keys["DiscountedTechnologyEmissionsPenalty"] = [(r, t, y) for r in REGION for t in TECHNOLOGY for y in YEAR]
var_keys["ModelPeriodEmissions"] = [(r, e) for r in REGION for e in EMISSION]

f = open("./result/variable_parameter_data", "w")
for k in var_keys:
    print("param\t" + k + "\t:=", file = f)
    for v in var_keys[k]:
        print("\t", end = "", file = f)
        for el in v:
            print(el, end = "\t", file = f)

        print(str(random.uniform(0.1, 1000000.0)), file = f)

    print(";\n", file = f)

f.close()