#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2 import QtCore, QtScxml

prefs = ["三重","京都","佐賀","兵庫","北海道","千葉","和歌山",
         "埼玉","大分","大阪","奈良","宮城","宮崎","富山","山口","山形","山梨",
         "岐阜","岡山","岩手","島根","広島","徳島","愛媛","愛知","新潟","東京",
         "栃木","沖縄","滋賀","熊本","石川","神奈川","福井","福岡","福島","秋田",
         "群馬","茨城","長崎","長野","青森","静岡","香川","高知","鳥取","鹿児島"]

def get_place(text):
    for pref in prefs:
        if pref in text:
            return pref

def get_date(text):
    if "今日" in text:
        return "今日"
    elif "昨日" in text:
        return "昨日"
    else:
        return ""
    
def get_type(text):
    if "天気" in text:
        return "天気"
    elif "気温" in text:
        return "気温"
    else:
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
        place = get_date(text)
        if place != "":
            sm.submitEvent("date")
            el.processEvents()
    elif current_state == "ask_type":
        place = get_type(text)
        if place != "":
            sm.submitEvent("type")
            el.processEvents()
            
    sm.submitEvent(text)
    el.processEvents()
    
    current_state = sm.activeStateNames()[0]
    print("current_state:", current_state)
    
    if current_state == "tell_info":
        print("天気をお伝えしますね")
        break
    else:
        sysutt = uttdic[current_state]
        print("sys>",sysutt)
        
print("ご利用ありがとうございました(*^^*)")