#class that incapsulates all possible extensions to the basic collaboration graph
import FileNodeExpansionPack
import numbers

class GraphExpansionPack:

    def __init__(self,baseGraph):
        self.baseGraph = baseGraph
        self.fileNodeExpansion = FileNodeExpansionPack.FileNodeExpansionPack(baseGraph.getNodeIterator(),baseGraph.getNodesList(),baseGraph.getClusterNodesList())

    #expand the base graph with file nodes that give a notion of the isolated files a programmer works on
    #@return a dictionary with the file nodes and edges lists in respectively "nodes" and "edges"
    def expandWithFileNodes(self):
        newNodeIterator = self.fileNodeExpansion.createFileNodes()
        if(isinstance(newNodeIterator,numbers.Number)):
            self.baseGraph.setNodeIterator(newNodeIterator)

        fileNodesList = self.fileNodeExpansion.getNodesList()


        fileEdgesList = self.fileNodeExpansion.getEdgesList()

        clusterFileNodesList = self.fileNodeExpansion.getClusterNodesList()
        

        clusterFileEdgesList = self.fileNodeExpansion.getClusterEdgesList()

        return {"nodes":fileNodesList,"edges":fileEdgesList,"clusternodes": clusterFileNodesList,"clusteredges":clusterFileEdgesList}
