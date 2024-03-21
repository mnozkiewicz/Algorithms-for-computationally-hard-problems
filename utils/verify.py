# APTO Piotr Faliszewski 2018
# Test solution for the VertexCover problem


import utils.dimacs
import sys


def loadSolution(name):
    f = open(name, "r")
    s = f.readline().strip()
    C = s.split(",")
    C = [int(c) for c in C]
    return C


if len(sys.argv) < 3:
    print("Invocation:")
    print("  python verify.py graph-file solution-file")
    exit()

try:
    G = dimacs.loadGraph(sys.argv[1])
    C = loadSolution(sys.argv[2])
except IOError:
    print("IOError")

E = dimacs.edgeList(G)
if dimacs.isVC(E, C):
    print("OK", len(C))
else:
    print("Fail!")
