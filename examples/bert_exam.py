#サンプルプログラム
#https://resanaplaza.com/2022/06/12/%E3%80%90%E5%AE%9F%E8%B7%B5%E3%80%91python%E3%81%A8bert%E3%81%A7%E6%84%9F%E6%83%85%E5%88%86%E6%9E%90%E3%81%97%E3%82%88%E3%81%86%E3%82%88%EF%BC%81/

from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer
 
# 感情分析の実行
model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
nlp = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)
 
 
print(nlp('授業が長くて疲れたな。家に帰って早く休もう。'))
