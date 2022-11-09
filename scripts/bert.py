from torch import nn
from transformers import AutoModel, AutoTokenizer
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import re

MODEL_NAME = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


train_data = fetch_20newsgroups(subset = 'train')
valid_data = fetch_20newsgroups(subset = 'test')

train = pd.DataFrame({"text" : train_data["data"], "target" : train_data["target"]})
valid = pd.DataFrame({"text" : valid_data["data"], "target" : valid_data["target"]})
print(train.shape, valid.shape)
train.head()

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained("bert-base-uncased")
        self.classifier = nn.Linear(in_features = 768, out_features = 20)
    
    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs = self.bert(input_ids = input_ids, attention_mask = attention_mask, token_type_ids = token_type_ids)
        pooler_output = outputs.pooler_output
        logits = self.classifier(pooler_output).squeeze(-1)
        return logits

    def cleaning(text):
        text = re.sub("\n", " ", text) # 改行削除
        text = re.sub("[^A-Za-z0-9]", " ", text) # 記号削除
        text = re.sub("[' ']+", " ", text) # スペース統一
        return text.lower() # 小文字で出力

