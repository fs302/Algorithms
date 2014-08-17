import networkx as nx
from collections import defaultdict
import sys

def read_nodeadjlist(filename):
  G = nx.Graph()
  for line in open(filename):
    e1, es = line.split(':')
    es = es.split()
    for e in es:
      if e == e1: continue
      G.add_edge(int(e1),int(e))
  return G

def findCommunities(filename):
  G = read_nodeadjlist(filename)
  c = nx.connected_components(G)
  return c

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Expected list of ego networks, e.g. 'python link_clustering.py *.egonet'"
    sys.exit(0)
  print "UserId,Predicted"
  for arg in sys.argv[1:]:
    egoUser = -1
    try:
      egoUser = int(arg.split('/')[-1].split('.egonet')[0])
    except Exception as e:
      print "Expected files to be names 'X.egonet' where X is a user ID"
      sys.exit(0)
    cs = list(findCommunities(arg))
    if len(cs) == 0:
      cs = [set(adj.keys())]
    cs = [' '.join([str(y) for y in x]) for x in cs]
    print str(egoUser) + ',' + ';'.join(cs)
