# -*- coding: utf-8 -*-
import math
import copy
import numpy as np
import matplotlib.pyplot as plt

isdebug = True

# 代码参考自 http://blog.csdn.net/chasdmeng/article/details/38709063

# 指定k个高斯分布参数，注意k个高斯分布具有相同均方差Sigma
def ini_data(Sigma,LatentMu,k,N):
    global X
    global Mu
    global Expectations
    X = np.zeros((1,N))
    Mu = np.random.random(k)
    probs = np.random.dirichlet(np.ones(k), 1).ravel()
    #probs = [0.5, 0.5]
    if isdebug:
        print "***********"
        print "Select Probability:",probs
    Expectations = np.zeros((N,k))
    for i in xrange(0,N):
        arm = np.argmax(np.random.multinomial(1, probs, size=1))
        X[0,i] = np.random.normal()*Sigma + LatentMu[arm]
    if isdebug:
        print "***********"
        print u"初始观测数据X："
        print X

# EM算法：步骤1，计算E[zij]
def e_step(Sigma,k,N):
    global Expectations
    global Mu
    global X
    for i in xrange(0,N):
        Denom = 0
        for j in xrange(0,k):
            Denom += math.exp((-1/(2*(float(Sigma**2))))*(float(X[0,i]-Mu[j]))**2)
        for j in xrange(0,k):
            Numer = math.exp((-1/(2*(float(Sigma**2))))*(float(X[0,i]-Mu[j]))**2)
            Expectations[i,j] = Numer / Denom
    if isdebug:
        print "***********"
        print u"隐藏变量E（Z）："
        print Expectations

# EM算法：步骤2，求最大化E[zij]的参数Mu
def m_step(k,N):
    global Expectations
    global X
    for j in xrange(0,k):
        Numer = 0
        Denom = 0
        for i in xrange(0,N):
            Numer += Expectations[i,j]*X[0,i]
            Denom +=Expectations[i,j]
        Mu[j] = Numer / Denom 

# 算法迭代iter_num次，或达到精度Epsilon停止迭代
def run(Sigma,LatentMu,k,N,iter_num,Epsilon):
    ini_data(Sigma,LatentMu,k,N)
    print u"初始均值:", Mu
    for i in range(iter_num):
        Old_Mu = copy.deepcopy(Mu)
        e_step(Sigma,k,N)
        m_step(k,N)
        print "第%d次迭代均值 %s" % (i,str(Mu))
        if sum(abs(Mu-Old_Mu)) < Epsilon:
            break
if __name__ == '__main__':
    LatentMu = [40,20,100]
    run(6,LatentMu,len(LatentMu),10000,100,0.0001)
    plt.hist(X[0,:],50)
    plt.show()
