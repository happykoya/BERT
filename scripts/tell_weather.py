#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2 import QtCore, QtScxml
import requests
import json
from datetime import datetime, timedelta, time

current_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
forecast_url = 'https://api.openweather.org/data.2.5/forecast'
appid = '99999999999999999999999999999'

prefs = ["三重","京都","佐賀","兵庫","北海道","千葉","和歌山",
         "埼玉","大分","大阪","奈良","宮城","宮崎","富山","山口","山形","山梨",
         "岐阜","岡山","岩手","島根","広島","徳島","愛媛","愛知","新潟","東京",
         "栃木","沖縄","滋賀","熊本","石川","神奈川","福井","福岡","福島","秋田",
         "群馬","茨城","長崎","長野","青森","静岡","香川","高知","鳥取","鹿児島"]

latlon= {"沖縄":(26.212,127.681),"鹿児島":(31.560,130.558),	"宮崎":(31.91,131.42), "長崎":(32.74,129.87),"熊本":(32.79,130.74),
             "大分":(33.23,131.61),"佐賀":(33.24,130.30), "高知":(33.56,133.53), "福岡":(33.60,130.41), "愛媛":(33.84,132.76),
             "徳島":(34.06,134.55), "山口":(34.18,131.47), "和歌山":(34.22,135.16),"香川":(34.34,134.04),"広島":(34.39,132.46), 
             "岡山":(34.66,133.93),"奈良":(34.68,135.83),"大阪府":(34.68,135.52),"兵庫":(34.69,135.18),"三重":(34.73,136.50),
             "静岡":(34.97,138.38),"滋賀":(35.00,135.86),"京都府":(35.02,135.75),"愛知":(35.18,136.90), "岐阜":(35.39,136.72),
             "神奈川":(35.44,139.64),"島根":(35.47,133.05),"鳥取":(35.50,134.23), "千葉":(35.60,140.12),"山梨":(35.66,138.56),	 
             "東京都":(35.68,139.692), "埼玉":(35.85,139.64), "福井":(36.06,136.22),"茨城":(36.34,140.44), "群馬":(36.39,139.06),	 
             "栃木":(36.56,139.88),"石川":(36.59,136.62),"長野":(36.65,138.18), "富山":(36.695,137.21),"福島":(37.75,140.46),
             "新潟":(37.90,139.02), "山形":(38.24,140.36), "宮城":(38.26,140.87), "岩手":(39.70,141.15), "秋田":(39.71,140.10), 
             "青森":(40.82,140.74), "北海道":(43.065,141.34)}

def get_place(text):
    for pref in prefs:
        if pref in text:
            return pref

def get_date(text):
    if "今日" in text:
        return "今日"
    elif "明日" in text:
        return "明日"
    else:
        return ""
    
def get_type(text):
    if "天気" in text:
        return "天気"
    elif "気温" in text:
        return "気温"
    else:
        return ""

def get_current_weather(lat,lon):
    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(current_weather_url,lat,lon,appid))
    return response.json()

def get_tomorrow_weather(lat,lon):
    today = datetime.today()
    tommorrow = today + timedelta(days=1)
    tommorrow_noon = datetime.combine(tommorrow,time(12.0))
    timestamp = tommorrow_noon.timestamp()

    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(forecast_url,lat,lon,appid))
    d = response.json()
    for i in range(len(d["list"])):
        dt = float(d["list"][i]["dt"])
        if dt >= timestamp:
            return d["list"][i]
    return "" 

app = QtCore.QCoreApplication()
el = QtCore.QEventLoop()

#SCXMLファイルの読み込み
sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')
sm.start()
el.processEvents()

print("sys>:こちらは天気情報案内システムです.")

uttdic = {"ask_place":"地名を教えてください.",
          "ask_date" :"日付を教えてください.",
          "ask_type" :"情報の種類を教えてください."}

current_state = sm.activeStateNames()[0]
print("current_state:",current_state)

sysutt = uttdic[current_state]
print("sys>",sysutt)

while True:
    text = input(">")
    if current_state == "ask_place":
        place = get_place(text)
        if place != "":
            sm.submitEvent("place")
            el.processEvents()
    elif current_state == "ask_date":
        date = get_date(text)
        if date != "":
            sm.submitEvent("date")
            el.processEvents()
    elif current_state == "ask_type":
        _type = get_type(text)
        if _type != "":
            sm.submitEvent("type")
            el.processEvents()
            
    sm.submitEvent(text)
    el.processEvents()
    
    current_state = sm.activeStateNames()[0]
    print("current_state:", current_state)
    
    if current_state == "tell_info":
        print("お伝えしますね")
        lat = latlon[place][0]
        lon = latlon[place][1]
        if date == "今日":
            print("lat=",lat,"lon=",lon)
            cw = get_current_weather(lat,lon)
            if _type == "天気":
                print(cw["weather"][0]["description"])
            elif _type == "気温":
                print(str(cw["main"]["temp"])+"度です")

        elif date == "明日":
            print("lat=",lat,"lon=",lon)
            cw = get_tomorrow_weather(lat,lon)
            if _type == "天気":
                print(cw["weather"][0]["description"])
            elif _type == "気温":
                print(str(cw["main"]["temp"])+"度です")

        break
    else:
        sysutt = uttdic[current_state]
        print("sys>",sysutt)

print("ご利用ありがとうございました(*^^*)")
