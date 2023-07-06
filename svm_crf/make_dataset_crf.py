import re
import random
import json
import xml.etree.ElementTree
import MeCab

prefs = ["三重","京都","佐賀","兵庫","北海道","千葉","和歌山",
         "埼玉","大分","大阪","奈良","宮城","宮崎","富山","山口","山形","山梨",
         "岐阜","岡山","岩手","島根","広島","徳島","愛媛","愛知","新潟","東京",
         "栃木","沖縄","滋賀","熊本","石川","神奈川","福井","福岡","福島","秋田",
         "群馬","茨城","長崎","長野","青森","静岡","香川","高知","鳥取","鹿児島"]

dates= ["今日","明日"]
types = ["天気","気温"]

mecab = MeCab.Tagger()
mecab.parse('')

def random_generate(root):
    buf = ""
    pos = 0
    posdic = {}
    if len(root)  == 0:
        return root.text, posdic
    
    for el in root:
        if el.tag == "place":
            pref = random.choice(prefs)
            buf += pref
            posdic["place"] = (pos, pos+len(pref))
            pos += len(pref)
        elif el.tag == "date":
            date = random.choice(dates)
            buf += date
            posdic["date"] = (pos, pos+len(date))
            pos += len(date)
        elif el.tag == "type":
            _type = random.choice(types)
            buf += _type
            posdic["type"] = (pos, pos+len(_type))
            pos += len(_type)
        if el.tail is not None:
            buf += el.tail
            pos += len(el.tail) 

    return buf, posdic

def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"



def main():
    da = ''
    f = open("crf_samples.dat","w")
    for line in open("exam.txt", "r"):
        line  = line.strip()
        if re.search(r'^da=', line):
            da = line.replace('da=', '')
        elif line == "":
            pass
        else:
            root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
            for i in range(1000):
                sample, posdic = random_generate(root)
                lis = []
                pos = 0
                prev_label = 0
                for line in mecab.parse(sample).splitlines():
                    if line == "EOS": break
                    else:
                        word, feature_str = line.split("\t")
                        features = feature_str.split(',')
                        postag  = features[0]
                        label = get_label(pos, posdic)
                        if label == "O":            lis.append([word,postag,"O"])
                        elif label == prev_label:   lis.append([word,postag,"I-"+label])
                        else:                       lis.append([word,postag,"B-"+label])
                        pos += len(word)
                        prev_label = label

            for word, postag, label in lis:
                f.write(word + "\t" + postag + "\t" + label +"\n")
            f.write("\n")
    
    print("finish increase")
    f.close()
        
if __name__ == "__main__":
    main()