#-*- encoding: utf-8 -*-
import warnings
warnings.filterwarnings(action="ignore")
import flask
server = flask.Flask(__name__)
import pandas as pd
import json
import dash
import dash_bootstrap_components as dbc
from plotly.graph_objs import Scatter, Layout
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
from datetime import datetime
import ipywidgets as widgets
from dateutil.relativedelta import *
app = dash.Dash(server= server, external_stylesheets=[dbc.themes.UNITED])
app.title = "중소기업 속보성 지표 대시보드"
globals()["count"] = 0

color_data = pd.read_excel("color.xlsx")
data = pd.read_csv("SMB_ELEC 추출_Extract.csv")

slider_data = data[data["규모"]=="중소기업전체"][data["지역"]=="전국"][data["업종"]=="전업종"]
slider_data.reset_index(inplace=True)
for index, value in slider_data.iterrows():
    slider_data["index"][index] = index



nav = dbc.Row(style={"margin-top":"0px","text-align":"center", "margin-botoom":"0px", "padding":"0%","display":"flex"},children=[
    dbc.Col(style={"padding":"0%","vertical-align":"middle"},children=[
         html.Div(style={ "width": "1660px","height":"50px", "margin-bottom":"0px","margin-top":"0px","margin-left":"15px"}, children=[
             html.Div(["상세-전력사용량 | "],style={"text-align":"center","width":"auto", "display":"inline-block", "font-family": "나눔고딕 ExtraBold", "font-size": "27px", "line-height" : "31px", "color": "rgb(76, 70, 60)", "font-weight" : "bold", "font-style": "normal",  "margin":"0%" ,"padding-top":"7px"}),
             html.Div([f"{max(data['날짜'].unique())}"],style={"width":"auto","margin-left":"0.5%","display":"inline-block", "font-family": "나눔고딕 ExtraBold", "font-size": "21px", "line-height" : "24px", "color": "rgb(106, 97, 84)", "font-weight" : "bold", "font-style": "normal", "margin":"0%","padding-top":"7px" },
                      id = "main-title"),
         ]),
    ]),
])

datetime.strptime(max(data["날짜"].unique()), "%Y-%m-%d").date()

nav_2 = dbc.Row(style={"height":"40px","background-color":"rgb(238, 238, 238)", "width":"1670px", "border":"none","padding":"0%", "margin-left":"15px"}, children=[
    dbc.Col(style={"width":"580px","padding-top":"6px"},children=[
        dbc.RadioItems(style={"font-family" : "나눔고딕"},
                       options=[dict(label= "중소기업전체",value=0),dict(label= "중소기업_소상공인제외",value=1), dict(label="소상공인",value=2)],value=0, inline=True,className="radio", id = "radio"),
        #html.Button(style={"font-size":"12px","padding-top":"3px","padding-bottom":"0px","border":"none","background-color":"rgb(230, 228, 222)","font-weight":"bold","width":"88px","height":"28px"}, children=["중소기업전체"]),
        #html.Button(style={"display":"inline-block", "font-size":"12px","padding-top":"3px","padding-bottom":"0px","margin-left":"10px","border":"none","background-color":"rgb(230, 228, 222)","font-weight":"bold","width":"138px","height":"28px"},children=["중소기업_소상공인제외"]),
        #html.Button(style={"font-size":"12px","padding-top":"3px","padding-bottom":"0px","margin-left":"10px","border":"none","background-color":"rgb(230, 228, 222)", "font-weight":"bold","width":"88px","height":"28px"}, children=["소상공인"])
    ]),


    dbc.Col(style = {"width":"200px","padding":"0px 0px 0px 0px","text-align":"right"}, children=[
        html.Div(style={"padding-top":"8px","width":"100px","margin-left":"400px"},id="test")
    ]),
    dbc.Col(style={"transform": "scale(1)","padding":"12px 0px 0px 0px","width":"510px"},children=[
        dcc.Slider(min = min(slider_data["index"].unique()),  max =max(slider_data["index"].unique()), value= max(slider_data["index"].unique()),included=False, id = "slider"),
       #dcc.Interval(id="auto-step",interval=1*1000,n_intervals=0, max_intervals=max(slider_data["index"].unique()))
    ]),

])



KPI_title_1 =dbc.Row(style={"padding":"0%", "width":"1138px", "margin":"0px 0px 0px 0px"}, children=[
            dbc.Col(style={"padding":"0%"}, children=[
                html.Div(style={"padding-top":"6px","background-color":"rgb(75,70, 61)", "text-align":"center","width":"100%","height":" 30px","margin-bottom":"0%","margin-top":"0%","margin-left":"0%","margin-right":"0%", "border-left": "1px solid", "border-right":"1px solid", "border-radius":"10px 10px 0px 0px"}, children=[
                    html.Div(style={"font-family":'나눔고딕',"font-size":"15px","line-height":"18px","color":"#ffffff", "font-weight":"bold", "font-style":"normal","margin-bottom":"0%","margin-top":"0px","margin-left":"0%","margin-right":"0%"},id="title3")
                ])
            ])
        ])

KPI_1 = dbc.Row(style={"padding":"0%","width":"1138px","height":"90px","border" : "1px solid", "margin-left":"0px", "margin-right":"0px", "border-radius":"0px 0px 10px 10px", "background-color":"rgb(255, 255, 255)"}, children=[
            dbc.Col(style={"padding":"0%", "width":"1138px","display":"flex","align-items":"center", "border-radius": "0px 0px 10px 10px"}, children=[
                html.Div(style={"float":"left", "width":"281px","text-align" : "center","padding-top":"10px","height":"90px","border-radius": "10px 10px 10px 0px"}, children=[
                        html.Img(style={"text-align" : "center", "height":"70px", "verticla-algin":"middle"}, src=app.get_asset_url("home.png"))]),
                html.Div(style={"float":"left","text-align" : "center", "width":"281px","height":"45px"}, children=[
                    html.H1(f"{data['Metric'].unique()[0]}",style={"margin-bottom":"0%","font-family":'나눔고딕','font-weight':'bold','text-align':'center', "font-size": "20px"}),
                    html.H1(style={"margin-bottom":"0%","font-family":'나눔고딕','font-weight':'bold','text-align':'center', "font-size": "20px"},id="kpi_1")]),
                html.Div(style={"float":"left","text-align" : "center", "width":"281px","height":"45px"}, children=[
                    html.H1(id="kpi_2"),
                    html.Div(style={"height":"5px"}),
                    html.H1("전년 동월 대비 증감률", style={"margin-bottom":"0%","font-family":'나눔고딕', 'text-align': 'center', "font-size": "13px","vertical-align":"middle"}, id="kpi_title1")]),
                html.Div(style={"float": "left", "text-align": "center", "width":"281px","height":"45px"}, children=[
                    html.H1(id="kpi_3"),
                    html.Div(style={"height":"5px"}),
                    html.H1("전월 대비 증감률", style={"margin-bottom":"0%","font-family":'나눔고딕', 'text-align': 'center', "font-size": "13px"}, id = "kpi_title2")
           ]),
   ]),

 ])



