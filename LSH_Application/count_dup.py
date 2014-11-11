import sys

# dup_list
finName = sys.argv[1]
# dup_count
foutName = sys.argv[2]

fin = open(finName, 'r')
fout = open(foutName,'w')

line = fin.readline()
m = {}
while line:
	data = line[:-1].split()
	a = int(data[0])
	b = int(data[1])
	if a not in m:
		m[a] = [a]
	m[a].append(b)
	line = fin.readline()

fin.close()

keys = m.keys()
keys.sort()
st = []
for key in keys:
	stand = min(m[key])
	print m[key],"min:",stand
	if stand not in st:
		fout.write(str(stand)+" "+str(len(m[key]))+"\n")
	st.append(stand)
fout.close()
