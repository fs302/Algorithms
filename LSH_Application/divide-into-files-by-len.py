# divide sentences into files with each files has the same length of sentences
import sys

if len(sys.argv)==3:
	DIRName = sys.argv[1]
	fileIn = open(sys.argv[2], 'r')
else:
	exit

group = {}
line = fileIn.readline()
while line:
	data = line.split()
	glen = len(data) - 1
	if glen not in group:
		group[glen] = []
	group[glen].append(line)
	line = fileIn.readline()

fileIn.close()

for glen in group:
	fo = open(DIRName+str(glen)+'.txt','w')
	for line in group[glen]:
		fo.write(line)
	fo.close()
