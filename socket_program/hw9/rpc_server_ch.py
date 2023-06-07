#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# サーバー側

from xmlrpc.server import SimpleXMLRPCServer

# 関数の実装（簡単な足し算）
def add_numbers(x, y):
    return x + y

# 関数の実装(大文字に変換)
def upper_text(text):
    converted_text = text.upper()
    return converted_text

# 関数の実装(小文字に変換)
def lower_text(text):
    converted_text = text.lower()
    return converted_text

# サーバーの作成と関数の登録
server = SimpleXMLRPCServer(("localhost", 8000))

server.register_function(upper_text, name="upper")
server.register_function(lower_text, name="lower")

print("サーバーを開始しました。\n")
print("クライアント側を待っています.....\n")
# クライアントからのリクエストを待機
server.serve_forever()
