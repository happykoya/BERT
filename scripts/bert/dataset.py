#BERTを実装する際には必要らしい
from transformers import AutoModel, AutoTokenizer
import torch
from torch.utils.data import Dataset, DataLoader
#データセットダウンロード用
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

#トークナイザーの生成
MODEL_NAME = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

#バッチサイズの指定
BATCH_SIZE = 8
MAX_LEN = 256

#データセット取得
train_data = fetch_20newsgroups(subset = 'train')
valid_data = fetch_20newsgroups(subset = 'test')
train = pd.DataFrame({"text" : train_data["data"], "target" : train_data["target"]})
valid = pd.DataFrame({"text" : valid_data["data"], "target" : valid_data["target"]})
print(train.shape, valid.shape)

class Data(Dataset):
    def __init__(self, data, tokenizer, max_length):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text = self.data["cleaned_text"].values[idx]
        encoded = tokenizer(
            text,
            padding = "max_length",
            max_length = self.max_length,
            truncation = True
        )
        input_ids = torch.tensor(encoded["input_ids"], dtype = torch.int32)
        attention_mask = torch.tensor(encoded["attention_mask"], dtype = torch.int32)
        token_type_ids = torch.tensor(encoded["token_type_ids"], dtype = torch.int32)
        label = self.data["target"].values[idx]
        label = torch.tensor(label, dtype = torch.int32)
        return input_ids, attention_mask, token_type_ids, label

def cleaning(text):
    text = re.sub("\n", " ", text) # 改行削除
    text = re.sub("[^A-Za-z0-9]", " ", text) # 記号削除
    text = re.sub("[' ']+", " ", text) # スペース統一
    return text.lower() # 小文字で出力


train["cleaned_text"] = train["text"].map(cleaning)
valid["cleaned_text"] = valid["text"].map(cleaning)

train_ds = Data(train, tokenizer, MAX_LEN)
train_dl = DataLoader(train_ds, batch_size = BATCH_SIZE, shuffle = True, drop_last = True)
valid_ds = Data(valid, tokenizer, MAX_LEN)
valid_dl = DataLoader(valid_ds, batch_size = BATCH_SIZE * 2, shuffle = False, drop_last = False)
