# By Muteb Alshammari
# Python imp. of MST and DMST to:
# Prim's Alg.
# DDA and IDA of Muteb Alshammari
#####
#
#######



import time
from random import randint
from heapq import heappush, heappop



class Vertex:
    def __init__(self, key):
        self.id = key
        self.heapIndex = float('inf')
        self.connectedTo = set()
        self.color = 0
        self.edges = set()

    def addNeighbor(self, nbr,w):
        self.connectedTo.add((nbr,w))
        
    def addEdge(self, edge):
        self.edges.add(edge)
        
    def remNeighbor(self, nbr):
        for v in self.getConnections():
            if v[0].id == nbr:
                self.connectedTo.remove(v)
                return
                
    def remEdge(self,edge):
        for e in self.getEdges():
            if e == edge:
                self.edges.remove(e)
                return
                
    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in
                self.connectedTo])
                
    def getConnections(self):
        return self.connectedTo
        
    def getEdges(self):
        if (len(self.edges)):
            return self.edges
        else:
            return 0
        
    def getEdge(self,edge):
        for e in self.getEdges():
            if e == edge:
                return e

    def getId(self):
        return self.id

    def getIndex(self):
        return self.heapIndex

    def getWeight(self, nbr):
        for v in self.getConnections():
            if v[0].id == nbr:
                return v[1]

class Graph:

    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.edgeList=set()
        self.numEdges = 0

    def addVertex(self, key):
        if (key<self.numVertices and self.numVertices>0):
            return
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex
    def addEdge(self, f, t, w):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        exist = 0
        if self.vertList[f].edges:
            for edge in self.vertList[f].getEdges(): # does not exist
                if edge.ds == t:
                    exist=1
        if self.vertList[t].edges:
            for edge in self.vertList[t].getEdges():
                if edge.ds == f:
                    exist=1
        if not exist:
            e = Edge(t, f, w)
            self.vertList[t].addEdge(e)
            e = Edge(f, t, w)
            self.vertList[f].addEdge(e)
            self.edgeList.add(e)
            self.vertList[f].addNeighbor(self.vertList[t], w)
            self.vertList[t].addNeighbor(self.vertList[f], w)

    def rmEdge(self, f, t):
        self.vertList[f].remNeighbor(t)
        for e in self.edgeList:
            if e.sr == f and e.ds == t:
                self.vertList[f].remEdge(e)
                self.vertList[t].remEdge(e)
                self.edgeList.remove(e)
                return
        
        
    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    
    def __contains__(self, n):
        return n in self.vertList

''' 

      tree class 
' 
'
'
''' 
class treeV:

    def __init__(self, vertex):
        self.id = vertex
        self.wieght = float('inf')
        self.parent = None
        self.color = 0
        self.children = set()
    def getChildren(self):
        return self.children

