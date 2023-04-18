import random

write_lines = []
uttrs = []

with open("dialogue_pairs.txt") as f:
    for l in f:
        if "\t" in l:
            l = l.strip()
            write_lines.append(l + "\t1\n")
            uttrs.append(l.split("\t")[0])
            uttrs.append(l.split("\t")[1])
            
for i in range(len(write_lines)):
    write_lines.append(random.choice(uttrs) + "\t" + random.choice(uttrs) + "\t0\n")
    
random.shuffle(write_lines)

index = 0
with open("dev.tsv", "w") as var_f:
    for l in write_lines[:200]:
        var_f.write(str(index) + "\t" + l)
        index += 1

index = 0
with open("train.tsv", "w") as var_f:
    for l in write_lines[200:]:
        var_f.write(str(index) + "\t" + l)
        index += 1
        
