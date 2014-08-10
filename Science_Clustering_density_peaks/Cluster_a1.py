def getDistance(pt1, pt2):
    tmp = pow(pt1[0]-pt2[0],2) + pow(pt1[1]-pt2[1],2)
    return pow(tmp,0.5)

def ChooseDc(dc_percent,points,dis,distance):
    avgNeighbourNum = dc_percent*len(points)
    
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
    dis.sort()
    return dis[int(avgNeighbourNum*len(points)*2)]

def drawOriginGraph(pl,points):
    x = [xx for (xx,yy) in points]
    y = [yy for (xx,yy) in points]
    pl.plot(x,y,'bo')

def drawDecisionGraph(pl,rho, delta):
    pl.plot(rho, delta,'go')

def Cluster():
    #=========Load Data=========
    InputFileName = "a1"
    OutputFileName = InputFileName + "_out"
    suffix = ".txt"

    Fin = open(InputFileName+suffix,"r")
    Fout = open(OutputFileName+suffix,"w")

    points = []
    for line in Fin.readlines():
        data = line.split()
        if len(data)==2:
            a = float(data[0])
            b = float(data[1])
            points.append((a,b))

    #=========Calculating=========
        #-----choose dc-----
    dc_percent = 0.02
    dis = []
    distance = {}
    dc = ChooseDc(dc_percent,points,dis,distance)
    print("dc:"+str(dc))

        #-----cal rho:"Cut off" kernel
    rho = [0 for i in range(len(points))]
    for i in range(0,len(points)):
        for j in range(i+1,len(points)):
            dij = getDistance(points[i],points[j])
            if dij<dc:
                rho[i] += 1
                rho[j] += 1

    rho_list =[(rho[i],i) for i in range(len(rho))]
    rho_sorted = sorted(rho_list, reverse=1)
    print("Highest rho:",rho_sorted[0])

    maxd = dis[-1]
    delta = [maxd for i in range(len(points))]
    nneigh = [0 for i in range(len(points))]
    for ii in range(1,len(rho_sorted)):
        for jj in range(0,ii):
            id_p1 = rho_sorted[ii][1] #get point1's id
            id_p2 = rho_sorted[jj][1] #get point2's id
            if (distance[ii,jj]<delta[id_p1]):
                delta[id_p1] = distance[ii,jj]
                nneigh[id_p1] = id_p2

    import pylab as pl
    fig1 = pl.figure(1)
    pl.subplot(121)
    drawOriginGraph(pl,points)
    pl.subplot(122)
    drawDecisionGraph(pl,rho,delta)
    pl.show()

    for i in range(len(points)):
        Fout.write(str(i)+","+str(rho[i])+","+str(delta[i])+"\n")

    #Assign Cluster

    Fin.close()
    Fout.close()

if __name__=="__main__":
    Cluster()
