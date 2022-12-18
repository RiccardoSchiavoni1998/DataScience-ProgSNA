#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from operator import itemgetter
from tabulate import tabulate

class GraphViewer():
    def __init__(self, G):
        self.G = G
    
    def setLayout(self, layout):
         match layout:
            case 'circular':
                self.pos = nx.circular_layout(self.G, scale=1, center=None, dim=2)
            case 'spring':
                self.pos = nx.spring_layout(self.G, seed=0)
            case 'shell':
                self.pos = nx.shell_layout(self.G, nlist=None, rotate=None, scale=1, center=None, dim=2)
            case 'random':
                self.pos = nx.random_layout(self.G, center=None, dim=2, seed=None)
            case 'spiral':
                self.pos = nx.spiral_layout(self.G, scale=1, center=None, dim=2, resolution=0.35, equidistant=False)
            case 'kamada_kawai':
                self.pos = nx.kamada_kawai_layout(self.G)
            case 'fruchterman_reingold':
                self.pos = nx.fruchterman_reingold_layout(self.G, dim=2, k=None, pos=None, fixed=None, iterations=50, weight='weight', scale=1.0, center=None)
            case _:
                return 0    
    
    def setColor(self, journal):
        match journal:
            case 'crisis-edges':
                return '#0000FF'
            case 'marsden-edges':
                return '#00FF00'
            case 'poetry-little-review-edges':
                return '#FF0000'
            case 'crisis-edges/marsden-edges':
                return '#00FFFF'
            case 'crisis-edges/poetry-little-review-edges':
                return '#FF00FF'
            case 'marsden-edges/poetry-little-review-edges':
                return '#FFFF00'
            case _:
                return '#000000'
    
    def drawGraph(self, edgesPartitioned=False, nodesPartitioned=False, commonNodes=False):
        if(nodesPartitioned):
            listColor = []
            for n in self.G.nodes():
                journals = []
                for e in self.G.edges(n, data=True):
                    journals.append(e[2]['Journal'])
                journals[:] = list(set(journals))
                if(all(x == journals[0] for x in journals)):
                    listColor.append(self.setColor(journals[0]))
                else:
                    listColor.append(self.setColor(''))
            nx.draw_networkx_nodes(self.G, self.pos, node_color=listColor, node_size=10)
        elif(commonNodes):
            listColor = []
            listSize = []
            for n in self.G.nodes():
                journals = []
                for e in self.G.edges(n, data=True):
                    journals.append(e[2]['Journal'])
                journals[:] = list(set(journals))
                if(len(journals)>1):
                    listColor.append(self.setColor("/".join(sorted(journals))))
                else:
                    listColor.append(self.setColor(''))
            nx.draw_networkx_nodes(self.G, self.pos, node_color=listColor, node_size=10)
        else:
            nx.draw_networkx_nodes(self.G, self.pos, node_color='#000000', node_size=10)
        if(edgesPartitioned):
            for u,v,d in self.G.edges(data=True):
                d['Color'] = self.setColor(d['Journal'])
            edges,colors = zip(*nx.get_edge_attributes(self.G,'Color').items())
            nx.draw_networkx_edges(self.G, self.pos, edge_color=colors, width=1, alpha=0.1)
        else:
            nx.draw_networkx_edges(self.G, self.pos, width=0.5, alpha=0.1)    
            
    def drawClique(self, nodeList):
        nx.draw(self.G.subgraph(nodeList), self.pos, arrows=True, with_labels=True, node_color='#000000', node_size=10, width=0.1, font_size=6)
    
    def drawCentrality(self, values=[], sizeValue=None):
        cent = np.fromiter(values, float)
        sizes = (cent / np.max(cent))*(np.max(cent)* sizeValue)
        normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
        colormap = cm.cool
        scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
        scalarmappaple.set_array(cent)
        nx.draw_networkx_nodes(self.G, self.pos, node_size=sizes, node_color=sizes, cmap=colormap)
        nx.draw_networkx_edges(self.G, self.pos, width=0.5, alpha=0.1)
        fig = plt.gcf()
        plt.colorbar(scalarmappaple)
    
    def drawTableTriads(self, triads):
        col_names = ["Triads", "Weight"]
        print(tabulate(sorted(triads, key=itemgetter(1), reverse = True), headers=col_names, tablefmt="fancy_grid"))
        
    
    def drawTableCentrality(self, dictCentr, centr, perc):
        values = dictCentr.values()
        theshold = max(values)*(perc)
        dataTable = []
        for key,val in zip(dictCentr,values):
            if val >= theshold:
                dataTable.append([key, val])
        col_names = ["Author", centr]
        print(tabulate(sorted(dataTable, key=itemgetter(1), reverse = True), headers=col_names, tablefmt="double_outline"))
    
    def drawDistribution(self, centrDict):
        #sns.displot(centrDict , bins =[0.00, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
        #"count", "density", "percent", "probability", "proportion", "frequency"
        maxVal= round(max(centrDict.values()),2)
        nBin = round(maxVal*20)
        bins=[]
        for x in range(nBin+1):
            bins.append(x/20)
        if(round(maxVal,1)>bins[-1]):
            bins.append(round(maxVal,1))
        ax = sns.histplot(centrDict, bins = bins, color='navy')
        #sns.histplot(centrDict, binrange = [0, round(max(centrDict.values()),1)], bins = 10 , kde=True, stat='count')
        dataTable = []
        for bar, b0, b1 in zip(ax.containers[0], bins[:-1], bins[1:]):
            dataTable.append([str(b0)+ " - " + str(b1), str(bar.get_height())])
        col_names = ["Range", "Count"]
        print(tabulate(dataTable, headers=col_names, tablefmt="fancy_grid"))
        plt.axis('on')
        plt.tight_layout()
        plt.show()
        
    def showLayout(self):
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

