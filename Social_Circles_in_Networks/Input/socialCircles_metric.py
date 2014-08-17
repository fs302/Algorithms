import os
from collections import defaultdict
import random
from pylab import *
import sys
from munkres import Munkres
import numpy

# Compute the loss for one user (i.e., one set of circles for one ego-network)
# usersPerCircle: list of sets of users (groundtruth). Order doesn't matter.
# usersPerCircleP: list of sets of users (predicted). Order doesn't matter.
def loss1(usersPerCircle, usersPerCircleP):
  #psize: either the number of groundtruth, or the number of predicted circles (whichever is larger)
  psize = max(len(usersPerCircle),len(usersPerCircleP)) # Pad the matrix to be square
  # mm: matching matrix containing costs of matching groundtruth circles to predicted circles.
  #     mm[i][j] = cost of matching groundtruth circle i to predicted circle j
  mm = numpy.zeros((psize,psize))
  # mm2: copy of mm since the Munkres library destroys the data during computation
  mm2 = numpy.zeros((psize,psize))
  for i in range(psize):
    for j in range(psize):
      circleP = set() # Match to an empty circle (delete all users)
      circle = set() # Match to an empty circle (add all users)
      if (i < len(usersPerCircleP)):
        circleP = usersPerCircleP[i]
      if (j < len(usersPerCircle)):
        circle = usersPerCircle[j]
      nedits = len(circle.union(circleP)) - len(circle.intersection(circleP)) # Compute the edit distance between the two circles
      mm[i][j] = nedits
      mm2[i][j] = nedits

  if psize == 0:
    return 0 # Edge case in case there are no circles
  else:
    m = Munkres()
    #print mm2 # Print the pairwise cost matrix
    indices = m.compute(mm) # Compute the optimal alignment between predicted and groundtruth circles
    editCost = 0
    for row, column in indices:
      #print row,column # Print the optimal value selected by matching
      editCost += mm2[row][column]
    return int(editCost)

if len(sys.argv) != 3:
  print "Expected two arguments (ground-truth and prediction filenames)"
  sys.exit(0)

groundtruthFile = sys.argv[1] # Ground-truth
predictionFile = sys.argv[2] # Prediction

gf = open(groundtruthFile, 'r') # Read the ground-truth
pf = open(predictionFile, 'r') # Read the predictions

# Should just be header
gf.readline()
pf.readline()

gLines = gf.readlines()
pLines = pf.readlines()

gf.close()
pf.close()

if len(gLines) != len(pLines):
  print "Ground-truth and prediction files should have the same number of lines"
  sys.exit(0)

circlesG = {}
circlesP = {}
for gl, pl in zip(gLines, pLines):
  uidG,friendsG = gl.split(',')
  uidP,friendsP = pl.split(',')
  circlesG[int(uidG)] = [set([int(x) for x in c.split()]) for c in friendsG.split(';')]
  circlesP[int(uidP)] = [set([int(x) for x in c.split()]) for c in friendsP.split(';')]

totalLoss = 0
for k in circlesP.keys():
  if not circlesG.has_key(k):
    print "Ground-truth has prediction for circle", k, "but prediction does not"
    sys.exit(0)
  l = loss1(circlesG[k], circlesP[k])
  print "loss for user", k, "=", l
  totalLoss += l

print "total loss for all users =", totalLoss
