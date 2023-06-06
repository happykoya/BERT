#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# クライアント側

import xmlrpc.client
# サーバーに接続
server = xmlrpc.client.ServerProxy("http://localhost:8000/")

# 関数の呼び出し
while 1:
    text = input("文字を入力してね:")
    result = server.change_text(text)
    print("結果:", result)