cards = dbc.Row(style={"padding":"0%", "width":"1138px", "margin":"0px 0px 0px 0px","height":"116px"}, children=[
                dbc.Col(style={"padding":"0%", "border":"1px solid", "background-color":"rgb(255, 255, 255)"}, children=[
                        dbc.Row(style={"margin":"0px"},children=[
                            html.Div([f"전년 동월 대비 증감"],style={ "font-family":'나눔고딕',"font-size":"15px","color":"#ffffff", "font-weight":"bold", "font-style":"normal","background-color":"rgb(75,70, 61)", "text-align":"center","height":"30px","padding":"3px 0px 0px 0px"})]),
                            html.Div(style={"float":"left","text-align" : "center","width":"50%","height":"80px","padding":"10px 0px 0px 0px"}, children=[
                                html.H1("최대 상승", style={'font-weight': 'bold', 'text-align': 'center', "font-size": "13px","margin-bottom":"0%"}, id = "kpi_title3"),
                                html.H1(style={'font-weight': 'bold', 'text-align': 'center', "font-size": "20px", "margin-bottom":"0%"}, id="kpi_4"),
                                html.H1(id="kpi_5")]),
                            html.Div(style={"float": "left", "text-align": "center","width":"50%","height":"80px","padding":"10px 0px 0px 0px"}, children=[
                                html.H1("최대 감소", style={'font-weight': 'bold', 'text-align': 'center', "font-size": "13px","margin-bottom":"0%"}, id = "kpi_title4"),
                                html.H1( style={'font-weight': 'bold', 'text-align': 'center', "font-size": "20px", "margin-bottom":"0%"},id="kpi_6"),
                                html.H1( id="kpi_7")]),
                ]),
    dbc.Card(style={"width":"5px","display": 'inline-block',"padding":"0%", "border":"none","background-color":"rgb(231, 228, 221)","height":"116px"}, children=[
        dbc.CardBody([

        ])
    ]),
    dbc.Col(style={"padding":"0%","margin-bottom":"0%","margin-top":"0%","margin-left":"0%","margin-right":"0%", "height":"116px", "border":"1px solid", "background-color":"rgb(255, 255, 255)"}, children=[
        dbc.Row([
                        html.Div([f"전월 대비 증감"],style={ "font-family":'나눔고딕',"font-size":"15px","color":"#ffffff", "font-weight":"bold", "font-style":"normal","background-color":"rgb(75,70, 61)", "text-align":"center","width":"100%","height":"30px","padding":"3px 0px 0px 0px"})]),
                        html.Div(style={"float":"left","text-align" : "center","width":"50%","height":"80px","padding":"10px 0px 0px 0px"}, children=[
                            html.H1("최대 증가", style={'font-weight': 'bold', 'text-align': 'center', "font-size": "13px","margin-bottom":"0%"}, id = "kpi_title5"),
                            html.H1( style={'font-weight': 'bold', 'text-align': 'center', "font-size": "20px", "margin-bottom":"0%"},id="kpi_8"),
                            html.H1(id="kpi_9")]),
                        html.Div(style={"float": "left", "text-align": "center","width":"50%","height":"80px","padding":"10px 0px 0px 0px"}, children=[
                            html.H1("최대 감소", style={'font-weight': 'bold', 'text-align': 'center', "font-size": "13px","margin-bottom":"0%"}, id = "kpi_title6"),
                            html.H1( style={'font-weight': 'bold', 'text-align': 'center', "font-size": "20px", "margin-bottom":"0%"},id="kpi_10"),
                            html.H1( id="kpi_11")]),
                        ]),
                ])

#options_1 = ["업종기준", "내림차순"]

card_2 = dbc.Row(style={"padding":"0%", "width":"1138px", "margin":"0px 0px 0px 0px", "height":"506px", "background-color":"rgb(255, 255, 255)"}, children=[
                dbc.Col(style={"padding":"0%", "width":"563px", "border":"1px solid","height":"506px"}, children=[
                    html.Div(style={"background-color":"rgb(75,70, 61)", "text-align":"center","padding":"0%"}, children=[
                        html.Button(["선택 취소"],style={"float":"right", "font-size":"11px","width":"94px","height":"24px","margin-top":"3px"},id="reset1"),
                        html.Div([f"전력사용량 현황(지역별)"],style={ "font-family":'나눔고딕',"font-size":"15px","color":"#ffffff", "font-weight":"bold", "font-style":"normal","margin-bottom":"0%","margin-top":"0px","margin-left":"94px","margin-right":"0%","height":"30px","padding-top":"3px"}),

                        html.Div([f"전년동월대비증감률"],style={"font-family":'나눔고딕',"font-size":"12px","color":"#000000", "font-weight":"bold", "font-style":"normal","text-decoration":"none","background-color":"rgb(238, 238, 238)","height":"30px","padding-top":"6px"}),
                        html.Div(style={"float":"left","text-align" : "center", "height":"321px",}, children=[
                            dbc.Row(style={"margin":"0px 0px 0px 0px"},children=[
                                html.Div(style={"padding": "0%", "width":"373px","height":"321px"}, children=[
                                    dbc.Col(style={"padding": "0%", }, children=[
                                        html.Div([dcc.Graph(id="map",config={'displayModeBar':False})])
                                    ])
                                ]),
                                html.Div(style={"padding": "0%", "height":"321px", "width":"150px"}, children=[
                                    dbc.Col(style={"padding": "0%"}, children=[
                                        html.Div([dcc.Graph(id="table1",config={'displayModeBar':False})])
                                    ])
                                ])
                            ]),
                            dbc.Row(style={"margin":"0px 0px 0px 0px"},children=[
                            html.Div(style={"font-family": '나눔고딕', "font-size": "12px", "line-height": "18px", "color": "#000000", "font-weight": "bold", "font-style": "normal",
                                                                               "text-decoration": "none", "background-color": "rgb(255, 255, 255)","text-align":"left","padding":"0%"}, id="title1" )]),
                            dbc.Row(style={"margin":"0px 0px 0px 0px"},children=[
                                html.Div(style={"padding": "0%"}, children=[
                                    dbc.Col([
                                        html.Div([dcc.Graph(id="bargraph1",config={'displayModeBar':False})])
                            ])
                        ])
                            ]),
                        ]),
                    ]),
                ]),
    dbc.Card(style={"width":"5px","display": 'inline-block',"padding":"0%", "border":"none","background-color":"rgb(231, 228, 221)"}, children=[
        dbc.CardBody([

        ])
    ]),
    dbc.Col(style={"padding":"0%","margin-bottom":"0%","margin-top":"0%","margin-left":"0%","margin-right":"0%","border":"1px solid","height":"506px"}, children=[
                    html.Div(style={"background-color":"rgb(75,70, 61)", "text-align":"center"}, children=[
                        dcc.Dropdown(options=[{"label":'업종기준',"value":'업종기준'},{"label":'내림차순',"value":'내림차순'}], placeholder="정렬기준",id='sort',style={"text-align":"center","font-weight":"bold","width":"94px","float":"left", "padding-top":"3px", "font-size":"11px", "size":"sm", "height":"24px","display":"inline-block"}),
                        html.Button(["선택 취소"],style={"float": "right", "font-size": "11px", "width": "94px", "height": "24px","margin-top": "3px"}, id="reset2"),
                        html.Div([f"전력사용량 현황(업종별)"],style={  "font-family":'나눔고딕',"font-size":"15px","color":"#ffffff", "font-weight":"bold", "font-style":"normal","margin-bottom":"0%","margin-top":"0px","margin-left":"94px","margin-right":"0%","height":"30px","padding-top":"3px"}),
                        dbc.Row(style={"float":"left","padding":"0%", "margin":"0% 0% 0% 0%"},children=[
                            html.Div(style={"width":"430px","font-family":'나눔고딕',"font-size":"12px","color":"#000000", "font-weight":"bold", "font-style":"normal","text-decoration":"none","background-color":"rgb(238, 238, 238)","height":"30px","padding-top":"6px"},
                                     id="title2"),
                            html.Div(style={"background-color":"rgb(255,255,255)","padding":"0%","width":"2.5px"}),
                            html.Div([f"전년 동월 대비 증감률"],style={"width":"130px","font-family":'나눔고딕',"font-size":"12px","color":"#000000", "font-weight":"bold", "font-style":"normal","background-color":"rgb(238, 238, 238)","text-align":"center","height":"30px","padding-top":"6px","padding-left":"0px","padding-right":'0px'}),
                        ]),
html.Div(style={"float":"left","text-align" : "center"}, children=[
                        dbc.Row(style={"margin":"0px 0px 0px 0px","float":"left","text-align" : "center"}, children=[
                            html.Div(style={"padding": "0%","height":"442px", "width":"430px"}, children=[
                                dbc.Col(style={"padding": "0%", }, children=[
                                dcc.Graph(id="bargraph2",config={'displayModeBar':False})])]),
                            #html.Div(style={"background-color":"rgb(255,255,255)","padding":"0%","width":"2.5px", "marg}),
                            html.Div(style={"padding": "0%","height":"442px","width":"130px"}, children=[
                                dbc.Col(style={"padding": "0%", }, children=[
                            dcc.Graph(id="table2",config={'displayModeBar':False})])])
                        ]),
                    ]),
                ])
])
    ])