class MST:

    def __init__(self):
        self.treeList = {}
 
    def init_MST(self, n):
        for i in range(n):
            self.treeList[i] = treeV(i)
                 
            
    def primMST(self, G, source):
        
        for v in self.treeList:
            self.treeList[v].color = 1
        self.treeList[source].color = 0
        heap = Heap()
        for e in G.vertList[source].getEdges():
            if e.heapIndex == float('inf'):
                heap.push(e, e.w)
            else:
                heap.update(e.w, e.heapIndex)
        while heap.heap():
            popped = heap.pop() # pop an edge with the min. wieght
            popped.heapIndex = float('inf')
            if self.treeList[popped.ds].color ==1:  # if the neighbur is not yet considered (new) 
                                                    #> and since we scaning the min edge then we need this edge for this vertex
               self.treeList[popped.ds].color = 0
               self.treeList[popped.sr].children.add(popped)
               e = Edge(popped.ds,popped.sr, popped.w)
               self.treeList[popped.ds].children.add(e)
               for e in G.vertList[popped.ds].getEdges():
                if self.treeList[e.ds].color == 1:
                    index = e.heapIndex
                    if index == float('inf'):
                        heap.push(e, e.w)
                    else:
                        heap.update(e.w, index)
          
            
    def incMST(self, G, x, y, w):
        e1 = Edge(x, y, w)
        e2 = Edge(y, x, w)
        e1.color = 1
        e2.color = 1
        G.addEdge(x, y, w)
        self.treeList[x].children.add(e1) # adding the edge to the MST (L.2)
        self.treeList[y].children.add(e2)
        path = []
        path = self.Find_path(path, x, x, y)

        max = w
        maxEdge = e1
        path.append(e1)
        for p in path:
            if max<p.w:
                max = p.w
                maxEdge = p
        # deleting maximum edge in the cycle
        for e in self.treeList[maxEdge.sr].getChildren():
            if e.ds == maxEdge.ds:
                self.treeList[maxEdge.sr].children.remove(e)
                break
        for e in self.treeList[maxEdge.ds].getChildren():
            if e.ds == maxEdge.sr:
                self.treeList[maxEdge.ds].children.remove(e)
                break 
        e1.color = 0
        e2.color = 0
        
        
    def Find_path(self, found, s , x, y):
        for e in self.treeList[x].children:
            if (s==e.ds):
                return e
            if e.color == 0:
                e.color = 1

                edge = self.Find_path(found, s, e.ds, y)
                e.color = 0
                if edge:
                    found.append(e)
                    return found
        return found

    def decMST(self, G, x, y, w):
        # remove edges from the graph
        for e in G.vertList[x].edges: 
            if e.ds == y:
                G.vertList[x].edges.remove(e)
                break
        G.vertList[x].remNeighbor(y)
        
        for e in G.vertList[y].edges:
            if e.ds == x:
                G.vertList[y].edges.remove(e)
                break
        
        notTreeEdge = 1
        for e in self.treeList[x].getChildren():
            if e.ds == y:
                e1 = e # memorize the founded edge to be deleted next
                notTreeEdge = 0
        if notTreeEdge:
            return # not a tree edge
        self.treeList[x].children.remove(e1)
        # delete the revirse edge (line.4)
        for e in self.treeList[y].getChildren():
            if e.ds == x:
                self.treeList[y].children.remove(e)
                break
        
        cut_x = cut_y = set()
        min_w = float('inf')  
        min_e = 0#Edge(1,1,10) # making suuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuure
        workSet = set()
        
        workSet.add(self.treeList[x].id)
        while (len(workSet)):
            x = workSet.pop()
            cut_x.add(x)
            self.treeList[x].color = 1
            for e in self.treeList[x].getChildren():
                if self.treeList[e.ds].color ==0:
                    workSet.add(e.ds)
        workSet = cut_x
        while (len(cut_x)):
            x = cut_x.pop()
            if G.vertList[x].getEdges():
                for e in G.vertList[x].getEdges():
                    if self.treeList[e.sr].color != self.treeList[e.ds].color and e.w < min_w:
                        min_w = e.w
                        min_e = e
        if min_e:
            self.treeList[min_e.sr].children.add(min_e)
            min_e2 = Edge(min_e.ds,min_e.sr,min_e.w)
            self.treeList[min_e2.sr].children.add(min_e2)
        while (len(workSet)):
            x = workSet.pop()
            self.treeList[x].color = 0
        

class Edge:

    def __init__(self, s1,s2, key):
        self.sr = s1
        self.ds = s2
        self.w = key
        self.color = 0
        self.heapIndex = float('inf')
    def getSR(self):
        return self.sr



class Heap:
    def __init__(self):
        self.heapList = {}
        self.len = 0

    def shiftUp(self, length):
        child = length
        while child > 0:
            parent=int((child - 1)/ 2)
            if self.heapList[child].w < self.heapList[parent].w:
                flip = self.heapList[child]
                self.heapList[child] = self.heapList[parent]
                self.heapList[parent] = flip

           # update indexes
                self.heapList[child].heapIndex = child
                self.heapList[parent].heapIndex = parent

           # move pointer ups
                child = parent
            else:
                return self

    def shiftDown(self, newV):
        length = self.len - 1

        child = newV * 2 + 1
        while newV * 2 + 1 <= length:
            try:
                child = newV * 2 + 1
                if child + 1 <= length and self.heapList[child].w > self.heapList[child + 1].w:
                    child += 1
                if child <= length and self.heapList[newV].w > self.heapList[child].w:
                    flip = self.heapList[child]
                    self.heapList[child] = self.heapList[newV]
                    self.heapList[newV] = flip

               # update indexes
                    self.heapList[child].heapIndex = child
                    self.heapList[newV].heapIndex = newV
                    newV = child
                else:
                    return self
            except:
                pass

    def push(self, edge, key):
        self.len += 1
        edge = Edge(edge.sr, edge.ds, key)  # new Edge
        edge.heapIndex = self.len - 1
        self.heapList[self.len - 1] = edge
        return self.shiftUp(self.len - 1)

    def update(self, key, index):
        if self.heapList[index].w > key:
            self.heapList[index].w = key
            return self.shiftUp(index)
        else:
            self.heapList[index].w = key
            return self.shiftDown(index)
        return self

    def heap(self):
        return self.len

    def pop(self):
        self.len -= 1
        popped = self.heapList[0]
        popped.heapIndex = float('inf')

        self.heapList[0] = self.heapList[self.len]
        self.shiftDown(0)

        return popped




