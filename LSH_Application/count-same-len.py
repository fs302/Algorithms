# count pairs in the same file, with edit distance <= 1

import sys
import os
import time

dirName = 'files/'
outFileName = 'pair_list.txt'

if len(sys.argv)==2:
	outFileName = sys.argv[1]

if len(sys.argv)==3:
	dirName = sys.argv[1]
	outFileName = sys.argv[2]

def time_me(fn):
	def _wrapper(*args, **kwargs):
		start = time.clock()
		fn(*args, **kwargs)
		print "%s cost %s second" %(fn.__name__, time.clock()-start)
	return _wrapper


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
	l = len(d1)
	count = 0
	for i in range(1,l):
		if d1[i] != d2[i]:
			count += 1
	if count<=1:
		return True
	else:
		return False
	

def process(f, pair, key):
	buckets = {} 
	# put line into buckets
	for line in f.readlines():
		data = line[:-1].split()
		bids = gethash(data,key)
		if str(bids) not in buckets:
			buckets[str(bids)] = []
		buckets[str(bids)].append(data)
	
	# bucket solve
	true_count = 0
	false_count = 0
	for bid in buckets:
		b = buckets[bid]
		for i in range(len(b)-1):
			for j in range(i+1,len(b)):
				if int(b[i][0])>int(b[j][0]):
					tmp = b[i]
					b[i] = b[j]
					b[j] = tmp
				if edit1(b[i],b[j]):
					pair.append((b[i][0],b[j][0]))
					true_count += 1
				else:
					false_count += 1
	return (true_count, false_count)
		
pair = []

key = range(1,2)
print "[count-same-len]"
print "key:", key
true_count = 0
false_count = 0
hashmap = [{} for i in key]
for fi in os.listdir(dirName):
	if '.txt' in fi:
		f = open(dirName+fi,'r')
		(tc,fc) = process(f,pair,key)
		true_count += tc
		false_count += fc
		f.close()
print key,"true pair:",true_count,", false pair:",false_count

key = range(-1,0)
print "key:", key
true_count = 0
false_count = 0
hashmap = [{} for i in key]
for fi in os.listdir(dirName):
	if '.txt' in fi:
		f = open(dirName+fi,'r')
		(tc,fc) = process(f,pair,key)
		true_count += tc
		false_count += fc
		f.close()
print key,"true pair:",true_count,", false pair:",false_count

'''for key in range(-5,0):
	print key
	true_count = 0
	false_count = 0
	hashmap = {}
	for fi in os.listdir(dirName):
		if '.txt' in fi:
			f = open(dirName+fi,'r')
			(tc,fc) = process(f,pair,key)
			true_count += tc
			false_count += fc
			f.close()
	print key,"true pair:",true_count,", false pair:",false_count
	print
'''
pair.sort()

fo = open(outFileName,'w')
if len(pair)>0:
	fo.write(pair[0][0]+" "+pair[0][1]+'\n')
for i in range(1,len(pair)):
	if pair[i]!=pair[i-1]:
		fo.write(pair[i][0]+" "+pair[i][1]+"\n")
fo.close()
