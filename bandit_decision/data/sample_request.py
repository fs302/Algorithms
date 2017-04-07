import random

fi = open("request_merge.csv","r")

fo = open("request_sample.csv","w")

sample_rate = 0.5
datasets = []
for line in fi.readlines():
    if random.random()<sample_rate:
        datasets.append(line)

random.shuffle(datasets)
for line in datasets:
    fo.write(line)

fi.close()
fo.close()
