#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import networkx as nx
from itertools import combinations

class GraphBuilder():
    
    def createGraph(self, fileName):
        self.G = nx.from_pandas_edgelist(pd.read_csv(fileName), 'Source', 'Target', ['Weight', 'Journal'], create_using=nx.Graph())
        
    def getGraph(self):
        return self.G 
    
    def filterEdges(self, minWeight):
        removeEdges = [(u, v) for (u, v, d) in self.G.edges(data=True) if d["Weight"] < minWeight]
        self.G.remove_edges_from(removeEdges)
    
    def filterNodes(self, minDegree):
        removeNodes=[]
        for n in self.G.degree:
            if n[1] < minDegree: removeNodes.append(n[0])
        self.G.remove_nodes_from(removeNodes)
    
    def findTriads(self, minWeight):
        triads = []
        for comb in combinations(self.G.nodes, 3):
            subGraph = self.G.subgraph(comb)
            if(subGraph.number_of_edges()==3): 
                aux = 0
                for elem in subGraph.edges(data=True):
                    aux += elem[2]['Weight']
                if(aux>=minWeight):
                    triads.append([subGraph.nodes(), aux])
        return triads
    
    def findMaxClique(self):
        cliques = nx.find_cliques(self.G)
        max = 0
        for clique in cliques:
            if(len(clique)>max):
                max=len(clique)
                maxClique=clique
        return maxClique
                
    def analyzeCentrality(self, centrality):
        match centrality:
            case 'degree':
                return nx.degree_centrality(self.G)
            case 'betweenness':
                return nx.betweenness_centrality(self.G, weight=None, normalized=True)
            case 'closeness':
                return nx.closeness_centrality(self.G)
            case 'eigenvector':
                return nx.eigenvector_centrality(self.G)
            case _:
                return [] 


