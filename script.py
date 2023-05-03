# By Muteb Alshammari
# Script that run the exp. 5 times and find the average
#####
#
#######

from MST import *
import random
import time
import sys

sumInc=sumDec=sumPrim = 0
for i in range(0,5):
    G = Graph()
        
    insertList = set()
    deleteList = set()

    # reading from file
    filename = sys.argv[1]
    numOp = 100
    with open(filename, 'r') as f:
        for v in range(0,int(f.readline())):
            G.addVertex(v)
        for line in f:
            split = line.split()
            x = int(split[0])
            y = int(split[1])
            w = int(split[2])
            G.addEdge(x,y,w)
            G.addEdge(y, x,w)

    # build the tree and collect the updated edges


    # build th tree and recording time
    mst = MST()
    mst.init_MST(G.numVertices)
    start = time.time()
    # Builing Prim's Alg.
    mst.primMST(G,0)
    end = time.time()
    prime = end-start
    sumPrim+= prime
    print("Time to run Prim's Alg.", end-start)

    # collecting updated edges from the tree
    for u in mst.treeList:
        for edge in mst.treeList[u].getChildren():
            isEdge = random.randint(0,1)
            if not isEdge:
                deleteList.add(edge)
    print (len(deleteList))
    start = time.time()
    for i in range(0,numOp):
        edge = deleteList.pop()
        insertList.add(edge)
        mst.decMST(G, edge.sr, edge.ds, edge.w)
    end = time.time()
    dec = end-start
    sumDec+= dec
    print("Time to run dec. Alg.", end-start)

    # DDA 
    # Inserting Edges 
    start = time.time()
    for i in range(0,numOp):
        edge = insertList.pop()
        mst.incMST(G, edge.sr, edge.ds, edge.w)
    end = time.time()
    inc = end-start
    sumInc+= inc
    print("Time to run Inc's Alg.", end-start)

 



    del G 
    del mst, insertList, deleteList
    time.sleep(5)
    
writing = open("results2", 'a')
writing.write(filename + "  SUM   SUM \n" + str(sumPrim/5) + "\n")
writing.write(str(sumDec/5) + "\n")
writing.write(str(sumInc/5) + "\n")
writing.write( "---------------------\n")
# Write to file