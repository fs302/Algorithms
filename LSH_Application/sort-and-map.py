import sys

# sentences
finName = sys.argv[1]
# sorted_and_mapped_list
foutName = sys.argv[2]
# duplicate_pair_list
dupPairFileName = sys.argv[3]
# duplicate_count_list
dupCountFileName = sys.argv[4]

fin = open(finName, 'r')

word_id = {}
count = 0

line = fin.readline()
m = {}
while line:
	data = line[:-1].split()
	key = int(data[0])
	target = []
	for word in data[1:]:
		if word not in word_id:
			word_id[word] = count
			count += 1
		target.append(word_id[word])
	val = ""
	for item in target[:-1]:
		val = val + str(item)+" "
	val += str(target[-1])
	if val not in m:
		m[val] = []
	m[val].append(key)
	line = fin.readline()

fin.close()

fout = open(foutName,'w')
dupPair = open(dupPairFileName,'w')
dupCount = open(dupCountFileName, 'w')

for val in m:
	li = m[val]
	length = len(li)
	key = min(li)
	fout.write(str(key)+" "+val+"\n")
	dupCount.write(str(key)+" "+str(length)+"\n")
	li.sort()
	for i in range(length-1):
		for j in range(i+1, length):
			dupPair.write(str(li[i])+" "+str(li[j])+"\n")
fout.close()
dupPair.close()
dupCount.close()