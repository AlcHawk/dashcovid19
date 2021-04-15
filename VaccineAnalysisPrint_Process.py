#%% Import required library

import tabula
from tabula import convert_into
import os
import pandas as pd
import xlsxwriter

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

    if len(rawTBL.columns) == 4 and "Unnamed: 0" in rawTBL.columns :
        rawTBL = rawTBL.drop(["Unnamed: 0"], axis=1)

    elif len(rawTBL.columns) == 3 and "Reaction NameTotalFatal" in rawTBL.columns :
        rawTBL = rawTBL.rename(index=str, columns={
                        "Reaction NameTotalFatal": "Reaction Name",
                        "Unnamed: 0": "Total",
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

for tblN in range(1, len(AZreportTBLs)) :
    AZreportTBL_sub = handleRawTBL(AZreportTBLs[tblN])
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
writer = pd.ExcelWriter('Data/VaccineAnalysisPrint.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
AZtbl_filter3.to_excel(writer, sheet_name='OxAstraZeneca', index=True)

# Close the Pandas Excel writer and output the Excel file.
writer.save()