card_3 = dbc.Row(style={"padding":"0%", "width":"523px", "margin":"0px 0px 0px 0px", "height":"504px"}, children=[
    dbc.Col(style={"padding": "0%", "width": "523px", "height":"504px"}, children=[
        html.Div(style={"background-color": "rgb(75,70, 61)", "text-align": "center", "padding": "0%", "height":"30px"},children=[
            html.Button(["이전년도 보기"],style={"float":"right", "font-size":"11px","width":"94px","height":"24px","margin-top":"3px"},id="return"),
            html.Div([f"전력사용량 추세"],style={ "font-family":'나눔고딕',"font-size":"15px","color":"#ffffff", "font-weight":"bold", "font-style":"normal","text-decoration":"none", "height":"30px","padding":"3px 0px 0px 0px","margin-left":"94px"}),
            dbc.Row(style={"background-color": "rgb(238, 238, 238)", "margin-left":"0px","margin-right":"0px"},children=[
                html.Div(style={"width":"140px", "padding":"0px"}),
                html.Div(['■'],style={"width":"70.75px","margin":"0px 0px 0px 0px","text-align":"right"}, id="line_title_1"),
                html.Div(style={"width":"70.75px","margin":"0px 0px 0px 0px","text-align":"left","font-size":"12px","padding-left":"0px", "padding-top":"6px"}, id="line_title_2"),
                html.Div(['■'],style={"width":"70.75px","margin":"0px 0px 0px 0px","text-align":"right"}, id="line_title_3"),
                html.Div(style={"width":"70.75px","margin":"0px 0px 0px 0px","text-align":"left","font-size":"12px","padding-left":"0px", "padding-top":"6px"}, id="line_title_4"),
                html.Div([f"[단위 : GWh]"],style={"float":"left","width":"100px","font-family": '나눔고딕', "font-size": "12px", "height": "30px", "color": "#000000", "font-style": "normal", "text-decoration": "none","background-color": "rgb(238, 238, 238)","padding":"3px 0px 0px 0px"})]),
            dcc.Graph(id="linegraph1",config={"displaylogo":False}),
            html.Div([f"전년 동월 대비 증감률"],style={"font-family": '나눔고딕', "font-size": "12px", "height": "30px", "color": "#000000","font-weight": "bold", "font-style": "normal", "text-decoration": "none","background-color": "rgb(238, 238, 238)","padding":"6px 0px 0px 0px"}),
            dcc.Graph(id="bargraph3",config={"displaylogo":False}),
            html.Div([f"전월 대비 증감률"],style={"font-family": '나눔고딕', "font-size": "12px", "height": "30px", "color": "#000000","font-weight": "bold", "font-style": "normal", "text-decoration": "none","background-color": "rgb(238, 238, 238)","padding":"6px 0px 0px 0px"}),
            dcc.Graph(id="bargraph4",config={"displaylogo":False})

])
        ])
    ])










app.layout = dbc.Container(style={"width":"1700px", "height":"905px","padding":"0%","background-color":"rgb(231, 228, 221)"}, children=[
    dbc.Row(style={"margin":"0% 0% 0% 0%"},children=[nav]),
    dbc.Row(style={"margin":"0% 0% 0% 0%"},children=[nav_2]),
    dbc.Row(style={"margin":"0% 0% 0% 0%","height":"15px"}, children=[]),
    dbc.Row(style={"margin":"0% 0% 0% 0%","float":"left","width":"1700px","height":"755px","background-color":"rgb(231, 228, 221)"},children=[
        dbc.Card(style={"padding":"0%", "margin-left":"15px",  "width":"1138px","height":"755px", "border-radius" : "10px 10px 0px 0px","background-color":"rgb(231, 228, 221)","border":"none"}, children=[
                KPI_title_1,
                KPI_1,
            dbc.Row(style={"margin":"0px 0px 0px 0px"},children=[
                dbc.Card(style={"height":"5px", "padding":"0%", "border":"none"}, children=[
                    dbc.CardBody(style={"height":"5px","margin-left":"0px 0px 0px 0px", "padding":"0%","background-color":"rgb(231, 228, 221)"})
                ])
            ]),
            dbc.Row(style={"margin":"0px 0px 0px 0px"},children=[cards]),
            dbc.Row(style={"margin": "0px 0px 0px 0px"}, children=[
                dbc.Card(style={"height": "5px", "padding": "0%", "border": "none"}, children=[
                    dbc.CardBody(style={"height": "5px", "margin-left": "0px 0px 0px 0px", "padding": "0%", "background-color": "rgb(231, 228, 221)"})
                ])
            ]),
            dbc.Row(style={"margin":"0px 0px 0px 0px"},children=[card_2]),
        ]),
        dbc.Card(style={"width":'10px',"height":'755px',"background-color": "rgb(231, 228, 221)", "border":"none","display":"inline-block","padding":"0%"}, children=[
        ]),
        dbc.Card(style={"padding":"0%", "width":"525px","height":"755px", "display":"inline-block", "border":"1px solid",}, children=[card_3])
    ]),
    dbc.Row(style={"position":"relative","height":"50px"}, children=[
    html.Div(style={"position":"absolute","bottom":"0px", "margin-left":"15px"}, children=[
        html.H4("출처 : 한국전력의 데이터를 중소벤처기업연구원에서 제공", style={"font-size":"11px", "font" : "나눔고딕","margin-bottom":"0px","font-weight":"bold"}),
        html.H4("주 : 전력사용량 통계는 중소벤처기업부가 중소기업 전력사용량을 파악하기 위해 조사 분석한 통계로 통계법에 따른 국가승인통게가 아님을 밝힙니다.", style={"font-size":"11px", "font" : "나눔고딕","font-weight":"bold"})
    ])
    ]),

],fluid=True)


@app.callback([Output("return","children"),
               Output("main-title","children"),
               Output("test","children"),
               Output("kpi_1","children"),
               Output("kpi_2","children"),
               Output("kpi_3","children"),
               Output("kpi_4","children"),
               Output("kpi_5","children"),
               Output("kpi_6","children"),
               Output("kpi_7","children"),
               Output("kpi_8","children"),
               Output("kpi_9","children"),
               Output("kpi_10","children"),
               Output("kpi_11","children"),
               Output("line_title_1","style"),
               Output("line_title_2","children"),
               Output("line_title_3","style"),
               Output("line_title_4","children"),
               Output("bargraph1","figure"),
               Output("bargraph2","figure"),
               Output("bargraph3","figure"),
               Output("bargraph4","figure"),
               Output("linegraph1","figure"),
               Output("table1","figure"),
               Output("table2","figure"),
               Output("map","figure"),
               Output("kpi_2","style"),
               Output("kpi_3","style"),
               Output("kpi_5","style"),
               Output("kpi_7","style"),
               Output("kpi_9","style"),
               Output("kpi_11","style"),
               Output("kpi_title1","children"),
               Output("kpi_title2","children"),
               Output("kpi_title3","children"),
               Output("kpi_title4","children"),
               Output("kpi_title5","children"),
               Output("kpi_title6","children"),
               Output("title1","children"),
               Output("title2","children"),
               Output("title3","children"),
               Output("map","clickData"),
               Output("bargraph2","clickData"),
               Output("reset1","n_clicks"),
               Output("reset2","n_clicks"),
                #Output("slider","value"),
# Output("slider","min"),
# Output("slider","max")


],


              [Input("radio", "value"),
               Input("map","clickData"),
               Input("slider","value")],
              Input("bargraph2","clickData"),
              Input("reset1","n_clicks"),
              Input("reset2","n_clicks"),
              Input("return","n_clicks"),
              Input("sort","value"),
              # Input("auto-step","n_intervals")

)


