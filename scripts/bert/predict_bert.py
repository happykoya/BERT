# ライブラリのインポート
import pandas as pd
import numpy as np
from IPython.display import display

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

# 訓練用データ読み込み
coqa = pd.read_json('http://downloads.cs.stanford.edu/nlp/data/coqa/coqa-train-v1.0.json')
# データの確認
display(coqa.head())

# データの先頭行の内容表示
item = coqa.loc[0,'data']
print(item)

#　テキスト(text)、質問(question)、回答(answer)の抽出
# 一つのテキストに対して質問、回答のペアは複数対応
cols = ["text","question","answer"]

# 抽出リストの１行分
comp_list = []
for index, row in coqa.iterrows():

    # 質問の個数だけ繰り返し
    for i in range(len(row["data"]["questions"])):
        temp_list = []

        # text
        temp_list.append(row["data"]["story"])

        # i番目の質問
        temp_list.append(row["data"]["questions"][i]["input_text"])

        # i番目の回答
        temp_list.append(row["data"]["answers"][i]["input_text"])

        # リストのリストを生成
        comp_list.append(temp_list)

# comp_listからデータフレームを生成
data = pd.DataFrame(comp_list, columns=cols)

#　２度目以降のために、csvファイルとしても保存
data.to_csv("CoQA_data.csv", index=False)

# 先頭と、最後の内容表示
display(data.head())
display(data.tail())

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# 特定の１セットを抽出
index = 10
text = data["text"][index]
question = data["question"][index]
answer = data["answer"][index]

# 質問、テキストの組をエンコードする
input_ids = tokenizer.encode(question, text)

# エンコードの値から逆向きにトークンの一覧を取得
tokens = tokenizer.convert_ids_to_tokens(input_ids)
# input_idsの長さを計算
input_len = len(input_ids)
print(f'入力文字列の長さ: {input_len}')

#　[SEP] tokenの最初の位置
sep_idx = input_ids.index(tokenizer.sep_token_id)
print("SEP token index: ", sep_idx)

#　セグメントAのトークン数　
# (pythonのindexはゼロから始まるので、sep token indexより１大きい)
num_seg_a = sep_idx+1
print("Number of tokens in segment A: ", num_seg_a)

# セグメントBのトークン数
num_seg_b = len(input_ids) - num_seg_a
print("Number of tokens in segment B: ", num_seg_b)

# segment_idsの計算
segment_ids = [0]*num_seg_a + [1]*num_seg_b
print(segment_ids)

#　segmeind_idsの長さとinput_idsの長さが一致していることの確認
assert len(segment_ids) == len(input_ids)

# inpit_idsとsegment_idsを用いて予測の実施
output = model(torch.tensor([input_ids]),  token_type_ids=torch.tensor([segment_ids]))

# answer_start と answer_endの計算
answer_start = torch.argmax(output.start_logits)
answer_end = torch.argmax(output.end_logits)
if answer_end >= answer_start:
    answer = " ".join(tokens[answer_start:answer_end+1])
else:
    answer = ("I am unable to find the answer to this question. Can you please ask another question?")

#  結果の確認
print(answer_start, answer_end, answer)

question_cap = question.capitalize()
answer_cap = answer.capitalize()

print(f"\nQuestion:\n{question_cap}")
print(f"\nAnswer:\n{answer_cap}")