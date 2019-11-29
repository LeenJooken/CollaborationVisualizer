#class for adding file nodes to the base graph
import FileNode
import FileNodeEdge
import ClusterFileNode
import ClusterFileNodeEdge
import Graph

class FileNodeExpansionPack:
    def __init__(self,nodeIterator,baseGraphNodes,baseGraphClusterNodes):
        #The file nodes
        self.nodesList = []
        self.edgesList = []
        self.baseGraphNodes = baseGraphNodes

        #The cluster file nodes
        self.clusterNodesList = []
        self.clusterEdgesList = []
        self.baseGraphClusterNodes = baseGraphClusterNodes

        #startpoint for unique node ID
        self.nodeIterator = nodeIterator
        self.nodeWeightThreshold = 0.1   #experimental, can be a user set param


    def getNodesList(self):
        return self.nodesList

    def getEdgesList(self):
        return self.edgesList

    def getClusterNodesList(self):
        return self.clusterNodesList

    def getClusterEdgesList(self):
        return self.clusterEdgesList


    #Function that creates the file nodes
    #@return the updated node iterator
    def createFileNodes(self):

        self.createRegularFileNodes()
        self.createClusterFileNodes()

        #If there are no file nodes
        if(not self.nodesList and not self.clusterNodesList):
            return

        #normalize the node weights
        self.normalizeNodeWeights()

        self.applyWeightThreshold()




        return self.nodeIterator

    #Function that keep only the (cluster) file nodes with a weight > threshold
    def applyWeightThreshold(self):

        #keep only the file nodes with a weight > threshold
        helplist = [x for x in self.nodesList if x.getWeight() >= self.nodeWeightThreshold]
        self.nodesList = helplist[:]
        #remove the filenode edges that arent needed anymore
        helplist2 = [x for x in self.edgesList if x.getFileNode() in self.nodesList]
        self.edgesList = helplist2[:]

        helplist3 = [x for x in self.clusterNodesList if x.getWeight() >= self.nodeWeightThreshold]
        self.clusterNodesList = helplist3[:]
        helplist4 = [x for x in self.clusterEdgesList if x.getClusterFileNode() in self.clusterNodesList]
        self.clusterEdgesList = helplist4[:]


    #Function that creates the regular file nodes
    def createRegularFileNodes(self):
        counter = 0
        #for every programmer node, make file node and an edge connecting the base node and file node
        for node in self.baseGraphNodes:
            filenode = FileNode.FileNode(self.nodeIterator,node)
            #only add the node if it contains files (weight must be > 0)
            if(filenode.getWeight() > 0):
                self.nodesList.append(filenode)
                self.nodeIterator += 1
                counter+= 1

                #create an edge connecting the two
                self.edgesList.append(FileNodeEdge.FileNodeEdge(filenode,node))



    #Function that creates the cluster file nodes
    def createClusterFileNodes(self):
        counter = 0
        #for every cluster node, make a file cluster node and an edge connecting the base cluster node and the file cluster node
        for clusterNode in self.baseGraphClusterNodes:
            clusterFileNode = ClusterFileNode.ClusterFileNode(self.nodeIterator,clusterNode)
            #only add the node if it contains files (weight must be > 0)
            if(clusterFileNode.getWeight() > 0):
                self.clusterNodesList.append(clusterFileNode)
                self.nodeIterator += 1
                counter+= 1

                #create an edge connecting the two
                self.clusterEdgesList.append(ClusterFileNodeEdge.ClusterFileNodeEdge(clusterFileNode,clusterNode))



    #Function to normalize the file node weights for both the regular and the cluster nodes between [0,max node weight]
    #We chose to make the nodes proportionate to the max node weight from the graph, to better balance out the visualisation
    #(Note that the weights of the base nodes were also normalized between [0,1])
    #Approach: normalize the (cluster) file node weights between [0,1] and multiply by the max node weight
    def normalizeNodeWeights(self):

        #get weight range of file nodes (both cluster and regular)
        fileNodeWeightList = self.getFileNodeWeightList()

        minFileNodeWeight = min(fileNodeWeightList)
        maxFileNodeWeight = max(fileNodeWeightList)
        maxNodeWeight = self.getMaxNodeWeight()

        #normalize between [0,1]
        for filenode in self.nodesList:
            if(minFileNodeWeight != maxFileNodeWeight):
                normWeight = ((filenode.getWeight() - minFileNodeWeight)/(maxFileNodeWeight - minFileNodeWeight))
            else:
                #very exceptional case that every node has the same weight or the list just consists of 1 node
                normWeight = 1/len(self.nodesList)
            #proportionate to the max base graph node weight
            normWeight *= maxNodeWeight
            filenode.setWeight(normWeight)

        for clusterfilenode in self.clusterNodesList:
            if(minFileNodeWeight != maxFileNodeWeight):
                normWeight = ((clusterfilenode.getWeight() - minFileNodeWeight)/(maxFileNodeWeight - minFileNodeWeight))
            else:
                #in the case that every node has the same weight or the list just consists of 1 node
                normWeight = 1/len(self.clusterNodesList)
            #proportionate to the max base graph node weight
            normWeight *= maxNodeWeight
            clusterfilenode.setWeight(normWeight)


    #Function that returns a list of all the weights of the file nodes (both regular and cluster)
    def getFileNodeWeightList(self):
        weights = []

        for node in self.nodesList:
            weights.append(node.getWeight())
        for node in self.clusterNodesList:
            weights.append(node.getWeight())
        return weights

    #Function that returns the max weight of all the base graph nodes and cluster nodes
    def getMaxNodeWeight(self):
        weights = []
        for node in self.baseGraphNodes:
            weights.append(node.getWeight())
        for node in self.baseGraphClusterNodes:
            weights.append(node.getWeight())

        return max(weights)