def update(change, clickData, value, clickData2, n_clicks1, n_clicks2, n_clicks3, sort,): #auto):

    if change == 0:
        radio = "중소기업전체"
    elif change ==1 :
        radio = "중소기업_소상공인제외"
    elif change == 2 :
        radio  = '소상공인'




    dddd = slider_data["날짜"][value]

    ctx = dash.callback_context


    if clickData is None :
        map_dt = "전국"

    elif clickData is not None :
        map_dt = ctx.inputs["map.clickData"]["points"][0]["location"]


    if clickData2 is None :
        ids = "전업종"


    elif clickData2 is not None:
        ids = clickData2["points"][0]["label"]


    try :
        if n_clicks1 > 0 :
            map_dt="전국"
            clickData = None
            n_clicks1 = 0
    except TypeError:
        pass

    try :
        if n_clicks2 > 0:
            ids = "전업종"
            clickData2 = None
            n_clicks2 = 0
    except TypeError:
        pass




    try :
        if n_clicks3 % 2 == 1:

            dddd_line = datetime.strftime(datetime.strptime(dddd, "%Y-%m-%d").date() + relativedelta(years=-1),"%Y-%m-%d")
            dddd_line = str(dddd_line[:5]) + "12" + str(dddd_line[7:])
            return_title = "돌아가기"

        elif n_clicks3 == 0 or n_clicks3 % 2 == 0:
            n_clicks3 = 0
            dddd_line = dddd
            return_title = "이전년도 보기"
    except TypeError :
        n_clicks3 = 0
        dddd_line = dddd
        return_title = "이전년도 보기"


    if sort == "업종기준":
        sort_data = "코드랭크"
        asc = False
        asc_2 = True
    elif sort == "내림차순":
        sort_data =  "Value"
        asc = True
        asc_2 = False
    else:
        sort_data="코드랭크"
        asc = False
        asc_2 = True

    #
    # if auto is None :
    #     v = max(slider_data["index"].unique())
    #     mi = min(slider_data["index"].unique())
    #     ma = max(slider_data["index"].unique())
    #     print(v)
    #     print(auto)
    # elif auto == 65:
    #     #auto = None
    #     #v = 65
    #     #auto = 0
    #     v = slider_data["index"].unique()[value]
    #     mi = min(slider_data["index"].unique())
    #     ma = max(slider_data["index"].unique())
    #
    # else :
    #     v = (auto)%max(slider_data["index"].unique())+1
    #     mi = min(slider_data["index"].unique())
    #     ma = max(slider_data["index"].unique())
    #     print(v)
    #     print(auto)
    #





    data_all = data[data["geo_region"] == map_dt][data["업종"] == ids]

    max_date_data = data_all[data_all["날짜"] == dddd].reset_index(drop=True)

    now = datetime.strptime(dddd, "%Y-%m-%d").date()
    last = now + relativedelta(years=-1)
    last = datetime.strftime(last, "%Y-%m-%d")
    last_date_data = data_all[data_all["날짜"] == last].reset_index(drop=True)

    if dddd > "2017-12-01" :
        last_year_up = round((max_date_data[max_date_data['규모'] == radio].sum()['Value'] / 1000), 2) - round((last_date_data[last_date_data['규모'] == radio].sum()['Value'] / 1000), 2)
        last_year_up = str(round((last_year_up / round((last_date_data[last_date_data['규모'] == radio].sum()['Value'] / 1000), 1)) * 100, 2)) + "%"
        kpi_title_1 = "전년 동월 대비 증감률"
    else:
        last_year_up = ""
        kpi_title_1 = ""

    if last_year_up >= "0":
        last_color = "rgb(217, 97, 111)"
        pm = "+"
    else:
        last_color = "rgb(89, 147, 201)"
        pm = ""

    last_month = now + relativedelta(months=-1)
    last_month = datetime.strftime(last_month, "%Y-%m-%d")
    last_month_data = data_all[data_all["날짜"] == last_month].reset_index(drop=True)

    if dddd > "2017-01-01":
        last_month_up = round((max_date_data[max_date_data['규모'] == radio].sum()['Value'] / 1000), 2) - round((last_month_data[last_month_data['규모'] == radio].sum()['Value'] / 1000), 2)
        last_month_up = str(round((last_month_up / round((last_month_data[last_month_data['규모'] == radio].sum()['Value'] / 1000), 1)) * 100, 2)) + "%"
        kpi_title_2 = "전월 대비 증감률"

    else:
        last_month_up = ""
        kpi_title_2 = ""

    if last_month_up >= "0":
        last_month_color = "rgb(217, 97, 111)"
        m_pm = "+"
    else:
        last_month_color = "rgb(89, 147, 201)"
        m_pm = ""

    data_kr = data[data["geo_region"] == map_dt][data["규모"] == radio]
    max_date_data_kr = data_kr[data_kr["날짜"] == dddd].reset_index(drop=True)

    now_kr = datetime.strptime(dddd, "%Y-%m-%d").date()
    last_year_kr = now_kr + relativedelta(years=-1)
    last_year_kr = datetime.strftime(last_year_kr, "%Y-%m-%d")
    last_year_data_kr = data_kr[data_kr["날짜"] == last_year_kr].reset_index(drop=True)

    data_kr_year = pd.merge(max_date_data_kr, last_year_data_kr, on="업종")
    data_kr_year["전년동월대비"] = data_kr_year["Value_x"] - data_kr_year["Value_y"]
    data_kr_year["전년대비증감률"] = (data_kr_year["Value_x"] - data_kr_year["Value_y"]) / data_kr_year["Value_y"] * 100
    data_kr_year = data_kr_year[["Metric_x", "업종", "Value_x", "Value_y", "전년동월대비", "전년대비증감률"]]

    data_kr_year = data_kr_year[data_kr_year["업종"] != "전업종"]

    now_kr = datetime.strptime(dddd, "%Y-%m-%d").date()
    last_month_kr = now_kr + relativedelta(months=-1)
    last_month_kr = datetime.strftime(last_month_kr, "%Y-%m-%d")
    last_month_data_kr = data_kr[data_kr["날짜"] == last_month_kr].reset_index(drop=True)

    data_kr_month = pd.merge(max_date_data_kr, last_month_data_kr, on="업종")
    data_kr_month["전월대비"] = data_kr_month["Value_x"] - data_kr_month["Value_y"]
    data_kr_month["전월대비증감률"] = (data_kr_month["Value_x"] - data_kr_month["Value_y"]) / data_kr_month["Value_y"] * 100
    data_kr_month = data_kr_month[["Metric_x", "업종", "Value_x", "Value_y", "전월대비","전월대비증감률"]]

    data_kr_month = data_kr_month[data_kr_month["업종"] != "전업종"]

    map_data = data[data["지역"] != "전국"][data["업종"] == ids][data["규모"] == radio][
        data["날짜"] == dddd].reset_index(drop=True)

    geo = json.load(open("korea_geojson2.geojson", encoding="utf-8"))
    for x in geo['features']:
        x['id'] = x["properties"]['CTP_KOR_NM']

    color_scale = ("rgb(108, 62, 94)", "rgb(214, 212, 213)", "rgb(221, 102, 95)")

    zmin = min(map_data["전년동월증감률"])
    zmax = max(map_data["전년동월증감률"])
    if zmax > 0:
        z0 = 0
    else:
        z0 = max(map_data["전년동월증감률"])

    if dddd > "2017-12-01":
        max_lastyear = str(format(data_kr_year.loc[data_kr_year['전년동월대비'].idxmax()]['전년동월대비'],',')) + "MWh"
        min_lastyear = str(format(data_kr_year.loc[data_kr_year['전년동월대비'].idxmin()]['전년동월대비'],',')) + "MWh"
        text_max_year = data_kr_year.loc[data_kr_year['전년동월대비'].idxmax()]['업종']
        text_min_year = data_kr_year.loc[data_kr_year['전년동월대비'].idxmin()]['업종']
        kpi_title_3 = "최대 증가"
        kpi_title_4 = "최대 감소"

    else:
        max_lastyear=""
        min_lastyear=""
        text_max_year =""
        text_min_year = ""
        kpi_title_3 = ""
        kpi_title_4 = ""


    if max_lastyear >= "0":
        max_lastyear_color = "rgb(217, 97, 111)"
        max_year_pm = "+"
    elif max_lastyear < "0":
        max_lastyear_color = "rgb(89, 147, 201)"
        max_year_pm = ""
    else :
        max_lastyear_color = "rgb(255, 255, 255)"
        max_year_pm = ""

    if min_lastyear >= "0":
        min_lastyear_color = "rgb(217, 97, 111)"
        min_year_pm = "+"
    elif min_lastyear < "0":
        min_lastyear_color = "rgb(89, 147, 201)"
        min_year_pm = ""

    if dddd > "2017-01-01":
        max_lastmonth = str(format(data_kr_month.loc[data_kr_month['전월대비증감률'].idxmax()]['전월대비'],','))+ "MWh"
        min_lastmonth = str(format(data_kr_month.loc[data_kr_month['전월대비증감률'].idxmin()]['전월대비'],','))+ "MWh"
        text_max_month = data_kr_month.loc[data_kr_month['전월대비증감률'].idxmax()]['업종']
        text_min_month = data_kr_month.loc[data_kr_month['전월대비증감률'].idxmin()]['업종']
        kpi_title_5 = "최대 증가"
        kpi_title_6 = "최대 감소"


    else:
        max_lastmonth=""
        min_lastmonth=""
        text_max_month =""
        text_min_month = ""
        kpi_title_5 = ""
        kpi_title_6 = ""



    if max_lastmonth >= "0":
        max_lastmonth_color = "rgb(217, 97, 111)"
        max_month_pm = "+"
    elif max_lastmonth < "0":
        max_lastmonth_color = "rgb(89, 147, 201)"
        max_month_pm = ""
    if min_lastmonth >= "0":
        min_lastmonth_color = "rgb(217, 97, 111)"
        min_month_pm = "+"
    elif min_lastmonth < "0":
        min_lastmonth_color = "rgb(89, 147, 201)"
        min_month_pm = ""


