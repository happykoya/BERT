from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill 
import MeCab

mecab = MeCab.Tagger()
mecab.parse('')

with open("svc.model", "rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc = dill.load(f)

def extract(utt):
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS": break
        else:
            word, feature_str = line.split("\t")
            words.append(word)

    token_str = " ".join(words)
    X = vectorizer.transform([token_str])
    Y = svc.predict(X)
    da = label_encoder.inverse_transform(Y)[0]
    return da

def main():
    for utt in ["大阪の明日の天気","もう一度はじめから","東京じゃなくて"]:
        da = extract(utt)
        print(utt,da)

if __name__ == "__main__":
    main()