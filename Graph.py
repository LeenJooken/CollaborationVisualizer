import Node
import Programmer
import Edge
import NodeWeightCalculator
import EdgeCalculator
import EdgeWeightCalculator
import GraphSimplification
#class that represents the social graph,
#contains a node and edge list
class Graph:

    #@param listOfProgrammers is a list of Programmer objects
    def __init__(self,listOfProgrammers,listOfCommits,nodeIterator):
        self.nodeslist = []
        self.edgeslist = []
        self.clusterNodeslist = []
        self.clusterEdgeslist = []
        self.nodeIterator = nodeIterator

        self.constructGraph(listOfProgrammers,listOfCommits)


    def getNodesList(self):
        return self.nodeslist

    def getEdgesList(self):
        return self.edgeslist

    def getClusterNodesList(self):
        return self.clusterNodeslist

    def getClusterEdgesList(self):
        return self.clusterEdgeslist

    def getNodeIterator(self):
        return self.nodeIterator

    def setNodeIterator(self,newIterator):
        if(newIterator > self.nodeIterator):
            self.nodeIterator = newIterator

    def addNodeToList(self,node):
        self.nodeslist.append(node)

    def addEdgeToList(self,edge):
        self.edgeslist.append(edge)

    #searches for node with that ID in the nodelist and returns it
    #@param ID = the id of the node you're searching for
    #@returns the node
    def getNodeByID(self,id):
        node = [target for target in self.nodeslist if target.getID()==id]
        return node[0]

    def getEdgeByID(self,sourceNodeID,targetNodeID):
        #edge could be (source,target) or (target,source)
        for edge in self.edgeslist:
            sID = edge.getSourceNodeID()
            tID = edge.getTargetNodeID()
            if(((sID == sourceNodeID)and(tID == targetNodeID))or((sID == targetNodeID)and(tID == sourceNodeID))):
                return edge

    #build the nodes list
    def buildNodesList(self,programmers):

        #include all programmers and set the weight default at 1
        #build the list
        for prog in programmers:
            self.addNodeToList(Node.Node(prog,1))



    #build the edges list
    def buildEdgesList(self,commits,programmers):
        #build the pair programming edges
        edgecalc = EdgeCalculator.EdgeCalculator(commits,programmers)
        #returns dictionary with source and target nodes IDs as key + weight as value
        print("   Building the pair programming edges")
        edgeDict = edgecalc.getPairProgrammingEdges()
        self.addPairProgrammingEdgesToList(edgeDict)

        #build all other edges apart from pair programming
        print("   Building the disjunct collaboration edges")
        edgeDict2 = edgecalc.getDisjunctColloborationEdges()
        self.addDisjunctCollaborationEdgesToList(edgeDict2)


    #creates edges for the pairprogramming pairs
    def addPairProgrammingEdgesToList(self,pairs):
        for IDs, info in pairs.items():
            edge = Edge.Edge(self.getNodeByID(IDs[0]),self.getNodeByID(IDs[1]))
            edge.setPairProgrammingWeight(info['weight'])
            edge.setPairProgCommitList(info['commits'])
            self.addEdgeToList(edge)


    def addDisjunctCollaborationEdgesToList(self,pairs):
        for IDs, info in pairs.items():
            #check first if edge already exists
            edge = self.getEdgeByID(IDs[0],IDs[1])
            if not isinstance(edge,Edge.Edge):
                #edge does not exist yet, make one
                edge = Edge.Edge(self.getNodeByID(IDs[0]),self.getNodeByID(IDs[1]))
                self.addEdgeToList(edge)
            else:
                #it's possible that source & target node are switched, so make sure it is set right
                #this is to make sure that the order of commit tuples is correct
                edge.resetSourceAndTargetNodes(self.getNodeByID(IDs[0]),self.getNodeByID(IDs[1]))

            edge.setDisjunctCollabCommitList(info['commits'])
            edge.setDistinctProgramming()

    #calculates the weights for the nodes using adapted versions of:
    #frequency significance
    #betweenness centrality
    #eigenvector centrality
    #degree centrality
    def calculateNodeWeights(self):
        nodecalc = NodeWeightCalculator.NodeWeightCalculator(self.nodeslist,self.edgeslist)#,self.totalImportanceAllFiles)
        nodecalc.calculateNodeWeights()

    #calculates the weights for the edges, making use of
    #frequency significance
    #proximity correlation
    def calculateEdgeWeights(self):
        edgecalc = EdgeWeightCalculator.EdgeWeightCalculator(self.edgeslist)
        edgecalc.calculateEdgeWeights()

        #Clean up the edges: delete edges with a weight of 0
        self.cleanUpEdges()

    #Function that deletes all edges with a weight of 0
    def cleanUpEdges(self):

        self.edgeslist = [edge for edge in self.edgeslist if edge.getWeight() != 0]


    #constructs the graph: builds node & edges list
    def constructGraph(self,programmers,commits):
        #build the base graph
        print("Building the nodes list")
        self.buildNodesList(programmers)
        print("Building the edges list")
        self.buildEdgesList(commits,programmers)


        #calculate the weights
        print("Calculating the edge weights")
        self.calculateEdgeWeights()
        print("Calculating the node weights")
        self.calculateNodeWeights()

        #simplyfiy the graph
        print("Simplifying the graph")
        self.graphSimplification()



    #simplify the graph
    def graphSimplification(self):
        simplifier = GraphSimplification.GraphSimplification(self.nodeslist,self.edgeslist)
        simplifier.simplifyGraph()
        self.nodeslist = simplifier.getNodesList()
        self.edgeslist = simplifier.getEdgesList()
        self.clusterNodeslist = simplifier.getClusterNodesList()
        self.clusterEdgeslist = simplifier.getClusterEdgesList()

    


    #function that deletes the node from the graph,
    #including its incident links
    def deleteNodeFromGraph(self,nodeID):
        node = self.getNodeByID(nodeID)

        #delete now all incident edges
        self.edgeslist = [edge for edge in self.edgeslist if not edge.containsNode(node)]

        #delete the node from the nodeslist
        self.nodeslist.remove(node)
