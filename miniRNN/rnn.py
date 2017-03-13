__author__ = 'fanshen.fs'

# implemented Andrej Karpathy's Mini-Rnn

import numpy as np
# import matplotlib.pyplot as plt
from collections import deque
import random

class RNN(object):

    def __init__(self, insize, outsize, hidsize, learning_rate):
        self.insize = insize

        self.h = np.zeros((hidsize, 1)) # hidden state stored from last batch of inputs

        self.W_hh = np.random.randn(hidsize, hidsize)*0.01 # hidden to hidden
        self.W_xh = np.random.randn(hidsize, insize)*0.01  # input to hidden
        self.W_hy = np.random.randn(outsize, hidsize)*0.01 # hidden to output
        self.b_h = np.zeros((hidsize, 1)) # bias of h
        self.b_y = np.zeros((outsize, 1)) # bias of y

        self.adaW_hh = np.zeros((hidsize, hidsize))
        self.adaW_xh = np.zeros((hidsize, insize))
        self.adaW_hy = np.zeros((outsize, hidsize))
        self.adab_h = np.zeros((hidsize, 1))
        self.adab_y = np.zeros((outsize, 1))

        self.learning_rate = learning_rate

    def train(self, x, y):

        xs, hs, ys, ps = {}, {}, {}, {}
        hs[-1] = np.copy(self.h)

        loss = 0
        # forward pass
        for t in xrange(len(x)):
            xs[t] = np.zeros((self.insize, 1))
            xs[t][x[t]] = 1
            hs[t] = np.tanh(np.dot(self.W_xh, xs[t]) + np.dot(self.W_hh, hs[t-1]) + self.b_h) # hidden state
            ys[t] = np.dot(self.W_hy, hs[t]) + self.b_y # un-normalized log probabilities of next chars
            ps[t] = np.exp(ys[t])/np.sum(np.exp(ys[t])) # probabilities for next charts
            loss += -np.log(ps[t][y[t],0]) # softmax(cross-entropy loss) *?*

        # backward pass: compute gradients going backwards
        dWxh, dWhh, dWhy = np.zeros_like(self.W_xh), np.zeros_like(self.W_hh), np.zeros_like(self.W_hy)
        dbh, dby = np.zeros_like(self.b_h), np.zeros_like(self.b_y)
        dhnext = np.zeros_like(hs[0])
        for t in reversed(xrange(len(x))):
            dy = np.copy(ps[t])
            dy[y[t]] -= 1
            dWhy += np.dot(dy, hs[t].T)
            dby += dy
            dh = np.dot(self.W_hy.T, dy) + dhnext  # backprop into h
            dhraw = (1 - hs[t] * hs[t]) * dh # backprop through tanh nonlinearity
            dbh += dhraw
            dWxh += np.dot(dhraw, xs[t].T)
            dWhh += np.dot(dhraw, hs[t-1].T)
            dhnext = np.dot(self.W_hh.T, dhraw)

        for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
            np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients

        for param, dparam, adaparam in zip([self.W_xh, self.W_hh, self.W_hy, self.b_h, self.b_y],\
                                           [dWxh, dWhh, dWhy, dbh, dby],\
                                           [self.adaW_xh, self.adaW_hh, self.adaW_hy, self.adab_h, self.adab_y]):
            adaparam += dparam * dparam
            param += -self.learning_rate*dparam/np.sqrt(adaparam + 1e-8) # adagrad update

        self.h = hs[len(x)-1]

        return loss


    def sample(self, seed, n):
        """
        sample a sequence of integers from the model
        h is memory state, seed_ix is seed letter for first time step
        """
        ixes = []
        h = self.h

        xhat = np.zeros((self.insize, 1))
        xhat[seed] = 1

        for t in range(n):
            h = np.tanh(np.dot(self.W_xh, xhat) + np.dot(self.W_hh, h) + self.b_h)
            y = np.dot(self.W_hy, h) + self.b_y
            p = np.exp(y) / np.sum(np.exp(y))
            ix = np.random.choice(range(self.insize), p=p.ravel()) # why random choice not softmax?

            xhat = np.zeros((self.insize, 1))
            xhat[ix] = 1
            ixes.append(ix)

        return ixes

def main():
    # open a text file
    data = open('obama.txt','r').read() # simple plain text file
    logfile = open('obama.log','w')
    chars = list(set(data))
    data_size, vocab_size = len(data), len(chars)
    print 'data has %d charaters, %d unique.' % (data_size, vocab_size)
    print chars

    # make some dictionaries for encoding end decoding from 1-of-k
    char_to_ix = {ch :i for i,ch in enumerate(chars)}
    ix_to_char = {i :ch for i,ch in enumerate(chars)}

    # insize and outsize are len(chars).
    rnn = RNN(len(chars), len(chars), 100, 0.1)

    # iterate over batches of input and target output
    seq_length = 25
    losses = []
    smooth_loss = -np.log(1.0/len(chars))*seq_length
    losses.append(smooth_loss)

    D = deque()
    MEMORY = 1000

    for i in range(len(data)):

        x = [char_to_ix[c] for c in data[i:i+seq_length]] # inputs to the RNN
        y = [char_to_ix[c] for c in data[i+1:i+seq_length+1]] # targets

        D.append((x,y))
        if len(D) > MEMORY:
            D.popleft()

        if i % 1000 == 0:
            sample_ix = rnn.sample(x[0], 200)
            txt = ''.join([ix_to_char[n] for n in sample_ix])
            print 'No.'+str(i)+' iteration: '+txt
            logfile.write('iteration '+str(i)+': '+txt+'\n')

        training_set = random.sample(D,1)
        loss = rnn.train(training_set[0][0], training_set[0][1])
        smooth_loss = smooth_loss*0.999 + loss*0.001

        if i % 1000 == 0:
            print 'iteration %d, smooth_loss = %f' % (i, smooth_loss)
            logfile.write('iteration %d, smooth_loss = %f\n' % (i, smooth_loss))
            losses.append(smooth_loss)

    # plt.plot(range(len(losses)), losses, 'b', label='smooth loss')
    # plt.xlabel('time in thousands of iterations')
    # plt.ylabel('loss')
    # plt.legend()
    # plt.show()

    data.close()
    logfile.close()

if __name__ == "__main__":
    main()