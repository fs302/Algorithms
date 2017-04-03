import random

def multi_result_random(dist,itemSplitor,kvSplitor):
    # dist like 'a:0.1^b:0.2^c:0.7', return a/b/c
    choice_probs = dist.split(itemSplitor)
    elevation = 0.0
    choice_queue = []
    total_volumn = 1e-6 + sum([float(choice_prob.split(kvSplitor)[1]) for choice_prob in choice_probs])
    for choice_prob in choice_probs:
        kv = choice_prob.split(kvSplitor)
        if len(kv) < 2:
            continue
        choice,prob = kv[0],float(kv[1])/total_volumn
        choice_queue.append((elevation + prob,choice))
        elevation += prob
    point = random.random()
    for choice in choice_queue:
        if choice[0] > point:
            return choice[1]
    return choice_queue[-1][1]
        
def loadPreferAndUV(preferFilename):
    preferFile = open(preferFilename,"r")
    head = preferFile.readline()
    preferDist = {}
    uvDist = []

    for line in preferFile.readlines():
        data = line.split(",")
        if len(data)<4:
            continue
        level,gender = data[0],data[1]
        dist = data[2]
        uv = int(data[3])
        preferDist[(level,gender)] = dist
        uvDist.append(str(level)+"&"+str(gender)+":"+str(uv))
    preferFile.close()    
    return preferDist,'^'.join(uvDist)
    

def generateRequest(requestNum):
    preferFileName = "data/prefer2.csv"
    requestFileName = "data/request3.csv"
    requestFile = open(requestFileName,"w")
    preferDist, uvDistStr = loadPreferAndUV(preferFileName)
    for t in range(requestNum):
        people = multi_result_random(uvDistStr,"^",":") # format: level&gender
        level,gender = people.split("&")
        choice = multi_result_random(preferDist[level,gender],"^",":")
        if choice == None:
            print choice
            continue
        if t % 10000 == 0:
            print str(t)+","+level+","+gender+","+choice
        requestFile.write(str(t)+","+level+","+gender+","+choice+"\n")
    requestFile.close()
    
if __name__ == "__main__":
    requestNum = 100000
    generateRequest(requestNum)
    print ("generate %d request"%requestNum)
