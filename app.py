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
