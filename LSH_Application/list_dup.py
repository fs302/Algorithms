import sys

# sentences
finName = sys.argv[1]
# dup_list
foutName = sys.argv[2]

fin = open(finName, 'r')
fout = open(foutName,'w')

line = fin.readline()
m = {}
while line:
	data = line[:-1].split()
	key = int(data[0])
	val = line[line.find(' ')+1:-1]
	print val
	if val not in m:
		m[val] = []
	m[val].append(key)
	line = fin.readline()

fin.close()

for val in m:
	li = m[val]
	for i in li:
		for j in li:
			if i != j:
				fout.write(str(i)+" "+str(j)+"\n")
fout.close()
