#Class that represents a cluster of nodes


class Cluster:

    def __init__(self,initNode=None,initEdge=None):
        self.nodeslist = []
        if(initEdge is not None):
            self.nodeslist.append(initNode)
        self.edgeslist = []
        if(initEdge is not None):
            self.edgeslist.append(initEdge)

    #check if the node is part of this cluster
    def containsNode(self,node):
        if(node in self.nodeslist):
            return True
        return False

    def getNodes(self):
        return self.nodeslist

    def getEdges(self):
        return self.edgeslist

    #add this node to the cluster
    def addNode(self,node):
        if node not in self.nodeslist:
            self.nodeslist.append(node)

    #add this edge to the cluster
    def addEdge(self,edge):
        if not edge in self.edgeslist:
            self.edgeslist.append(edge)

    #function that scans the edge list & returns the nodes that aren't in this cluster
    #but are neighbours
    #@return dictionary with node as key and the edge it is part off as value
    def getNeighbourAggrNodes(self):
        neighbours = {}
        for edge in self.edgeslist:
            nodes = edge.getTupleFormat()
            if (nodes[0] not in self.nodeslist):
                neighbours[nodes[0]] = edge
            if (nodes[1] not in self.nodeslist):
                neighbours[nodes[1]] = edge
        return neighbours
