# -*- coding: utf-8 -*-
#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import plotly.express as px

import pandas as pd
import lorem
import pathlib

import datetime

today = datetime.date.today()
tdy = str(today).replace("-", "")


#%%
# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()

#%%
## Read in data

pressLst = pd.read_excel(DATA_PATH.joinpath(f"CDC_Press List.xlsx"), keep_default_na=False, infer_datetime_format=True)
pressTDY = pressLst.loc[pressLst["YMD"] == pressLst.iloc[1, 2]]

cases = pd.read_excel(DATA_PATH.joinpath("COVID-19_TW.xlsx"), keep_default_na=False, parse_dates=[1], infer_datetime_format=True)
cases_filter = cases.loc[cases["案例"] != ""]
caseTDS = pd.crosstab(index=cases_filter["來源"], columns=["人次"], rownames=["來源"])
caseTDS.reset_index(level=0, inplace=True)
caseTDS = caseTDS.sort_values(by=["人次"], ascending=False)

caseDayTDS = pd.crosstab(index=cases_filter["新聞稿發布日期"], columns=["人次"], rownames=["確診日期"])
caseDayTDS.reset_index(level=0, inplace=True)
# caseDayTDS = caseDayTDS.sort_values(by=["人次"], ascending=False)
startDate = caseDayTDS["確診日期"][0].date()
endDate = caseDayTDS["確診日期"][caseDayTDS.shape[0]-1].date()
dateLst = pd.date_range(start=startDate, end=endDate, freq='D')
dateRangeDS = pd.DataFrame({"日期":dateLst})
caseDayDS = dateRangeDS.merge(caseDayTDS, how="left", left_on="日期", right_on="確診日期", )
caseDayDS = caseDayDS.fillna(0)
caseDayDS["累積人次"] = caseDayDS["人次"].cumsum()
caseDayDS_Melt = caseDayDS.melt(id_vars=list(caseDayDS.keys()[:2]), var_name='Subject', value_name='人次')
caseDayDS_Melt["Subject"][caseDayDS_Melt["Subject"] == "人次"] = "新增人次"

# Colours
color_1 = "#003399"
color_2 = "#00ffff"
color_3 = "#002277"
color_b = "#F8F8FF"


#%%
## Paragraph
# iniLst = [
#     html.H6(
#     "適用對象再放寬，有需求者可至指定院所自費檢驗武漢肺炎",
#     className="page-1h",
#     ),
# ]
# iniLst.extend(
#     list(item if item != "\@" else html.Br() for item in
#     ['發佈日期：2020-05-29',
#     "\@",
#     '中央流行疫情指揮中心今(29)日表示，由於國內COVID-19(武漢肺炎)疫情已趨穩定且檢驗量能日益提升，考量民眾因緊急情況、工作及出國求學等因素，而有自費檢驗武漢肺炎之需求，指揮中心再度放寬適用對象，有檢驗需求民眾，可至指定院所進行自費檢驗，以取得相關檢驗證明文件。適用對象如下：',
#     "\@",
#     '居家隔離/檢疫者，因二親等內親屬身故或重病等社會緊急需求，需外出奔喪或探視。',
#     "\@",
#     '因旅外親屬事故或重病等緊急特殊因素入境他國家/地區之民眾。',
#     "\@",
#     '因工作因素之民眾。',
#     "\@",
#     '出國求學之民眾。',
#     "\@",
#     '外國或中國大陸、香港、澳門人士出境。',
#     "\@",
#     '相關出境適用對象之眷屬。',
#     "\@",
#     '因其他因素須檢驗之民眾。',
#     "\@",
#     '指揮中心指出，自費檢驗出境之民眾，每人以3個月內申請1次為原則。為同步提升民眾自費檢驗便利性，指揮中心將自費檢驗指定醫院由原本18家增設至37家，提供符合前述適用條件之民眾進行自費檢驗，有關服務時間及收費金額請以醫院公告為準。相關申請規定公布於疾病管制署全球資訊網/嚴重特殊傳染性肺炎/醫療照護機構感染管制相關指引項下，民眾可自行參考運用。',
#     '指揮中心提醒，由於目前國際疫情仍嚴峻，依據疾管署國際旅遊疫情建議等級，全球現況皆為第三級警告(Warning)，即避免所有非必要旅遊，請民眾於出境前確實評估所赴國家/地區相關風險及是否有出境之必要，以避免因前往之國家/地區實施相關邊境封鎖等管制措施，致無法返臺。另提醒自國外返臺的民眾，須配合居家檢疫等相關防疫措施，以降低可能傳播風險，保障自己、親友及周遭人員的健康。'
#     ]
#     )
# )

# secLst = [
#     html.H6(
#     "台灣社區已相對安全，放寬精神科病房探視，各行各業依風險條件逐步調整",
#     className="page-1h",
#     ),
# ]

