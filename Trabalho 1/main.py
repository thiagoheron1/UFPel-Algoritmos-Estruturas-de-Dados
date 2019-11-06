#!/usr/bin/env python
# coding: utf-8

# #### Imports

# In[ ]:


import sys 
import numpy as np
from collections import defaultdict 
import time
import random


# #### Class Graph

# In[2]:


class Graph(): 
    def __init__(self): 
        # Algoritmo Aproximativo
        self.numberVertex = 0 
        self.matrixAdjacency = []
        
        # DFS
        self.graph = defaultdict(list) 
        
    def readerInputFile(self, nameFile):    
        with open(nameFile) as f:
            file = f.readlines()
            

            # Remove '\n'
            file = ['{0}'.format(line.replace("\n", "")) for line in file]
            #print(file)
            
            # Read/Remove(pop) the first line with numberVertex and numberEdges
            numberVertex, numberEdges = file.pop(0).split()
            numberVertex = int(numberVertex)
            numberEdges = int(numberEdges)

            # Create Numpy Array = Matrix Adjacency
            matrixAdjacency = np.zeros((numberVertex, numberVertex), dtype="int")

            # Update Matrix Adjacency with values of input file
            for line in file:
                line = line.split(" ")
                matrixAdjacency[ int(line[0]) ][ int(line[1]) ] = line[2]
                matrixAdjacency[ int(line[1]) ][ int(line[0]) ] = line[2]
        
        self.matrixAdjacency = matrixAdjacency
        self.numberVertex = len(matrixAdjacency)
    
        # AddEdges em formato de grafo - Algoritmo Solução Otima
        numberLine = 0
        for line in matrixAdjacency:
            numberColumns = 0
            for columns in line:
                if columns != 0:
                    self.addEdge(numberLine, numberColumns)
                numberColumns += 1

            numberLine +=1
    
    def writerInputFile(self, nameFile, numberVertex):
        f = open(nameFile, 'w')
        buff = "%d %d\n" % (numberVertex, numberVertex)
        f.write(buff)

        for i in range (0, numberVertex):
            for j in range (i, numberVertex):
                buff = "%d %d %d\n" % (i, j, random.randint(0, 99))
                f.write(buff)
        f.close()

    # Methods of Approximate Algorithm: Approx-TSP-Tour --------------------------
    def printMST(self, parent): 
        
        # Create a numpy MatrixMST of Zeros
        matrixMST = np.zeros((self.numberVertex, self.numberVertex), dtype="int")
        
        #print("Edge \tWeight")
        for i in range(1, self.numberVertex): 
            #print(parent[i], "-", i, "\t", self.graph[i][ parent[i] ])
            matrixMST[parent[i]][i] = self.matrixAdjacency[i][parent[i]]
            matrixMST[i][parent[i]] = self.matrixAdjacency[i][parent[i]]
        return matrixMST
     
    def minKey(self, key, mstSet): 
        min = sys.maxsize 
        for v in range(self.numberVertex): 
            if key[v] < min and mstSet[v] == False: 
                min = key[v] 
                min_index = v 
        return min_index 

    def algorithmPrim(self): 
        start = time.time()
        key = [sys.maxsize] * self.numberVertex
        parent = [None] * self.numberVertex
        mstSet = [False] * self.numberVertex
        
        key[0] = 0 
        parent[0] = -1 

        for cout in range(self.numberVertex):
            u = self.minKey(key, mstSet) 
            mstSet[u] = True
            for v in range(self.numberVertex): 
                if self.matrixAdjacency[u][v] > 0 and mstSet[v] == False and key[v] > self.matrixAdjacency[u][v]: 
                    key[v] = self.matrixAdjacency[u][v] 
                    parent[v] = u 
        matrixMST = self.printMST(parent) 
        
        #print("MST:\n", matrixMST, "\n")
        end = time.time()
        elapsed = end - start
        print("Time Algorithm Prim:", elapsed)
        return matrixMST       
    
    def cicloEuclidiano(self, MST):

        start = time.time()
        nodesVisited = []
        nodeInitial = random.randint(0, self.numberVertex-1)
        #nodeInitial = 1

        cicloEuclediano = []
        cicloEuclediano.append(nodeInitial)
        stack = []
        allVisited = 0


        while(allVisited != 1):
            nodesVisited.append(nodeInitial)
            #print("nodesVisited", nodesVisited)
            #print("Nodo: ", nodeInitial, "Arestas: ", MST[nodeInitial])
            
            indexNodo = 0
            for aresta in MST[nodeInitial]:

                #print("\t Aresta[", indexNodo,"] = ", aresta)
                if aresta != 0 and (indexNodo not in nodesVisited):
                    cicloEuclediano.append(indexNodo)
                    stack.append(nodeInitial)
                    nodeInitial = indexNodo   
                    break

                try:
                    if (len(MST[nodeInitial])-1) == indexNodo:
                        nodeInitial = stack.pop(len(stack)-1)
                        cicloEuclediano.append(nodeInitial)

                    indexNodo = indexNodo + 1
                except IndexError:
                    allVisited = 1
            #print("\n")
        #print("cicloEuclediano", cicloEuclediano)
        end = time.time()
        elapsed = end - start
        print("Time Euclidean:", elapsed)
        return cicloEuclediano
    
    def cicloHamiltoniano(self, cicloEuclidiano):
        start = time.time()
        cicloHamiltoniano = []
        for nodo in cicloEuclidiano:
            if nodo not in cicloHamiltoniano:
                cicloHamiltoniano.append(nodo)
        #print("cicloHamiltoniano", cicloHamiltoniano)
        end = time.time()
        elapsed = end - start
        print("Time Hamiltoniano:", elapsed)
        return cicloHamiltoniano
        
    # Methods of Algorithm: Depth-First Search -----------------------------------
    def addEdge(self, u, v): 
        self.graph[u].append(v) 

    def DFS(self, start):
        visitedVertex = []
        stack = [start]
        
        vertexList = []
        edgeList = []
        for key, value in self.graph.items():
            vertexList.append(key)
            for adj in value:
                edgeList.append((key, adj))

        adjacencyList = [[] for vertex in vertexList]
        for edge in edgeList:
            adjacencyList[edge[0]].append(edge[1])
        
        start = time.time()
        visited = self.DFSUtil(stack, adjacencyList, visitedVertex)
        end = time.time()
        elapsed = end - start
        print("DFS Time:", round(elapsed, 4))
        return visited
    
    def DFSUtil(self, stack, adjacencyList, visitedVertex):
        while stack:
            current = stack.pop()
            for neighbor in adjacencyList[current]:
                if not neighbor in visitedVertex:
                    stack.append(neighbor)
            visitedVertex.append(current)
        return visitedVertex
        