# 맵차트
    map_data = map_data.fillna(0)

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geo,
        locations=map_data.geo_region,
        featureidkey="id",
        z=round(map_data.전년동월증감률, 2),
        text="시도명 ",
        hoverinfo="text+location", showscale=False, showlegend=True, colorscale=color_scale, zmin=zmin, zmax=zmax,
        zmid=z0,
        name=""

    ))

    fig.update_layout(width=373, height=321, mapbox_style="white-bg", mapbox_zoom=5,
                      mapbox_center={"lat": 35.757981, "lon": 127.661132},
                      mapbox_layers=[{"below": "traces", "sourcetype": "raster", "source": [
                          "https://api.vworld.kr/req/wmts/1.0.0/DE397ADA-C03E-3476-8C97-341F3DFCA328/gray/{z}/{y}/{x}.png"],
                                      "opacity": 0.3}],
                      showlegend=True,
                      mapbox_accesstoken="pk.eyJ1Ijoid2pzcXVkZG4iLCJhIjoiY2t3Mnc1YXd6MGpmdDJwcDZqa2ZtNW0yayJ9.TEQ51RPJX8z5bZEUyW5h5w",
                      # shapes=[{"x0": 0,"y0": 0,"x1": 1,"y1": 1,}],
                      margin=dict(l=0, t=0, b=0, r=0),
                      legend=dict(yanchor="top", y=0.1, xanchor="right", itemsizing="trace", itemwidth=100,
                                  bgcolor="rgba(0,0,0,0)")
                      )

    # 지역 바 차트
    map_data = data[data["지역"] != "전국"][data["업종"] == ids][data["규모"] == radio][
        data["날짜"] == dddd].reset_index(drop=True)

    map_data = map_data.sort_values(by=["sd cd"])

    map_data["text"] = np.nan
    for index, value in map_data.iterrows():
        map_data["text"][
            index] = f"{dddd}{map_data['지역'][index]}의 전력 사용량 합계는 {round(map_data['Value'][index] / 1000, 1)} Gwh입니다."

    fig_bar = go.Figure(go.Bar(
        x=map_data["지역"],
        y=round(map_data["Value"] / 1000, 1),
        marker=dict(color="rgb(128, 124, 118)"),
        text=round(map_data["Value"] / 1000, 1),
        textposition='outside',
        hoverinfo="text",
        hovertext=map_data.text

    ))

    fig_bar_layout = go.Layout(margin=go.layout.Margin(
        l=0,
        r=0,
        b=0
        , t=0
    ), plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(visible=False), width=563, height=92)

    fig_bar.update_layout(fig_bar_layout)
    # fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)',yaxis=dict(visible= False))

    # 업종 바 차트
    bar_data = data[data["geo_region"] == map_dt][data["업종"] != "전업종"][data["규모"] == radio][data["날짜"] == dddd].reset_index(drop=True)
    bar_data = pd.merge(bar_data, color_data, on="업종")




    bar_data = bar_data.sort_values(by=[sort_data], ascending=asc)

    bar_date_2 = bar_data.copy()

    bar_data["text"] = np.nan
    for index, value in bar_data.iterrows():
        bar_data["text"][
            index] = f"{dddd}{bar_data['업종'][index]}의 전력 사용량 합계는 {round(bar_data['Value'][index] / 1000, 1)} Gwh입니다."

    if dddd_line == "2017-01-01":
        bar_data = bar_data.sort_values(by=[sort_data], ascending=asc, ignore_index=True)


    fig_bar_2 = go.Figure(go.Bar(
        y=bar_data["업종"],
        yaxis="y2",
        x=round(bar_data["Value"] / 1000, 1),
        marker=dict(color=bar_data["colorX"]),
        text=round(bar_data["Value"] / 1000, 1),
        textposition='auto',
        orientation="h", textfont=dict(family="나눔고딕"),
        hoverinfo="text",
        hovertext=bar_data.text

    ))

    fig_bar_2_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False, domain=[0.32, 1]),
                                 yaxis2=dict(position=0.02, side="right"), margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                                 height=442, width=420)






    fig_bar_2.update_layout(fig_bar_2_layout)

    # 업종 바 차트 테이블
    if dddd > "2017-12-01":
        bar_table_data = bar_date_2.sort_values(by=[sort_data], ascending=asc_2)

        bar_table_data["전년동월증감률"] = round(bar_table_data["전년동월증감률"], 2)
        bar_table_data = bar_table_data[bar_table_data["날짜"] > "2017-12-01"]
        bar_table_data["color"] = np.nan
        bar_table_data["증감"] = np.nan
        for index, values in bar_table_data.iterrows():
            if bar_table_data["전년동월증감률"][index] > 0:
                bar_table_data["color"][index] = "rgb(217, 97, 111)"
                bar_table_data["증감"][index] = "+"
            elif bar_table_data["전년동월증감률"][index] < 0 :
                bar_table_data["color"][index] = "rgb(89, 147, 201)"
                bar_table_data["증감"][index] = "-"
            else :
                bar_table_data["color"][index] = "rgb(89, 147, 201)"
                bar_table_data["증감"][index] = ""
            bar_table_data["전년동월증감률"][index] = str(abs(bar_table_data["전년동월증감률"][index])) + "%"


        cols_to_show_2 = ["증감", "전년동월증감률"]

        bar_data_color = []
        n = len(bar_table_data)
        for col in cols_to_show_2:
            if col == "지역":
                bar_data_color.append(["black"] * n)
            else:
                bar_data_color.append(bar_table_data["color"].tolist())



        fig_table_bar = go.Figure([go.Table(
            header=dict(values=[bar_table_data.증감, bar_table_data.전년동월증감률],
                        fill_color="white",
                        align=['right', 'left'],
                        font=dict(size=1, color="white"),
                        height=0),
            cells=dict(values=[bar_table_data.증감, bar_table_data.전년동월증감률],
                       fill_color="white",
                       align=['right', 'left'],
                       font=dict(color=bar_data_color, size=13),
                       height=442 / len(bar_table_data))
        )])

        fig_table_bar_layout = go.Layout(margin=go.layout.Margin(l=0, r=0, b=0, t=0), height=442, width=120)
        fig_table_bar.update_layout(fig_table_bar_layout)

    else :
        bar_table_data_2 = bar_date_2.sort_values(by=[sort_data], ascending=True)
        bar_table_data_2 = bar_table_data_2[["Metric","날짜",sort_data]]
        bar_table_data_2 = bar_table_data_2[bar_table_data_2["날짜"] <= "2017-12-01"]
        fig_table_bar = go.Figure([go.Table(
            header=dict(values=[bar_table_data_2.Metric, bar_table_data_2.Metric],
                        fill_color="white",
                        align=['right', 'left'],
                        font=dict(size=1, color="white"),
                        height=0),
            cells=dict(values=[bar_table_data_2.Metric, bar_table_data_2.Metric],
                       fill_color="white",
                       align=['right', 'left'],
                       font=dict(color="white", size=1),
                       height=0)
        )])

        fig_table_bar_layout = go.Layout(margin=go.layout.Margin(l=0, r=0, b=0, t=0), height=442, width=130)
        fig_table_bar.update_layout(fig_table_bar_layout)



    # 라인차트


    try:
        if dddd_line > "2017-12-01":

            data_LP = data[data["업종"] == ids][data["geo_region"] == map_dt][data["규모"] == radio][data["날짜"]<=dddd_line]
            data_LP["Line_C"] = np.nan
            data_LP["year"] = "1"
            data_LP["month"] = "1"
            data_LP["X"] = np.nan
            for index, values in data_LP.iterrows():
                data_LP["날짜"][index] = datetime.strptime(data_LP["날짜"][index], "%Y-%m-%d").date()
                data_LP["year"][index] = data_LP["날짜"][index].strftime("%Y")
                data_LP["month"][index] = data_LP["날짜"][index].strftime("%m")
                try :
                    if data_LP["year"][index] == "2022":
                        data_LP["Line_C"][index] = "rgb(227, 87, 115)"
                    elif data_LP["year"][index] == "2021":
                        data_LP["Line_C"][index] = "rgb(77, 161, 194)"
                    elif data_LP["year"][index] == "2020":
                        data_LP["Line_C"][index] = "rgb(228, 147, 67)"
                    elif data_LP["year"][index] == "2019":
                        data_LP["Line_C"][index] = "rgb(209, 188, 70)"
                    elif data_LP["year"][index] == "2018":
                        data_LP["Line_C"][index] = "rgb(90, 178, 190)"
                    elif data_LP["year"][index]  == "2017":
                        data_LP["Line_C"][index] = "rgb(223, 111, 51)"
                except ValueError:
                    pass
                if data_LP["month"][index] <= "09":
                     data_LP["X"][index] = str(data_LP["month"][index])[1] + "월"
                else:
                    data_LP["X"][index] = str(data_LP["month"][index]) + "월"

            now_date = datetime.strptime(dddd_line,"%Y-%m-%d").date()
            now_year = now_date.strftime("%Y")
            last_date = now_date + relativedelta(years=-1)
            last_year = last_date.strftime("%Y")


            data_C_LP = data_LP[data_LP["year"] == now_year]
            data_C_LP["Value"] = round(data_C_LP["Value"] / 1000, 1)
            data_C_LP['text'] = np.nan


            data_L_LP = data_LP[data_LP["year"] == last_year]
            data_L_LP["Value"] = round(data_L_LP["Value"] / 1000, 1)
            data_L_LP['text'] = np.nan

            for index, values in data_C_LP.iterrows():
                data_C_LP['text'][
                    index] = f"{data_C_LP['year'][index]}년 {data_C_LP['X'][index]}의 전력 사용량 합계는 {data_C_LP['Value'][index]}GWH 입니다."
            for index, values in data_L_LP.iterrows():
                data_L_LP['text'][
                    index] = f"{data_L_LP['year'][index]}년 {data_L_LP['X'][index]}의 전력 사용량 합계는 {data_L_LP['Value'][index]}GWH 입니다."





            fig_line = make_subplots(specs=[[{"secondary_y": True}]])
            fig_line.add_trace(go.Scatter(
                x=data_C_LP["X"], y=data_C_LP["Value"], name=f"{data_C_LP['year'].unique()[0]}",
                mode= "markers+lines+text",
                text = data_C_LP["Value"],
                textposition="top center",
                textfont={"size": 10, "color": f"{data_C_LP['Line_C'].unique()[0]}"},
                hovertext=data_C_LP["text"],
                hoverinfo="text",
                line= dict(shape ="spline", color = f"{data_C_LP['Line_C'].unique()[0]}")
            ))


            fig_line.add_trace(go.Scatter(
                    x=data_L_LP["X"], y=data_L_LP["Value"], name=f"{data_L_LP['year'].unique()[0]}",
                mode="markers+lines+text",
                text=data_L_LP["Value"],
                textposition="bottom center",
                textfont={"size": 10, "color": f"{data_L_LP['Line_C'].unique()[0]}"},
                hovertext=data_L_LP["text"],
                    hoverinfo="text",
                line=dict(shape="spline", color = f"{data_L_LP['Line_C'].unique()[0]}")
                ))

            #frames = go.Frame(data=fig_line, traces=[0,12])

            #updmenus = [{"args":[None,{'frame':{"duration":12, "mode":"immediate"}}],"method":"animate"}]


            fig_line_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=00, l=50, t=0, b=0), height=207, width=523,
                                        showlegend=False,
                                        modebar_remove=["toImage", "zoom", "pan","select", "zoomin", "zoomout","autoscale","reset","senddatatocloud","lasso","resetscale"],
                                        modebar_add=["togglespikelines"])
                                        #xaxis={"showspikes":True}, yaxis={'showspikes':True})
            fig_line.update_layout(fig_line_layout)


        else:
            data_LP = data[data["업종"] == ids][data["geo_region"] == map_dt][data["규모"] == radio][data["날짜"]<=dddd_line]
            data_LP["year"] = "1"
            data_LP["month"] = "1"
            data_LP["Line_C"] = np.nan
            data_LP["X"] = np.nan
            for index, values in data_LP.iterrows():
                data_LP["날짜"][index] = datetime.strptime(data_LP["날짜"][index], "%Y-%m-%d").date()
                data_LP["year"][index] = data_LP["날짜"][index].strftime("%Y")
                data_LP["month"][index] = data_LP["날짜"][index].strftime("%m")
                try :
                    if data_LP["year"][index] == "2022":
                        data_LP["Line_C"][index] = "rgb(227, 87, 115)"
                    elif data_LP["year"][index] == "2021":
                        data_LP["Line_C"][index] = "rgb(77, 161, 194)"
                    elif data_LP["year"][index] == "2020":
                        data_LP["Line_C"][index] = "rgb(228, 147, 67)"
                    elif data_LP["year"][index] == "2019":
                        data_LP["Line_C"][index] = "rgb(209, 188, 70)"
                    elif data_LP["year"][index] == "2018":
                        data_LP["Line_C"][index] = "rgb(90, 178, 190)"
                    elif data_LP["year"][index]  == "2017":
                        data_LP["Line_C"][index] = "rgb(223, 111, 51)"
                except ValueError:
                    pass
                if data_LP["month"][index] <= "09":
                     data_LP["X"][index] = str(data_LP["month"][index])[1] + "월"
                else:
                    data_LP["X"][index] = str(data_LP["month"][index]) + "월"

            now_date = datetime.strptime(dddd_line,"%Y-%m-%d").date()
            now_year = now_date.strftime("%Y")
            last_date = now_date + relativedelta(years=-1)
            last_year = last_date.strftime("%Y")


            data_C_LP = data_LP[data_LP["year"] == now_year]
            data_C_LP["Value"] = round(data_C_LP["Value"] / 1000, 1)
            data_C_LP['text'] = np.nan
            for index, values in data_C_LP.iterrows():
                data_C_LP['text'][
                    index] = f"{data_C_LP['year'][index]}년 {data_C_LP['X'][index]}의 전력 사용량 합계는 {data_C_LP['Value'][index]}GWH 입니다."

            fig_line = go.Figure(go.Scatter(
                x=data_C_LP["X"], y=data_C_LP["Value"], name=f"{data_C_LP['year'].unique()[0]}",
                mode="markers+lines+text",
                text=data_C_LP["Value"],
                textposition="top center",
                textfont={"size": 10, "color": f"{data_C_LP['Line_C'].unique()[0]}"},
                hovertext=data_C_LP["text"],
                hoverinfo="text",
                line=dict(shape="spline", color=f"{data_C_LP['Line_C'].unique()[0]}"),

            ))
            fig_line_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=0, l=50, t=0, b=0), height=207, width=523,
                                        showlegend=False,
                                        modebar_remove=["toImage", "zoom", "pan","select", "zoomin", "zoomout","autoscale","reset","lasso","resetscale"],
                                        modebar_add=["togglespikelines"])
            fig_line.update_layout(fig_line_layout)



    except IndexError :
        fig_line = go.Figure(go.Scatter())
        fig_line_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(visible=False),yaxis=dict(visible=False))
        fig_line.update_layout(fig_line_layout)

    # 전년동월 바 차트
    data_Bar_LP = data[data["업종"] == ids][data["geo_region"] == map_dt][data["규모"] == radio][data["날짜"] <= dddd]

    data_Bar_LP["year"] = "1"
    data_Bar_LP["month"] = "1"
    data_Bar_LP["Line_C"] = np.nan
    data_Bar_LP["X"] = np.nan
    for index, values in data_Bar_LP.iterrows():
        data_Bar_LP["날짜"][index] = datetime.strptime(data_Bar_LP["날짜"][index], "%Y-%m-%d").date()
        data_Bar_LP["year"][index] = data_Bar_LP["날짜"][index].strftime("%Y")
        data_Bar_LP["month"][index] = data_Bar_LP["날짜"][index].strftime("%m")
        try:
            if data_Bar_LP["year"][index] == "2022":
                data_Bar_LP["Line_C"][index] = "rgb(227, 87, 115)"
            elif data_Bar_LP["year"][index] == "2021":
                data_Bar_LP["Line_C"][index] = "rgb(77, 161, 194)"
            elif data_Bar_LP["year"][index] == "2020":
                data_Bar_LP["Line_C"][index] = "rgb(228, 147, 67)"
            elif data_Bar_LP["year"][index] == "2019":
                data_Bar_LP["Line_C"][index] = "rgb(209, 188, 70)"
            elif data_Bar_LP["year"][index] == "2018":
                data_Bar_LP["Line_C"][index] = "rgb(90, 178, 190)"
            elif data_Bar_LP["year"][index] == "2017":
                data_Bar_LP["Line_C"][index] = "rgb(223, 111, 51)"
        except ValueError:
            pass
        if data_Bar_LP["month"][index] <= "09":
            data_Bar_LP["X"][index] = str(data_Bar_LP["month"][index])[1] + "월"
        else:
            data_Bar_LP["X"][index] = str(data_Bar_LP["month"][index]) + "월"

    now_date = datetime.strptime(dddd, "%Y-%m-%d").date()
    now_year = now_date.strftime("%Y")
    last_date = now_date + relativedelta(years=-1)
    last_year = last_date.strftime("%Y")

    data_Bar_LP["color"] = np.nan
    data_Bar_LP["color2"] = np.nan
    data_Bar_LP["text"] = np.nan
    data_Bar_LP["text2"] = np.nan
    data_Bar_LP["X"] = np.nan
    data_Bar_LP["per"] = np.nan
    data_Bar_LP["per2"] = np.nan
    for index, value in data_Bar_LP.iterrows():
        data_Bar_LP["전년동월증감률"][index] = round(data_Bar_LP["전년동월증감률"][index], 1)
        data_Bar_LP["전월증감률"][index] = round(data_Bar_LP["전월증감률"][index], 1)
        data_Bar_LP["per"][index] = str(data_Bar_LP["전년동월증감률"][index]) + "%"
        data_Bar_LP["per2"][index] = str(data_Bar_LP["전월증감률"][index]) + "%"
        if data_Bar_LP["month"][index] <= "09":
            data_Bar_LP["X"][index] = str(data_Bar_LP["month"][index])[1] + "월"
        else:
            data_Bar_LP["X"][index] = str(data_Bar_LP["month"][index]) + "월"


        if data_Bar_LP["전년동월증감률"][index] > 0:
            data_Bar_LP["color"][index] = "rgb(217, 97, 111)"
            data_Bar_LP["text"][
                index] = f"{data_Bar_LP['year'][index]}년 {data_Bar_LP['X'][index]}의 전년 동월 대비 증감률은 +{data_Bar_LP['전년동월증감률'][index]}% 입니다."
        elif data_Bar_LP["전년동월증감률"][index] < 0:
            data_Bar_LP["color"][index] = "rgb(89, 147, 201)"
            data_Bar_LP["text"][
                index] = f"{data_Bar_LP['year'][index]}년 {data_Bar_LP['X'][index]}의 전년 동월 대비 증감률은 -{data_Bar_LP['전년동월증감률'][index]}% 입니다."

        if data_Bar_LP["전월증감률"][index] > 0:
            data_Bar_LP["color2"][index] = "rgb(217, 97, 111)"
            data_Bar_LP["text2"][
                index] = f"{data_Bar_LP['year'][index]}년 {data_Bar_LP['X'][index]}의 전월 대비 증감률은 +{data_Bar_LP['전월증감률'][index]}% 입니다."
        elif data_Bar_LP["전월증감률"][index] < 0:
            data_Bar_LP["color2"][index] = "rgb(89, 147, 201)"
            data_Bar_LP["text2"][
                index] = f"{data_Bar_LP['year'][index]}년 {data_Bar_LP['X'][index]}의 전월 대비 증감률은 -{data_Bar_LP['전월증감률'][index]}% 입니다."

    data_C_BP = data_Bar_LP[data_Bar_LP["year"] == now_year]

    fig_7 = go.Figure(go.Bar(
        x=data_C_BP["X"], y=data_C_BP["전년동월증감률"], marker=dict(color=data_C_BP["color"]),
        text=data_C_BP["per"],
        textposition="inside",
        textfont=dict(color="white"),
        hoverinfo="text",
        hovertext=data_C_BP["text"]

    ))

    fig_7_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=0, l=50, t=0, b=0), height=207, width=523,
                             showlegend=False,
                             modebar_remove=["toImage", "zoom", "pan", "select", "zoomin", "zoomout", "autoscale","reset", "senddatatocloud", "lasso", "resetscale"],
                             modebar_add=["togglespikelines"]
                             )
    fig_7.update_layout(fig_7_layout)


    # 전월대비 바 차트
    fig_8 = go.Figure(go.Bar(
        x=data_C_BP["X"], y=data_C_BP["전월증감률"], marker=dict(color=data_C_BP["color2"]),
        text=data_C_BP["per2"],
        textposition="inside",
        hoverinfo="text",
        textfont=dict(color="white"),
        hovertext=data_C_BP["text2"],
    ))
    fig_8.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=True), margin=dict(r=0))

    fig_8_layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=0, l=50, t=0, b=0), height=211, width=523,
                             showlegend=False,
                             modebar_remove=["toImage", "zoom", "pan","select", "zoomin", "zoomout","autoscale","reset","senddatatocloud","lasso","resetscale"],
                             modebar_add=["togglespikelines"] )
    fig_8.update_layout(fig_8_layout)

    # 전월대비 표
    if dddd > "2017-12-01":
        map_data["전년동월증감률"] = round(map_data["전년동월증감률"], 2)
        map_data["color"] = np.nan
        map_data["증감"] = np.nan
        map_data["table"] = np.nan

        for index, values in map_data.iterrows():
            if map_data["전년동월증감률"][index] > 0:
                map_data["color"][index] = "rgb(217, 97, 111)"
                map_data["증감"][index] = "+"
            elif map_data["전년동월증감률"][index] < 0:
                map_data["color"][index] = "rgb(89, 147, 201)"
                map_data["증감"][index] = "-"
            else :
                map_data["color"][index] = "rgb(89, 147, 201)"
                map_data["증감"][index] = ""
            map_data["table"][index] = str(abs(map_data["전년동월증감률"][index])) + "%"

        cols_to_show = ["지역", "증감", "table"]

        map_data_color = []
        n = len(map_data)
        for col in cols_to_show:
            if col == "지역":
                map_data_color.append(["black"] * n)
            else:
                map_data_color.append(map_data["color"].tolist())

        fig_table = go.Figure([go.Table(
            header=dict(values=[map_data.지역],
                        fill_color="white",
                        align=['center', 'right', 'left'],
                        font=dict(size=1, color="white"),
                        height=0),

            cells=dict(values=[map_data.지역, map_data.증감, map_data.table],
                       fill_color="white",
                       align=['center', 'right', 'left'],
                       font=dict(color=map_data_color, size=11), height=19),
            columnwidth=[1, 1, 1]
        )])

        table_layout = go.Layout(margin=go.layout.Margin(
            l=0,
            r=0,
            b=0
            , t=0
        ), width=150, height=321)

        fig_table.update_layout(table_layout)
    else :
        map_data = map_data[["지역","날짜"]]
        map_data = map_data[map_data["날짜"] <= "2017-12-01"]
        fig_table = go.Figure([go.Table(
            header=dict(values=[map_data.지역],
                        fill_color="white",
                        align=['center', 'right', 'left'],
                        font=dict(size=1, color="white"),
                        height=0),

            cells=dict(values=[map_data.지역, map_data.지역, map_data.지역],
                       fill_color="white",
                       align=['center', 'right', 'left'],
                       font=dict(color=["black","white","white"], size=11), height=19),
            columnwidth=[1, 1, 1]
        )])
        table_layout = go.Layout(margin=go.layout.Margin(
            l=0,
            r=0,
            b=0
            , t=0
        ), width=150, height=321)

        fig_table.update_layout(table_layout)

    title1 = f"지역별 전력 사용량(단위 : GWh, 합계 : {format(round((max_date_data[max_date_data['규모'] == radio].sum()['Value'] / 1000), 1),',')}GWh"
    title2 = f"전력사용량(단위 : GWh, 합계: {format(round((max_date_data[max_date_data['규모'] == radio].sum()['Value'] / 1000), 1),',')}GWH)"
    title3 = f"전력사용량 현황({map_dt} {radio} {ids})"

    year = dddd[:4]
    if str(dddd[5:6]) <= "09":
        month = dddd[6]
    else:
        month = dddd[5:7]
    main_title = f"{year}년 {month}월"
    try:
        line_title_1 = str(data_L_LP["Line_C"].unique()[0])
        line_title_2 = str(data_L_LP["year"].unique()[0])
    except UnboundLocalError :
        line_title_1 = "rgb(238, 238, 238)"
        line_title_2 = ""
    try:
        line_title_3 = str(data_C_LP["Line_C"].unique()[0])
        line_title_4 = str(data_C_LP["year"].unique()[0])
    except IndexError:
        line_title_3 = "rgb(238, 238, 238)"
        line_title_4 = ""

    return return_title,\
           main_title,\
           main_title,\
           f"{format(round((max_date_data[max_date_data['규모'] == radio].sum()['Value'] / 1000), 1),',')}GWh",\
           f"{pm}{last_year_up}",\
           f"{m_pm}{last_month_up}",\
           f"{text_max_year}",\
           f"{max_year_pm}{max_lastyear}",\
           f"{text_min_year}",\
           f"{min_year_pm}{min_lastyear}",\
           f"{text_max_month}",\
           f"{max_month_pm}{max_lastmonth}",\
           f"{text_min_month}",\
           f"{min_month_pm}{min_lastmonth}",\
           {"width":"70.75px", "margin": "0px 0px 0px 0px", "text-align": "right", "color":line_title_1}, \
           line_title_2,\
           {"width":"70.75px","margin":"0px 0px 0px 0px","text-align":"right","color":line_title_3},\
           line_title_4,\
           fig_bar, \
           fig_bar_2, \
           fig_7, \
           fig_8, \
           fig_line, \
           fig_table,\
           fig_table_bar,\
           fig, \
           {"margin-bottom": "0%", "font-family": '나눔고딕', 'font-weight': 'bold', 'text-align': 'center', "font-size": "20px", "color": last_color, "vertical-align": "middle"},\
           {"margin-bottom":"0%","font-family":'나눔고딕','font-weight': 'bold', 'text-align': 'center', "font-size": "20px", "color": last_month_color},\
           {'font-weight': 'bold', 'text-align': 'center', "font-size": "18px", "color": max_lastyear_color,"margin-bottom":"0%"},\
           {'font-weight': 'bold', 'text-align': 'center', "font-size": "18px", "color": min_lastyear_color,"margin-bottom":"0%"},\
           {'font-weight': 'bold', 'text-align': 'center', "font-size": "18px", "color": max_lastmonth_color,"margin-bottom":"0%"},\
           {'font-weight': 'bold', 'text-align': 'center', "font-size": "18px", "color": min_lastmonth_color,"margin-bottom":"0%"}, \
           kpi_title_1,\
           kpi_title_2,\
           kpi_title_3,\
           kpi_title_4,\
           kpi_title_5,\
           kpi_title_6,\
           title1,\
           title2,\
           title3,\
           clickData,\
           clickData2,\
           0,\
           0,\
           # v,\
           # mi,\
           # ma












if __name__ == '__main__':
   #os.environ["FLASK_ENV"] = "development"
    #app.run()
   app.run(host='0.0.0.0', port=5050, debug=True)

