import sys

# dup-count-list
f1Name = sys.argv[1]

# pair-list
f2Name = sys.argv[2]

f1 = open(f1Name, 'r')

# get dup-count
line = f1.readline()
pc = {}
while line:
	data = line[:-1].split()
	key = int(data[0])
	val = int(data[1])
	pc[key] = val
	line = f1.readline()

f1.close()

# record total pair
tot = 0

f2 = open(f2Name,'r')
for line in f2.readlines():
	data = line[:-1].split()
	a = int(data[0])
	b = int(data[1])
	n = 1
	if a in pc:
		n = pc[a]
	m = 1
	if b in pc:
		m = pc[b]
	tot += n*m
	print n*m

for db in pc:
	n = pc[db]
	tot += n*(n-1)/2
	print n*(n-1)/2

print tot
	
