# tokenizer インスタンスの生成
# 対象モデルは'bert-base-uncased'
# torchtextのバージョンアップに伴い、legacyを付ける必要あり
from torchtext.legacy import data
from torchtext.legacy import datasets
import csv
from transformers import BertTokenizer, BertModel,AdamW, get_constant_schedule_with_warmup
import torch
import torch.nn as nn
import random
from BERTSentiment import *
import torch.optim as optim
from tqdm import tqdm
import time
import math

# GPU利用
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert = BertModel.from_pretrained('bert-base-uncased')

# tokenizer関数の動作確認
tokens = tokenizer.tokenize("What's going on?")
# convert_tokens_to_ids関数の動作確認
indexes = tokenizer.convert_tokens_to_ids(tokens)
# BERT固有の特殊トークン達
cls_token = tokenizer.cls_token
sep_token = tokenizer.sep_token
pad_token = tokenizer.pad_token
unk_token = tokenizer.unk_token
#print(cls_token, sep_token, pad_token, unk_token)

# idによるトークン表記
cls_token_idx = tokenizer.cls_token_id
sep_token_idx = tokenizer.sep_token_id
pad_token_idx = tokenizer.pad_token_id
unk_token_idx = tokenizer.unk_token_id
#print(cls_token_idx, sep_token_idx, pad_token_idx, unk_token_idx)

#シード値
SEED = 2222
# 訓練時のバッチサイズ
BATCH_SIZE = 16
#インスタンス生成用
OUTPUT_DIM = 2

N_EPOCHS = 3
#train_data_len = 25000
train_data_len = 2500
warmup_percent = 0.2

# 入力テキストのトークン化関数
def tokenize(sentence):
    tokens = tokenizer.tokenize(sentence) 
    # 252までで切る
    tokens = tokens[:254-2]
    return tokens

# モデルのパラメータ数の確認
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# スケジューラの定義
def get_scheduler(optimizer, warmup_steps):
    scheduler = get_constant_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps)
    return scheduler

#　精度計算
def categorical_accuracy(preds, y):
    max_preds = preds.argmax(dim = 1, keepdim = True)
    correct = (max_preds.squeeze(1)==y).float()
    return correct.sum() / len(y)

def train(model, iterator, optimizer, criterion, scheduler):
    
    epoch_loss = 0
    epoch_acc = 0
    model.train()
    
    for batch in tqdm(iterator):
        optimizer.zero_grad() # clear gradients first
        torch.cuda.empty_cache() # releases all unoccupied cached memory 
        text = batch.text
        label = batch.label
        predictions = model(text)
        loss = criterion(predictions, label)
        acc = categorical_accuracy(predictions, label)
        loss.backward()
        optimizer.step()
        scheduler.step()
        epoch_loss += loss.item()
        epoch_acc += acc.item()
        
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

def evaluate(model, iterator, criterion):
    epoch_loss = 0
    epoch_acc = 0
    model.eval()
    
    with torch.no_grad():
        for batch in tqdm(iterator):
            text = batch.text
            label = batch.label
            predictions = model(text)
            loss = criterion(predictions, label)
            acc = categorical_accuracy(predictions, label)
            epoch_loss += loss.item()
            epoch_acc += acc.item()
        
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

if __name__ == "__main__":
    # 正解ラベル
    LABEL = data.LabelField()
    # 入力データ
    TEXT = data.Field(batch_first = True,
                    use_vocab = False,
                    # 上で定義したトークン化関数
                    tokenize = tokenize,
                    # 前処理として各トークンをIDに変換
                    preprocessing = tokenizer.convert_tokens_to_ids,
                    init_token = cls_token_idx,
                    eos_token = sep_token_idx,
                    pad_token = pad_token_idx)

    train_data, valid_data = datasets.IMDB.splits(TEXT, LABEL)

    train_data1, train_data2 = train_data.split(random_state=random.seed(SEED),split_ratio=0.1)
    valid_data1, valid_data2 = valid_data.split(random_state=random.seed(SEED),split_ratio=0.1)

    # 訓練用、検証用のイテレーターの定義
    train_iterator, valid_iterator = data.BucketIterator.splits(
        (train_data1, valid_data1), 
        batch_size = BATCH_SIZE, 
        device = device)

    # 訓練データの中身を見てみる
    #idx0 = train_data[1].text
    #print(idx0)

    # token表記に戻してみる
    #text0 = tokenizer.convert_ids_to_tokens(idx0)
    #print(text0)

    model = BERTSentiment(bert,OUTPUT_DIM).to(device)
    print(f'The model has {count_parameters(model):,} trainable parameters')

    # 最適化関数の定義
    optimizer = AdamW(model.parameters(),lr=2e-5,eps=1e-6)

    # 損失関数の定義
    criterion = nn.CrossEntropyLoss().to(device)
    
    total_steps = math.ceil(N_EPOCHS*train_data_len*1./BATCH_SIZE)
    warmup_steps = int(total_steps*warmup_percent)
    scheduler = get_scheduler(optimizer, warmup_steps)

    best_valid_loss = float('inf')
    
    # 学習
    # 学習時間は１epochあたり５分、計15分程度です(Google ColabでGPU利用の場合)
    for epoch in range(N_EPOCHS):

        start_time = time.time()
        # 学習と評価
        train_loss, train_acc = train(model, train_iterator, optimizer, criterion, scheduler)
        # 検証データによる評価
        valid_loss, valid_acc = evaluate(model, valid_iterator, criterion)
        
        #  処理時間の計算
        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)
        
        # 検証データの損失が最もいい場合は、モデルを保存する
        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), 'bert-nli.pt')
        
        print(f'Epoch: {epoch+1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
        print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}%')
        print(f'\t Val. Loss: {valid_loss:.3f} |  Val. Acc: {valid_acc*100:.2f}%')