#%% Import required library

import tabula
from tabula import convert_into
import os
import pandas as pd
import xlsxwriter, openpyxl

# tabula.environment_info()

#%% Define Function

def handleRawTBL(inDS):
    """
    Extract table information from PDF file. Process the column names and add column CAT for SOC and PT.
    Return the whole table as pd dataframe.

    Args:
        inDS ([type]): pandas dataframe

    Returns:
        [type]: pandas dataframe
    """

    rawTBL = inDS

    # =====> For AZ PDF
    if len(rawTBL.columns) == 4 and ("Unnamed: 0" in rawTBL.columns and list(rawTBL.columns).index("Unnamed: 0")) == 1 :
        rawTBL = rawTBL.drop(["Unnamed: 0"], axis=1)

    # =====> For AZ PDF
    elif len(rawTBL.columns) == 3 and "Reaction NameTotalFatal" in rawTBL.columns :
        rawTBL = rawTBL.rename(index=str, columns={
                        "Reaction NameTotalFatal": "Reaction Name",
                        "Unnamed: 0": "Total",
                        "Unnamed: 1": "Fatal"}
                    )
    
    # =====> For BNT PDF
    if len(rawTBL.columns) == 4 and "Reaction Name" in rawTBL.columns and "Unnamed: 0" in rawTBL.columns :
        rawTBL = rawTBL.drop(["Fatal"], axis=1)
        rawTBL = rawTBL.rename(index=str, columns={
                        "Unnamed: 0": "Fatal"}
                    )

    # =====> For BNT PDF
    elif len(rawTBL.columns) == 5 and "Reaction Name" in rawTBL.columns and "Unnamed: 0" in rawTBL.columns :
        rawTBL = rawTBL.drop(["Unnamed: 0", "Fatal"], axis=1)
        rawTBL = rawTBL.rename(index=str, columns={
                        "Unnamed: 1": "Fatal"}
                    )

    handTBL = rawTBL.reset_index()
    handTBL.loc[:, "index"] = handTBL.loc[:, "index"].astype(int)

    handTBL.loc[handTBL.loc[:, "index"] == 0, "CAT"] = "SOC"
    handTBL.loc[(handTBL.loc[:, "Total"].isna()) & (handTBL.loc[:, "index"] != 0), "CAT"] = "PT"
   
    print(handTBL.shape)
    handTBL = handTBL.drop(["index"], axis=1)

    return handTBL



#%% Process Datasets for Vaccine Analysis Print (VAP) of Oxford/AZ
AZreportTBLs = tabula.read_pdf('COVID-19_vaccine_AstraZeneca_analysis_print.pdf', pages="all")

AZtbl = handleRawTBL(inDS=AZreportTBLs[0])
AZtbl["PAGEN"] = 2

for tblN in range(1, len(AZreportTBLs)) :
    AZreportTBL_sub = handleRawTBL(AZreportTBLs[tblN])
    AZreportTBL_sub["PAGEN"] = tblN + 2
    AZtbl = pd.concat([AZtbl, AZreportTBL_sub], axis=0, ignore_index=True)

# =====> Handle for PDF Display Issue
AZtbl.loc[AZtbl.loc[:, "Reaction Name"] == "Device electrical issues", "CAT"] = "PT"

AZtbl_filter = AZtbl[~AZtbl.loc[:, "Reaction Name"].str.contains("cont'd|SOC TOTAL|TOTAL REACTIONS|TOTAL REPORTS|TOTAL FATAL OUTCOME REPORTS", case=True, regex=True)]

AZtbl_filter2 = AZtbl_filter
AZtbl_filter2.loc[AZtbl_filter2.loc[:, "CAT"] == "SOC", "SOC"] = AZtbl_filter2.loc[AZtbl_filter2.loc[:, "CAT"] == "SOC", "Reaction Name"]
AZtbl_filter2.loc[:, 'SOC'] = AZtbl_filter2.loc[:, 'SOC'].fillna(method='ffill')
AZtbl_filter2.loc[AZtbl_filter2.loc[:, "CAT"] == "PT", "PT"] = AZtbl_filter2.loc[AZtbl_filter2.loc[:, "CAT"] == "PT", "Reaction Name"]
AZtbl_filter2.loc[:, 'PT'] = AZtbl_filter2.loc[:, 'PT'].fillna(method='ffill')

