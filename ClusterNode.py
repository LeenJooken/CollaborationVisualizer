#Class that represents a cluster of nodes

class ClusterNode:

    def __init__(self,nodes,inClusterEdges,outClusterEdges,neighbours):
        #nodes that are a part of this cluster
        self.nodeslist = nodes
        #ID should be unique, so give it the ID of the first node
        self.ID = nodes[0].getID()

        #edges between the nodes of this cluster
        #so source and target are both nodes that are in this cluster
        #and the edges will not show up on the final graph
        self.inClusterEdgeslist = inClusterEdges
        #list of edges that start from one of the cluster nodes and go to
        #a target node outside the cluster
        self.outClusterEdgeslist = outClusterEdges
        #list of these target nodes, which the cluster is connected to
        #These target nodes could belong to another cluster !!!! So WATCH OUT
        self.neighbours = neighbours
        self.weight = self.calculateWeightCorrected()
        self.label = self.constructLabel()

    def getWeight(self):
        return self.weight

    def getID(self):
        return self.ID

    def getClusterNodes(self):
        return self.nodeslist

    def getNumberOfMembers(self):
        return len(self.nodeslist)

    def getLabel(self):
        return self.label

    def getInClusterEdges(self):
        return self.inClusterEdgeslist

    def getOutClusterEdges(self):
        return self.outClusterEdgeslist

    def getNeighbours(self):
        return self.neighbours

    #@return true if this node is part of the cluster
    def containsNode(self,node):
        return(node in self.nodeslist)

    #check if a node with this label is in this cluster
    def contrainsNodeByLabel(self,nodeName):
        for node in self.nodeslist:
            if(node.getLabel == nodeName):
                return True
        return False


    def calculateWeight(self):
        weight = 0
        for node in self.nodeslist :
            weight += node.getWeight()
        weight = weight / len(self.nodeslist)
        return weight

    #calculates the avg weight and corrects it with the weight of the most important node
    def calculateWeightCorrected(self):
        avgWeight = self.calculateWeight()
        #find heaviest node
        heaviest = -1
        for node in self.nodeslist:
            if(node.getWeight() > heaviest):
                heaviest = node.getWeight()
        finalWeight = (avgWeight + heaviest )/2
        return finalWeight

    def constructLabel(self):
        #just paste all the node labels together
        label = ""
        count = 0
        for node in self.nodeslist:
            if(count != 0):
                label += "+"
            label += node.getLabel()
            count += 1
        return label

    #returns all the edges that start in this cluster and connect to this neighbour outside the cluster
    def getOutEdgesForNeighbour(self,neighbour):
        list = []
        for edge in self.outClusterEdgeslist:
            if(edge.containsNode(neighbour)):
                list.append(edge)

        return list

    def getListOfProgrammers(self):
        prog = []
        for node in self.nodeslist:
            prog.append(node.getProgrammer())
        return prog
