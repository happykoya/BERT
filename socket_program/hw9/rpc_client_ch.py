#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# クライアント側

import xmlrpc.client
# サーバーに接続
server = xmlrpc.client.ServerProxy("http://localhost:8000/")

# 関数の呼び出し
while 1:
    text = input("文字を入力してね:")
    change_way = input("変換方法は?:")
    if change_way == "大文字" or change_way == "upper":
        result = server.upper(text)
        
    elif change_way == "小文字" or change_way == "小" or change_way == "lower":
        result = server.lower(text)
        
    print("結果:", result)
