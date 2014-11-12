# count sentences in neighbor files, that is (n,n+1), fit the standard [edit distance <= 1]
import sys
import os

dirName = 'files/'
outFileName = 'nn_pair_list.txt'

if len(sys.argv)==2:
	outFileName = sys.argv[1]

if len(sys.argv)==3:
	dirName = sys.argv[1]
	outFileName = sys.argv[2]

def gethash(data, key):
	global hashmap
	bucketnum = 21312111
	targets = []
	for i in range(len(key)):
		k = key[i]
		value = int(data[k])
		target = (value * 213 + 1) % bucketnum 
		while target in hashmap[i] and hashmap[i][target] != value:
			target = (target + 1) % bucketnum 
		hashmap[i][target] = value
		targets.append(target)
	return targets
		
def edit1(d1,d2):
	k = 1 
	l = len(d1)
	while k < l and d1[k]==d2[k]:
		k += 1
	if k != l:
		while k < l and d1[k]==d2[k+1]:
			k += 1
	if k==l:
		return True
	else:
		return False

def process(f1,f2, pair, key):
	buckets_1 = {}
	buckets_2 = {}
	# put line into buckets
	for line in f1.readlines():
		data = line[:-1].split()
		bids = gethash(data, key)
		bid = str(bids)
		if bid not in buckets_1:
			buckets_1[bid] = []
		buckets_1[bid].append(data)
	
	for line in f2.readlines():
		data = line[:-1].split()
		bids = gethash(data,key)
		bid = str(bids)
		if bid not in buckets_2:
			buckets_2[bid] = []
		buckets_2[bid].append(data)
	
	# bucket solve
	true_count = 0
	false_count = 0
	for bid in buckets_1:
		if bid not in buckets_2:
			continue
		b1 = buckets_1[bid]
		b2 = buckets_2[bid]
		for i in b1:
			for j in b2: 
				if edit1(i,j):
					pair.append((i[0],j[0]))
					true_count += 1
				else:
					false_count += 1
	return (true_count, false_count)
		
pair = []

key = range(1,2)
print "[count-next-len]"
print "key:",key
true_count = 0
false_count = 0
hashmap = [{} for i in key]
files = os.listdir(dirName)
for i in range(len(files)):
	fi = files[i]
	if '.txt' in fi:
		fj = str(int(fi.split('.')[0])+1)+'.txt' 
		if (fj in files):
			f1 = open(dirName+fi,'r')
			f2 = open(dirName+fj,'r')
			(tc,fc) = process(f1,f2,pair,key)
			true_count += tc
			false_count += fc
			f1.close()
			f2.close()
print key,"true pair:",true_count,", false pair:",false_count

key = range(-1,0)
print "key:",key
true_count = 0
false_count = 0
hashmap = [{} for i in key]
files = os.listdir(dirName)
for i in range(len(files)):
	fi = files[i]
	if '.txt' in fi:
		fj = str(int(fi.split('.')[0])+1)+'.txt' 
		if (fj in files):
			f1 = open(dirName+fi,'r')
			f2 = open(dirName+fj,'r')
			(tc,fc) = process(f1,f2,pair,key)
			true_count += tc
			false_count += fc
			f1.close()
			f2.close()
print key,"true pair:",true_count,", false pair:",false_count

pair.sort()

fo = open(outFileName,'w')
if len(pair)>0:
	fo.write(pair[0][0]+" "+pair[0][1]+'\n')
for i in range(1,len(pair)):
	if pair[i]!=pair[i-1]:
		fo.write(pair[i][0]+" "+pair[i][1]+"\n")
fo.close()
