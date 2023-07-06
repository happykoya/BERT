from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill 
import MeCab

mecab = MeCab.Tagger()
mecab.parse('')

SENTS = []
LABELS = []

def train_svc():
    for line in open("da_samples.dat", "r"):
        line = line.strip()
        da, utt = line.split('\t')
        words = []
        for line in mecab.parse(utt).splitlines():
            if line == "EOS":break
            else:
                word, feature_str = line.split("\t")
                words.append(word)

        SENTS.append(" ".join(words))
        LABELS.append(da)

    vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split())
    X = vectorizer.fit_transform(SENTS)

    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(LABELS)

    svc = SVC(gamma="scale")
    svc.fit(X,Y)

    with open("svc.model","wb") as f:
        dill.dump(vectorizer, f)
        dill.dump(label_encoder,f)
        dill.dump(svc, f)