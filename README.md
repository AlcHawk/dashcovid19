## dash-multipage-report

# COVID-19 Multipage Report

# Table of Content

<!-- TOC -->

- [COVID-19 Multipage Report](#covid-19-multipage-report)
- [Table of Content](#table-of-content)
- [Rerport Contents](#rerport-contents)
    - [First Page](#first-page)
    - [Second Page](#second-page)
- [System](#system)
    - [Requirements](#requirements)
    - [How to run this app](#how-to-run-this-app)
- [Resources](#resources)

<!-- /TOC -->

# Rerport Contents 
## First Page
- The latest press from TW CDC (中央疫情指揮中心 最新新聞稿)

## Second Page
- Confirmed Cases Trend of Newly Added and Cumulated in TW (個案確診人數以新增及累積人數趨勢圖)
- Frequency of Sources of Confirmed Cases in TW (個案確診來源分佈)


# System
## Requirements

* Python 3.7

## How to run this app

To run first create a virtual environment for running this app with Python 3. Clone this repository 
and open your terminal/command prompt in the root folder.

```
git clone https://github.com/AlcHawk/dashcovid19
cd dashcovid19
python3 -m virtualenv venv
```
In Unix system:
```
source venv/bin/activate
```
In Windows: 

```
venv\Scripts\activate
```

Install all required packages by running:
```
pip install -r requirements.txt
```

Run this app locally with:
```
python app.py
```

# Resources

* [Dash](https://dash.plot.ly/)
* [Dash - Multipage Report](https://dash-gallery.plotly.host/dash-multipage-report/)