AZtbl_filter3 = AZtbl_filter2[AZtbl_filter2.loc[:, "CAT"].isna()]
AZtbl_filter3 = AZtbl_filter3.drop(["CAT"], axis=1)

#%% Ouput integrated data of VAP of Oxford/AZ to EXCEL
# writer = pd.ExcelWriter('Data/VaccineAnalysisPrint.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
# AZtbl_filter3.to_excel(writer, sheet_name='OxAstraZeneca', index=True)

# Close the Pandas Excel writer and output the Excel file.
# writer.save()


#%% Process Datasets for Vaccine Analysis Print (VAP) of Pfizer/BNT
PFBNTreportTBLs = tabula.read_pdf('COVID-19_mRNA_Pfizer-_BioNTech_Vaccine_Analysis_Print.pdf', pages="all")

BNTtbl = handleRawTBL(inDS=PFBNTreportTBLs[0])
BNTtbl["PAGEN"] = 2

for tblN in range(1, len(PFBNTreportTBLs)) :
    BNTreportTBL_sub = handleRawTBL(PFBNTreportTBLs[tblN])
    BNTreportTBL_sub["PAGEN"] = tblN + 2
    BNTtbl = pd.concat([BNTtbl, BNTreportTBL_sub], axis=0, ignore_index=True)

# =====> Handle for PDF Display Issue
BNTtbl.loc[BNTtbl.loc[:, "Reaction Name"] == "Device issues NEC", "CAT"] = "PT"

BNTtbl_filter = BNTtbl[~BNTtbl.loc[:, "Reaction Name"].str.contains("cont'd|SOC TOTAL|TOTAL REACTIONS|TOTAL REPORTS|TOTAL FATAL OUTCOME REPORTS", case=True, regex=True)]

BNTtbl_filter2 = BNTtbl_filter
BNTtbl_filter2.loc[BNTtbl_filter2.loc[:, "CAT"] == "SOC", "SOC"] = BNTtbl_filter2.loc[BNTtbl_filter2.loc[:, "CAT"] == "SOC", "Reaction Name"]
BNTtbl_filter2.loc[:, 'SOC'] = BNTtbl_filter2.loc[:, 'SOC'].fillna(method='ffill')
BNTtbl_filter2.loc[BNTtbl_filter2.loc[:, "CAT"] == "PT", "PT"] = BNTtbl_filter2.loc[BNTtbl_filter2.loc[:, "CAT"] == "PT", "Reaction Name"]
BNTtbl_filter2.loc[:, 'PT'] = BNTtbl_filter2.loc[:, 'PT'].fillna(method='ffill')

BNTtbl_filter3 = BNTtbl_filter2[BNTtbl_filter2.loc[:, "CAT"].isna()]
BNTtbl_filter3 = BNTtbl_filter3.drop(["CAT"], axis=1)

#%% Ouput integrated data of VAP of Pfizer/BNT to EXCEL
# writer = pd.ExcelWriter('Data/VaccineAnalysisPrint.xlsx', engine='openpyxl', mode='a')

# Convert the dataframe to an XlsxWriter Excel object.
# BNTtbl_filter3.to_excel(writer, sheet_name='PfizerBNT', index=True)

# Close the Pandas Excel writer and output the Excel file.
# writer.save()


#%% Ouput integrated data of VAP (Oxford/AZ, Pfizer/BNT) to EXCEL
writer = pd.ExcelWriter('Data/VaccineAnalysisPrint.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
AZtbl_filter3.to_excel(writer, sheet_name='OxAstraZeneca', index=True)
BNTtbl_filter3.to_excel(writer, sheet_name='PfizerBNT', index=True)

# Close the Pandas Excel writer and output the Excel file.
writer.save()