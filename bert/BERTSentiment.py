# モデルの定義
# 事前学習済みモデルの後段に線形関数を追加し、この出力で感情分析をする
import torch.nn as nn

class BERTSentiment(nn.Module):
    def __init__(self,
                 bert,
                 output_dim):
        
        super().__init__()
        
        self.bert = bert
        embedding_dim = bert.config.to_dict()['hidden_size']
        self.out = nn.Linear(embedding_dim, output_dim)
        
    def forward(self, text):
        #text = [batch size, sent len]

        #embedded = [batch size, emb dim]
        embedded = self.bert(text)[1]
        
        #output = [batch size, out dim]
        output = self.out(embedded)
        
        return output