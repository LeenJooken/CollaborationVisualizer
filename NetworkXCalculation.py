import networkx as nx
import operator

class NetworkXCalculation:

    def __init__(self,nodelist,edgelist):
        self.nodelist = nodelist
        self.edgelist = edgelist
        self.betweennessCentrality = {}
        self.eigenvectorCentrality = {}
        self.graph = self.buildGraph()


    #Use the node and edge list to build a networkx graph
    def buildGraph(self):
        graph=nx.Graph()
        #add nodes from a iterable container
        graph.add_nodes_from(self.nodelist)


        #add edges as tuples
        for edge in self.edgelist:
            edgeTuple = edge.getTupleFormat()
            graph.add_edge(*edgeTuple,weight=edge.getWeight())
        return graph


    def calculateBetweennessCentrality(self):
        b=nx.betweenness_centrality(self.graph,None, False, "weight",
                           True, None)

        #normalize based on min and max betweenness centrality instead of using the number of nodes,
        #otherwise the values are way to small to make a real impact
        maxValue = max(b.items(), key=operator.itemgetter(1))[1]
        minValue = min(b.items(), key=operator.itemgetter(1))[1]
        for node,bValue in b.items():
            b[node] = (bValue-minValue)/(maxValue-minValue)

        self.betweennessCentrality = b

    def getBetweennessCentrality(self,node):
        return self.betweennessCentrality[node]


    def calculateEigenvectorCentrality(self):
        centrality = nx.eigenvector_centrality(self.graph,weight="weight")
        #normalize between [0,1]
        maxValue = max(centrality.items(), key=operator.itemgetter(1))[1]
        minValue = min(centrality.items(), key=operator.itemgetter(1))[1]

        for node,eValue in centrality.items():
            centrality[node] = (eValue-minValue)/(maxValue-minValue)

        self.eigenvectorCentrality = centrality


    def getEigenvectorCentrality(self,node):
        return self.eigenvectorCentrality[node]
