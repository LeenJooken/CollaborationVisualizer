#class that represents an edge that connects a node in the base graph with a file node

class FileNodeEdge:
        def __init__(self,fileNode,baseGraphNode):
            self.fileNode = fileNode
            self.baseGraphNode = baseGraphNode
            self.weight = 0.2 #adjust this weight to determine the thickness in the visualization, has no other use!!
            self.type = "Undirected"
            self.collaborationType = "NA"


        def getWeight(self):
            return self.weight

        def getType(self):
            return self.type

        def getCollaborationType(self):
            return self.collaborationType

        def getFileNode(self):
            return self.fileNode

        def getBaseGraphNode(self):
            return self.baseGraphNode

        def getFileNodeID(self):
            return self.fileNode.getID()

        def getBaseGraphNodeID(self):
            return self.baseGraphNode.getID()
