import re
import random
import json
import xml.etree.ElementTree

prefs = ["三重","京都","佐賀","兵庫","北海道","千葉","和歌山",
         "埼玉","大分","大阪","奈良","宮城","宮崎","富山","山口","山形","山梨",
         "岐阜","岡山","岩手","島根","広島","徳島","愛媛","愛知","新潟","東京",
         "栃木","沖縄","滋賀","熊本","石川","神奈川","福井","福岡","福島","秋田",
         "群馬","茨城","長崎","長野","青森","静岡","香川","高知","鳥取","鹿児島"]

dates= ["今日","明日"]
types = ["天気","気温"]



def random_generate(root):
    if len(root)  == 0:
        return root.text
    buf = ""
    for el in root:
        if el.tag == "place":
            pref = random.choice(prefs)
            buf += pref 
        elif el.tag == "date":
            date = random.choice(dates)
            buf += date
        elif el.tag == "type":
            _type = random.choice(types)
            buf += _type

        if el.tail is not None:
            buf += el.tail
    return buf


def main():
    da = ''
    f = open("da_samples.dat","w")
    for line in open("exam.txt", "r"):
        line  = line.strip()
        if re.search(r'^da=', line):
            da = line.replace('da=', '')
        elif line == "":
            pass
        else:
            root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
            for i in range(1000):
                sample = random_generate(root)
                f.write(da + "\t" + sample + "\n")
    
    print("finish increase")
    f.close()
        
if __name__ == "__main__":
    main()