# mapping words to numbers

import sys

if len(sys.argv)<2:
	print 'usage python mapping_words.py inFile OutFile'


fileIn = open(sys.argv[1], 'r')
fileOut = open(sys.argv[2], 'w')

word_id = {}
count = 0

line = fileIn.readline()
while line:
	data = line[:-1].split()
	target = [int(data[0])]
	for word in data[1:]:
		if word not in word_id:
			word_id[word] = count
			count += 1
		target.append(word_id[word])
	for item in target[:-1]:
		fileOut.write(str(item)+" ")
	fileOut.write(str(target[-1])+"\n")
	line = fileIn.readline()

print "Word Set Size:",count
fileIn.close()
fileOut.close()
