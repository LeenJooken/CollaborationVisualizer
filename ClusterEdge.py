#This class represents an edge that goes from an outside node to a cluster

class ClusterEdge:


    def __init__(self,sourceNode,targetCluster,interClusterEdge,collabType,weight):
        self.sourceNode = sourceNode
        self.targetCluster = targetCluster
        self.weight = weight
        self.type = "Undirected"
        self.collaborationType = collabType
        #boolean that says whether the source node is also a cluster
        self.interClusterEdge = interClusterEdge

    def getSourceNodeID(self):
        return self.sourceNode.getID()

    def isSourceNode(self,node):
        return(self.sourceNode == node)

    def getTargetClusterID(self):
        return self.targetCluster.getID()

    def getIfInterClusterEdge(self):
        return self.interClusterEdge

    def getWeight(self):
        return self.weight

    def getType(self):
        return self.type

    def getCollaborationType(self):
        return self.collaborationType

    def isBetweenTheseTwoClusters(self,cluster1,cluster2):
        if((self.sourceNode == cluster1) and(self.targetCluster == cluster2)):
            return True
        elif ((self.targetCluster == cluster1) and (self.sourceNode == cluster2)):
            return True
        return False
