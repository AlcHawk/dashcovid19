#%%
import requests, pyquery as pq
import pandas as pd
from io import BytesIO
from io import StringIO
import io
# import wget
import xlsxwriter, xlrd

import datetime
import time
import sys

if len(sys.argv) > 1:
    rootdir = sys.argv[1]
else:
    rootdir = "."

tdy = time.strftime("%Y%m%d")

#%% Download Integrated Data Information by Someone from Google Spreadsheet

srcUrl = 'https://docs.google.com/spreadsheets/d/1qh20J-5rGVIEjLcGKJnfj7huAp-nCxsd-fJdmh3yZKY/export?gid=0&format=xlsx'

out_fname = f'{rootdir}/Data/COVID-19_TW.xlsx'

res = requests.get(srcUrl)
res.encoding = 'utf-8'

with open(out_fname, 'wb') as f:
    f.write(res.content)


# %% Run Demo - Get Press Release List from CDC
def fetchUrlInfoDF(url):
    res = requests.get(url)
    con = pq.PyQuery(res.text)

    Next = "下一頁" in con("ul.pagination > li > a").text()

    # Get Title and Link list
    hyperlinks = con("div.content-boxes-v3 > a")

    titleLst = list(map(lambda x: pq.PyQuery(x).attr.title, hyperlinks))
    relLinkLst = list(map(lambda x: pq.PyQuery(x).attr.href, hyperlinks))

    # Get Year and Date Information
    yrMoLst = [yrMo.text for yrMo in con('div.content-boxes-v3 > a > div.icon-custom.icon-md.icon-line > p.icon-year')]
    dateLst = [date.text for date in con('div.content-boxes-v3 > a > div.icon-custom.icon-md.icon-line > p.icon-date')]
    
    urlDF = pd.DataFrame({"Press Title":titleLst, "Relative Link":relLinkLst, "Year-Month":yrMoLst, "Day":dateLst})
    # urlDF["Year"] = urlDF["Year-Month"].str.split(" - ", n=1, expand=True)[0]
    # urlDF["Month"] = urlDF["Year-Month"].str.split(" - ", n=1, expand=True)[1]

    return urlDF, Next

def fetchPageContent(url):
    res = requests.get(url)
    con = pq.PyQuery(res.text)

    urlText = con("div.news-v3-in > div").text()
    
    return urlText

def fetchTxtKW(contxt):  
    CESS_PRESS = False
    if r"中央流行疫情指揮中心" in contxt:
        CESS_PRESS = True
    elif r"指揮中心" in contxt:
        CESS_PRESS = True

    EPIDEM = False
    if r"疫情" in contxt:
        EPIDEM = True
    
    return (CESS_PRESS, EPIDEM)

# Download list
pressUrl = "https://www.cdc.gov.tw/Bulletin/List/MmgtpeidAR5Ooai4-fgHzQ"

pressDF, DFnext = fetchUrlInfoDF(url=pressUrl)

readEnd = False
urlN = 2

while readEnd == False:
    psUrl = f"https://www.cdc.gov.tw/Bulletin/List/MmgtpeidAR5Ooai4-fgHzQ?page={urlN}&startTime=2020.01.01"
    print(psUrl)

    pressTB, TBNext = fetchUrlInfoDF(url=psUrl)
    pressDF = pd.concat([pressDF, pressTB])

    if TBNext:
        urlN += 1
    else:
       readEnd = True 

# Assign and Handle list data
pressDF_handle = pressDF.reset_index(drop=True)

pressDF_handle["Year"] = list(map(int, pressDF_handle["Year-Month"].str.split(" - ", n=1, expand=True)[0]))
pressDF_handle["Month"] = list(map(int, pressDF_handle["Year-Month"].str.split(" - ", n=1, expand=True)[1]))
pressDF_handle["Day"] = list(map(int, pressDF_handle["Day"]))

pressDF_handle["YMD"] = pd.to_datetime(
    pressDF_handle.loc[:,["Year", "Month", "Day"]]
)

pressDF_handle["Full Link"] = "https://www.cdc.gov.tw" + pressDF_handle["Relative Link"]

pressDF_handle = pressDF_handle.drop(["Year-Month", "Year", "Month", "Day"], axis=1)

#%%
# Start extracting detail of press from CDC
start_time1 = datetime.datetime.now()

contentDF = pd.DataFrame(list(map(fetchPageContent, pressDF_handle["Full Link"])), columns=["Page Content Raw"])

end_time1 = datetime.datetime.now()

print(f'The execution time is {end_time1 - start_time1}')

#%%
# Merge detail with press list
pressDF_m = pressDF_handle.merge(contentDF, left_index=True, right_index=True)

pressDF_m["Page Content"] = list(map(lambda x: x.replace("\n\n", "\n").replace("\n", "\$\@\$"), pressDF_m["Page Content Raw"]))
pressDF_m_ex = pressDF_m.drop(["Page Content Raw"], axis=1)

pressDF_m_ex.to_excel(f"{rootdir}/Data/CDC_Press List.xlsx", sheet_name="Press", index=False)

# %%
