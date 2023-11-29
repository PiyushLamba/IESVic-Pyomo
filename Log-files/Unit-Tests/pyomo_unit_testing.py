"""
    This file is to perform the unit testing for the Pyomo OSeMosys Implementation
    This file could be used in future for continuous integration and testings, if
    a proper test set is been given. 

    The file will read the result from a log file called constriant_cases.log, which
    contains all output of the constraint function from a mathprog, which is guranteed
    to be a correct result.

    The test cases, are generated separately by calling MathProg/GLPK from system. At
    the moment, this was not integrated to the file yet. And is to be done in future
    work 
"""

import unittest

from pyomo_constraint_function import *

constraint_function_result_glpk_src = None
constraint_sol_dict = None

def TesterFunc(model, index, funcName):
    return funcName(model, *index)

class Pyomo_OseMosys_Constraint_Implementation_Testing(unittest.TestCase):
    def setUp(self):
        self.model = ModelConstructor("/home/mylaptop/IESVic-Pyomo-Test/test/pyomo_test.dat")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_CAa4_Constraint_Capacity(self):
        kvs = constraint_sol_dict["CAa4_Constraint_Capacity"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, CAa4_Constraint_Capacity_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            errmsg = "Error associated with " + str(key)
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                msg = errmsg
            )


    def test_CAa4b_Constraint_Capacity(self):
        kvs = constraint_sol_dict["CAa4b_Constraint_Capacity"]
        
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, CAa4b_Constraint_Capacity_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            errmsg = "Error associated with " + str(key)
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                msg = errmsg
            )

    def test_CAa5_TotalNewCapacity(self):
        kvs = constraint_sol_dict["CAa5_TotalNewCapacity"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, CAa5_TotalNewCapacity_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_CAb1_PlannedMaintenance(self):
        kvs = constraint_sol_dict["CAb1_PlannedMaintenance"]
        for key in kvs:
            values = kvs[key]


            val = TesterFunc(self.model, key, CAb1_PlannedMaintenance_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_CAb1_PlannedMaintenance_Negative(self):
        kvs = constraint_sol_dict["CAb1_PlannedMaintenance_Negative"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, CAb1_PlannedMaintenance_Negative_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_EBa10_EnergyBalanceEachTS4(self):
        kvs = constraint_sol_dict["EBa10_EnergyBalanceEachTS4"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, EBa10_EnergyBalanceEachTS4_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_EBa11_EnergyBalanceEachTS5(self):
        kvs = constraint_sol_dict["EBa11_EnergyBalanceEachTS5"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, EBa11_EnergyBalanceEachTS5_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_EBb4_EnergyBalanceEachYear4(self):
        kvs = constraint_sol_dict["EBb4_EnergyBalanceEachYear4"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, EBb4_EnergyBalanceEachYear4_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_S1_StorageLevelYearStart(self):
        kvs = constraint_sol_dict["S1_StorageLevelYearStart"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, S1_StorageLevelYearStart_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_StorageLevelTSStart(self):
        kvs = constraint_sol_dict["StorageLevelTSStart"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, S2_StorageLevelTSStart_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC8_StorageRefilling(self):
        kvs = constraint_sol_dict["SC8_StorageRefilling"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC8_StorageRefilling_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC9_StopModeLeakage(self):
        kvs = constraint_sol_dict["SC9_StopModeLeakage"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC9_StopModeLeakage_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_NonStorageConstraint(self):
        kvs = constraint_sol_dict["NonStorageConstraint"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, NonStorageConstraint_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC1_LowerLimit(self):
        kvs = constraint_sol_dict["SC1_LowerLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC1_LowerLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC1a_LowerLimitEndofModelPeriod(self):
        kvs = constraint_sol_dict["SC1a_LowerLimitEndofModelPeriod"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC1a_LowerLimitEndofModelPeriod_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC2_UpperLimit(self):
        kvs = constraint_sol_dict["SC2_UpperLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC2_UpperLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC2a_UpperLimitEndofModelPeriod(self):
        kvs = constraint_sol_dict["SC2a_UpperLimitEndofModelPeriod"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC2a_UpperLimitEndofModelPeriod_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC2a_UpperLimitEndofModelPeriod_Negative(self):
        kvs = constraint_sol_dict["SC2a_UpperLimitEndofModelPeriod_Negative"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC2a_UpperLimitEndofModelPeriod_Negative_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SC7_StorageMaxUpperLimit(self):
        kvs = constraint_sol_dict["SC7_StorageMaxUpperLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SC7_StorageMaxUpperLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SI6_SalvageValueStorageAtEndOfPeriod1(self):
        kvs = constraint_sol_dict["SI6_SalvageValueStorageAtEndOfPeriod1"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SI6_SalvageValueStorageAtEndOfPeriod1_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SI7_SalvageValueStorageAtEndOfPeriod2(self):
        kvs = constraint_sol_dict["SI7_SalvageValueStorageAtEndOfPeriod2"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SI7_SalvageValueStorageAtEndOfPeriod2_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SI8_SalvageValueStorageAtEndOfPeriod3(self):
        kvs = constraint_sol_dict["SI8_SalvageValueStorageAtEndOfPeriod3"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SI8_SalvageValueStorageAtEndOfPeriod3_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SV1_SalvageValueAtEndOfPeriod1(self):
        kvs = constraint_sol_dict["SV1_SalvageValueAtEndOfPeriod1"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SV1_SalvageValueAtEndOfPeriod1_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SV2_SalvageValueAtEndOfPeriod2(self):
        kvs = constraint_sol_dict["SV2_SalvageValueAtEndOfPeriod2"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SV2_SalvageValueAtEndOfPeriod2_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SV3_SalvageValueAtEndOfPeriod3(self):
        kvs = constraint_sol_dict["SV3_SalvageValueAtEndOfPeriod3"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SV3_SalvageValueAtEndOfPeriod3_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_SV4_SalvageValueDiscountedToStartYear(self):
        kvs = constraint_sol_dict["SV4_SalvageValueDiscountedToStartYear"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, SV4_SalvageValueDiscountedToStartYear_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_TCC1_TotalAnnualMaxCapacityConstraint(self):
        kvs = constraint_sol_dict["TCC1_TotalAnnualMaxCapacityConstraint"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, TCC1_TotalAnnualMaxCapacityConstraint_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_TCC2_TotalAnnualMinCapacityConstraint(self):
        kvs = constraint_sol_dict["TCC2_TotalAnnualMinCapacityConstraint"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, TCC2_TotalAnnualMinCapacityConstraint_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_NCC1_TotalAnnualMaxNewCapacityConstraint(self):
        kvs = constraint_sol_dict["NCC1_TotalAnnualMaxNewCapacityConstraint"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, NCC1_TotalAnnualMaxNewCapacityConstraint_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_AAC2_TotalAnnualTechnologyActivityUpperLimit(self):
        kvs = constraint_sol_dict["AAC2_TotalAnnualTechnologyActivityUpperLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, AAC2_TotalAnnualTechnologyActivityUpperLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_AAC3_TotalAnnualTechnologyActivityLowerLimit(self):
        kvs = constraint_sol_dict["AAC3_TotalAnnualTechnologyActivityLowerLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, AAC2_TotalAnnualTechnologyActivityUpperLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_TAC2_TotalModelHorizonTechnologyActivityUpperLimit(self):
        kvs = constraint_sol_dict["TAC2_TotalModelHorizonTechnologyActivityUpperLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, TAC2_TotalModelHorizonTechnologyActivityUpperLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_TAC3_TotalModelHorizenTechnologyActivityLowerLimit(self):
        kvs = constraint_sol_dict["TAC3_TotalModelHorizenTechnologyActivityLowerLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, TAC3_TotalModelHorizenTechnologyActivityLowerLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_RM3_ReserveMargin_Constraint(self):
        kvs = constraint_sol_dict["RM3_ReserveMargin_Constraint"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, RM3_ReserveMargin_Constraint_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_RE4_EnergyConstraint(self):
        kvs = constraint_sol_dict["RE4_EnergyConstraint"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, RE4_EnergyConstraint_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_E5_DiscountedEmissionsPenaltyByTechnology(self):
        kvs = constraint_sol_dict["E5_DiscountedEmissionsPenaltyByTechnology"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, E5_DiscountedEmissionsPenaltyByTechnology_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_E8_AnnualEmissionsLimit(self):
        kvs = constraint_sol_dict["E8_AnnualEmissionsLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, E8_AnnualEmissionsLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

    def test_E9_ModelPeriodEmissionsLimit(self):
        kvs = constraint_sol_dict["E9_ModelPeriodEmissionsLimit"]
        for key in kvs:
            values = kvs[key]

            val = TesterFunc(self.model, key, E9_ModelPeriodEmissionsLimit_rule)
            pyomo_result = val[0] + val[1]
            mathprog_result = values[0] + values[1]
            self.assertEqual(
                round(pyomo_result, 3), 
                round(mathprog_result, 3), 
                ("Error associated with " + str(key))
            )

if __name__ == "__main__":
    file = "/home/mylaptop/IESVic-Pyomo-Test/test/result/constraints_cases.log"

    constraint_function_result_glpk_src = open(file, "r")
    
    dict_global_tmp = dict()
    str_cur_key = str()

    for line in constraint_function_result_glpk_src:
        if "\t" in line:
            key = line[line.find("(") + 1 : line.find(")")].split("\t")
            for i in range(len(key)):
                try:
                    key[i] = int(key[i])
                except:
                    pass
            
            key = tuple(key)
            val = line.split()[-2:]
            dict_global_tmp[str_cur_key][key] = (
                float(val[0].strip(", ")), float(val[1].strip(", ")))

        else:
            str_cur_key = line[:-1]
            dict_global_tmp[str_cur_key] = dict()

    constraint_function_result_glpk_src.close()
    constraint_sol_dict = dict_global_tmp
    f = open("./view_tmp", "w")
    print(str(constraint_sol_dict), file = f)
    f.close()

    unittest.main()