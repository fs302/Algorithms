#Load Data
InputFileName = "a1"
OutputFileName = InputFileName + "_out"
suffix = ".txt"

Fin = open(InputFileName+suffix,"rb")
Fout = open(OutputFileName+suffix,"wb")

points = []
for line in Fin.readlines():
    data = line.split()
    if len(data)==2:
        a = int(data[0])
        b = int(data[1])
        points.append((a,b))

def getDistance(pt1, pt2):
    tmp = pow(pt1[0]-pt2[0],2) + pow(pt1[1]-pt2[1],2)
    return pow(tmp,0.5)

#Calculating
    #-----choose dc
dis = []
distance = {}
maxd = 0
for i in range(0,len(points)):
    for j in range(i+1,len(points)):
        pt1 = points[i]
        pt2 = points[j]
        d = getDistance(pt1,pt2)
        dis.append(d)
        distance[i,j] = d
        dis.append(d)
        distance[j,i] = d
        if d>maxd:
            maxd = d
            

dc_percent = 2.0
dis.sort()
dc = dis[int(len(dis)*dc_percent)/100]
    #-----choose dc
    #-----cal rho
rho = [0 for i in range(len(points))]

for i in range(0,len(points)):
    for j in range(i+1,len(points)):
        dij = getDistance(points[i],points[j])
        if dij<dc:
            rho[i] += 1
            rho[j] += 1
    #-----cal rho

rho_list =[(rho[i],i) for i in range(len(rho))]
rho_sorted = sorted(rho_list, reverse=1)
print("Highest rho:",rho_sorted[0])

delta = [maxd for i in range(len(points))]
nneigh = [0 for i in range(len(points))]
for ii in range(1,len(rho_sorted)):
    for jj in range(0,ii):
        id_p1 = rho_sorted[ii][1]
        id_p2 = rho_sorted[jj][1]
        if (distance[ii,jj]<delta[id_p1]):
            delta[id_p1] = distance[ii,jj]
            nneigh[id_p1] = id_p2

for i in range(len(points)):
    Fout.write(str(rho[i])+","+str(delta[i])+","+str(i)+"\n")

#Assign Cluster

Fin.close()
Fout.close()
