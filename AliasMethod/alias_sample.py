import numpy        as np
import numpy.random as npr

def alias_setup(probs):
    K       = len(probs)
    q       = np.zeros(K)
    J       = np.zeros(K, dtype=np.int)

    # Sort the data into the outcomes with probabilities
    # that are larger and smaller than 1/K.
    smaller = []
    larger  = []
    for kk, prob in enumerate(probs):
        q[kk] = K*prob
        if q[kk] < 1.0:
            smaller.append(kk)
        else:
            larger.append(kk)

    # Loop though and create little binary mixtures that
    # appropriately allocate the larger outcomes over the
    # overall uniform mixture.
    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        J[small] = large
        q[large] = q[large] - (1.0 - q[small])

        if q[large] < 1.0:
            smaller.append(large)
        else:
            larger.append(large)

    return J, q

def alias_draw(J, q):
    K  = len(J)

    # Draw from the overall uniform mixture.
    kk = int(np.floor(npr.rand()*K))

    # Draw from the binary mixture, either keeping the
    # small one, or choosing the associated larger one.
    if npr.rand() < q[kk]:
        return kk
    else:
        return J[kk]

K = 1000
N = 1000000

print "K=",K,",N=",N

import time

# Get a random probability vector.
probs = npr.dirichlet(np.ones(K), 1).ravel()

#print "Probability Distribution:",probs

t_start = time.time()

# Construct the table.
J, q = alias_setup(probs)

# print J
# print q

# Generate variates.
X = np.zeros(N)
Xs = np.zeros(K)
for nn in xrange(N):
    result = alias_draw(J, q)
    X[nn] = result
    Xs[result] += 1


t_end = time.time()

print "Alias Sample Time Used:",t_end-t_start

#print "Sample:", X

t_start = time.time()


Y = np.zeros(N)
Ys = np.zeros(K)
for nn in xrange(N):
    result = np.argmax(np.random.multinomial(1, probs, size=1))
    Y[nn] = result
    Ys[result] += 1


t_end = time.time()

print "np.random.multinomial Sample Time Used:",t_end-t_start


sum_Xs = sum(Xs)
Xs_norm = [float(x)/sum_Xs for x in Xs]

#print "Alias Sample Prob:",Xs_norm

sum_Ys = sum(Ys)
Ys_norm = [float(y)/sum_Ys for y in Ys]

#print "np.random.multinomial Sample Prob:", Ys_norm

print "Alias Sample Sum Abs diff:",sum(np.abs(Xs_norm-probs))
print "np.random.multinomial Sum Abs diff:", sum(np.abs(Ys_norm-probs))