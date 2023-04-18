import spacy
from spacy import displacy
nlp = spacy.load('ja_ginza')
doc = nlp('新橋で打ち合わせをしましょう。')

# 単語の係り受け解析
for token in doc:
    print(token.text+' ← '+token.head.text+', '+token.dep_)

# グラフ表示
displacy.render(doc, style='ent', jupyter=False)