#Class that represents an edges between a base graph cluster node and the cluster file node that belongs to it
#Inherits from FileNodeEdge because they represent the same, only the source and target nodes are a different type
import FileNodeEdge


class ClusterFileNodeEdge(FileNodeEdge.FileNodeEdge):
    def __init__(self, clusterFileNode, baseGraphClusterNode):
        super().__init__(clusterFileNode, baseGraphClusterNode)

    def getClusterFileNode(self):
        return(self.getFileNode())

    def getBaseGraphClusterNode(self):
        return(self.getBaseGraphNode())

    def getClusterFileNodeID(self):
        return self.getFileNodeID()

    def getBaseGraphClusterNodeID(self):
        return self.getBaseGraphNodeID()