# secLst.extend(
#     [
#         "因應國內疫情平穩，社區內相對安全，將逐步適度放寬防疫措施。考量精神科病房平均住院天數較長，為減少病患情緒起伏，自今(25)日起，放寬精神科病房探視，辦理方式如下：實地探視採預約制，且實名(聯)登錄管理探視者的個人資料。訪客配合院方量體溫、手部清潔、詢問旅遊接觸史(TOCC)等相關感管措施。每位病人1天限探視1次，且同一時間同一探視空間原則限1組訪客，每組訪客人數最多2人，訪客與病人全程都須佩戴口罩。",
#         html.Br(),
#         "民眾前往醫院探視親友前，請務必先行向院方申請預約及確認相關事宜，並配合醫院感染管制之相關規定。",
#         html.Br(),
#         "另外有關各行各業防疫放寬標準，可參考下列原則：維持室內1.5公尺、室外1公尺之安全社交距離。配戴口罩。適當阻隔設施如隔板等。",
#         html.Br(),
#         "上述原則若能全數達成，加上實名(聯)制為最安全條件，若因場地等因素受限，至少要達成其中一項防護原則，再加上實名(聯)制進行試辦，依結果及風險條件持續調整相關防疫措施，即可逐步放寬。",
#     ]
# )


paragLst = [html.H6("疫情指揮中心 最新新聞稿", className="page-1i"),]
for pressN in range(pressTDY.shape[0]):
    iniLst = [
        html.H6(
        pressTDY.iloc[pressN, 0],
        className="page-1h",
        ),
    ]
    iniLst.extend(
        list(item if item != "\@" else html.Br() for item in
            pressTDY.iloc[pressN, 4].split("\$")
        )
    )

    if pressN % 2 == 1:
        paragLst.extend( [html.Div(iniLst, className="page-1k", )] )
    else:
        paragLst.extend( [html.Div(iniLst, className="page-1l", )] )


## Figure
fig_dayInc_scale = 150
fig_dayInc = px.line(
            caseDayDS_Melt,
            x="日期", y="人次",
            color="Subject",
            range_x=[startDate, endDate],
            title={
                    'text': "累積總人次",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
            # width= 4*fig_dayInc_scale, height= 3*fig_dayInc_scale
            )
fig_dayInc.update_xaxes(
    showgrid=True,
    tickangle=45,
    tickfont=dict(size=12),
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig_dayInc.update_layout(
    xaxis=dict(
        # tickformat = "%Y %b",
        tick0 = startDate,
        dtick = 'M1'
    ),
    xaxis_range=[ startDate, endDate ],
)
# fig_dayInc.add_scatter(x=caseDayDS['日期'], y=caseDayDS['人次'], mode='lines')

# fig_dayInc.show()


fig_src_scale = 100
fig_src = px.bar(
            caseTDS,
            x="來源", y="人次",
            text="人次",
            # labels={'來源': 'Source', '人次':'Number of Subject'},
            # title="確診人次統計",
            title={
                    'text': "確診人次統計",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
            width= 4*fig_src_scale, height= 3*fig_src_scale
            )

fig_src.layout.font = dict(family="Helvetica")
# fig.update_traces(marker_color=color_1)
fig_src.update_traces(marker_color='green', textposition='auto')


#%%
# Server
app = dash.Dash(__name__)
app.title = 'COVID-19 Information of TW'

server = app.server

app.layout = html.Div(
    children=[
        # Page 1
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    html.Img(
                                                        # src=app.get_asset_url(
                                                        #     "dash-logo-new.png"
                                                        # ),
                                                        className="page-1a",
                                                    )
                                                ),
                                                html.Div(
                                                    [
                                                        html.H6("SARS-CoV-2/COVID-19 Information"),
                                                        html.H5("新型冠狀肺炎/武漢肺炎"),
                                                        html.H6("疫情資訊"),
                                                    ],
                                                    className="page-1b",
                                                ),
                                            ],
                                            className="page-1c",
                                        )
                                    ],
                                    className="page-1d",
                                ),
                                html.Div(
                                    [
                                        html.H1(
                                            [
                                                html.Span(tdy[4:], className="page-1e"),
                                                # html.Span("19"),
                                            ]
                                        ),
                                        html.H6(tdy[0:4]),
                                    ],
                                    className="page-1f",
                                ),
                            ],
                            className="page-1g",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "嚴重特殊傳染性肺炎",
                                            className="page-1h"
                                        ),
                                        html.H6(
                                            "- 衛生福利部疾病管制署",
                                            className="page-1h"
                                        ),
                                        html.P(),
                                        html.P(html.A('官網連結', href='https://www.cdc.gov.tw/Disease/SubIndex/N6XvFa1YP9CXYdB0kNSA9A', target="_blank")),
                                    ],
                                    className="page-1i",
                                ),
                            ],
                            className="page-1j",
                        ),
                        html.Div(
                            # [
                            #     html.Div(
                            #         iniLst,
                            #         className="page-1k",
                            #     ),
                            #     html.Div(
                            #         secLst,
                            #         className="page-1l",
                            #     ),
                            # ],
                            paragLst,
                            className="page-1n",
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        ),

        # Page 2
        html.Div(
            [
                html.Div(
                    [
                        html.Div([html.H1("Status Summary (TW)")], className="page-2a"),
                        html.Div(
                            [   
                                dcc.Graph(figure=fig_dayInc)
                            ],
                            className="page-3",
                        ),
                        html.Div(
                            [   
                                # html.Strong(
                                #     "確診人次統計",
                                #     className="page-3",
                                # ),
                                dcc.Graph(figure=fig_src)
                            ],
                            className="page-3",
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        ),

    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
