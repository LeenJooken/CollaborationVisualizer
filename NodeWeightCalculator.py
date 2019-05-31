import NetworkXCalculation
#This class is designed to calculate the weights of the nodes
#You have to initialize the class with the nodelist and edgesList
#To actually calculate the node weights, call calculateNodeWeights()
class NodeWeightCalculator:
    def __init__(self,nodeList,edgesList):
        self.nodeList = nodeList
        self.edgesList = edgesList
        self.networkXCalculation = NetworkXCalculation.NetworkXCalculation(nodeList,edgesList)

        #weight matrix for the metrics, used to calculate the end weight
        self.FSW = 0.15
        self.BCW = 0.25
        self.ECW = 0.30
        self.DCW = 0.30

    def calculateNodeWeights(self):
        #calculate the betweenness centrality
        self.networkXCalculation.calculateBetweennessCentrality()
        self.networkXCalculation.calculateEigenvectorCentrality()
        for node in self.nodeList:
            freqSign = self.calculateFrequencySignificance(node)
            betwCentr = self.calculateBetweennessCentrality(node)
            eigenvectorCentr = self.calculateEigenvectorCentrality(node)
            degreeCentr = self.calculateDegreeCentrality(node)

            weight = self.FSW*freqSign + self.BCW*betwCentr + self.ECW*eigenvectorCentr + self.DCW*degreeCentr

            node.setWeight(weight)


    #function that calculates the frequency significance:
    #unary significance metric from Fuzzy Mining: relative importance of node
    #the more often a node is mentioned in the log, the more important it is:
    #but you can choose how often you commit ex. 1 large commit or several smaller commits
    #So we look at how many files that person worked on
    #6 situations but we cant tell whether a file is big or important
    #Important: if regularly modified with a timespan of at least 1 month in between modifications

    def calculateFrequencySignificance(self,node):
        files = node.getDistinctFileList()
        #take the sum of the file importances
        importance = 0

        for file in files:
            importance += file.getImportance()

        #normalize the importance: the importance of each file ]0,1]
        #so just divide it by the number of files
        importance = importance/len(files)


        return importance

    #function that calculate the betweenness centrality:
    #Graph theory centrality measure
    #= number of shortest paths that pass through the vertex
    #high value if node is important gatekeeper of info between disparate parts of the graph
    #So in our case: shows people that form a connection between many seperate collab teams
    def calculateBetweennessCentrality(self,node):
        betweenCentr = self.networkXCalculation.getBetweennessCentrality(node)
        return betweenCentr

    def calculateEigenvectorCentrality(self,node):
        eigenvCentr = self.networkXCalculation.getEigenvectorCentrality(node)
        return eigenvCentr

    #Function that calculates the degree centrality
    #Graph theory metric
    #The number of links incident on the node
    #The less people the node collabs with, the more important he is
    #'cause he's the only one with knowledge of this code
    #This combined with frequency significance (the importance and number of the files)
    #Can uncover dangerous nodes: only nodes with knowledge about very important code parts
    #Algorithm:
    #number of nodes they are NOT connected to / number they can possibly be connected to (n=-1)
    #PROBLEM! : separate metric for pair programming vs distinct edges?
    def calculateDegreeCentrality(self,node):

        degreeCentr = 0
        numberOfNodes = len(self.nodeList)
        distinctDegreeCentr = self.calculateDistinctDegreeCentrality(node,numberOfNodes)
        pairProgDegreeCentr = self.calculatePairProgDegreeCentrality(node,numberOfNodes)
        degreeCentr = distinctDegreeCentr - pairProgDegreeCentr
        #result could lay between [-1,1] -> normalize to [0,1]
        #normalization
        degreeCentr = (degreeCentr+1)/2


        return degreeCentr

    #Function that calculates the degree centrality solely for distinct edges (so no pair programming edges are taken into account)
    #Algorithm:
    #number of nodes they are NOT connected to (= n-1 - number they ARE connected to)
    #divided by
    #number of nodes they could be connected to (=n-1)
    #Or simplified formula = 1 - ((number they are connected to)/(n-1))
    def calculateDistinctDegreeCentrality(self,node,numberOfNodes):
        numberOfIncidentLinks = self.countIncidentDistinctLinks(node)
        distinctDegreeCentr = 1-(numberOfIncidentLinks/(numberOfNodes-1))
        return distinctDegreeCentr

    #Function that counts the number of incident links on node (non pair programming)
    def countIncidentDistinctLinks(self,node):
        count = 0
        for edge in self.edgesList:
            if((edge.containsNode(node))and(edge.getIfDistinctCollab())):
                count += 1
        return count

    #Function that calculates the degree centrality of pair programming edges only
    #Algorithm:
    #Number of nodes they are connected to / number of nodes they could be connected to (=n-1)
    #Note: this one does not calculate the inverse like the distinct function,
    #This because we will later subtract this value
    def calculatePairProgDegreeCentrality(self,node,numberOfNodes):
        numberOfIncidentLinks = self.countIncidentPairProgLinks(node)
        pairProgDegreeCentr = numberOfIncidentLinks / (numberOfNodes - 1)
        return pairProgDegreeCentr

    def countIncidentPairProgLinks(self,node):
        count = 0
        for edge in self.edgesList:
            if((edge.containsNode(node)) and (edge.getIfPairProgramming())):
                count += 1
        return count