# In[5]:


# Define name of file
nameFile = "files/graph100.txt"

# Create Graph Object
g = Graph()

# Read and Write Input Files
g.writerInputFile(nameFile, 300)
g.readerInputFile(nameFile)

#print("Matriz de Adjacência:\n", g.matrixAdjacency, "\n")
#print("Formato em Grafo:\n", g.graph, "\n")


# #### Calculate Time

# In[6]:


# Start Time - Approximate Algorithm: Approx-TSP-Tour -----------------
startAll = time.time()

MST = g.algorithmPrim()
Euclidean = g.cicloEuclidiano(MST)
Hamiltoniano = g.cicloHamiltoniano(Euclidean)

endAll = time.time()

print("\tTime Approximate Algorithm:", round(endAll - startAll, 4), "\n---------------------------------")
# End Time - Approximate Algorithm: Approx-TSP-Tour
#------------------------------------------------------------------------

# Calculate DFS
DFS = g.DFS(random.randint(0, g.numberVertex-1))
pass


# #### Output: Approximate Algorithm (Approx-TSP-Tour)

# In[ ]:


#print("MST:\n", MST, "\n-----------------------")
#print("Euclidean:\n", Euclidean, "\n-----------------------")
#print("Hamiltoniano:\n", Hamiltoniano, "\n-----------------------")


# #### Output: Depth-First Search

# In[ ]:


#print("DFS:\n", DFS , "\n-----------------------")


# In[ ]:




