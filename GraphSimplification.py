#Class that handles the graph simplification
#Based the Fuzzy Mining Adaptive Graph Simplification technique
#1. Conflict Resolution -> not applicable
#2. Edge Filtering
#3. Node Aggregation and Abstraction
import operator
import Edge
import Node
import Cluster
import ClusterNode
import ClusterEdge

class GraphSimplification:

    def __init__(self,nodes,edges):
        self.nodeslist = nodes
        self.edgeslist = edges
        self.cutoffParam = 0.5
        self.aggregationVictimParam = self.calculateAggregationVictimParam()
        self.aggregationCorrelationParam = self.calculateAggregationCorrelationParam(self.aggregationVictimParam)
        self.abstractionVictimParam = self.aggregationVictimParam
        self.abstractionCorrelationParam = self.aggregationCorrelationParam

        self.clusterlist = []
        self.recursiveHelp = []
        self.clusterNodeslist = []
        self.clusterEdgeslist=[]

    def getNodesList(self):
        return self.nodeslist

    def getEdgesList(self):
        return self.edgeslist

    def getClusterEdgesList(self):
        return self.clusterEdgeslist

    def getClusterNodesList(self):
        return self.clusterNodeslist

    def calculateAggregationVictimParam(self):
        weight = 0
        for node in self.nodeslist:
            weight += node.getWeight()
        cutoff = weight / len(self.nodeslist)
        return cutoff

    def calculateAggregationCorrelationParam(self,avgNodeWeight):
        weight = 0
        for edge in self.edgeslist:
            weight += edge.getWeight()
        avgEdgeWeight = weight/len(self.edgeslist)
        corrParam = abs(avgNodeWeight - avgEdgeWeight)
        return corrParam

    #We need the local differences between a node and an incident edge
    #the corrParam will be the avg of these differences
    def calculateAggregationCorrelationParam2(self):
        localDifferences = []
        for node in self.nodeslist:
            edges = self.collectIncidentEdges(node)
            for edge in edges:
                difference = abs(node.getWeight() - edge.getWeight())
                localDifferences.append(difference)
        corrParam = sum(localDifferences)/len(localDifferences)
        return corrParam

    def simplifyGraph(self):
        #Edge Filtering
        self.edgeFiltering()
        #Aggregation
        self.aggregation()
        #Abstraction
        self.abstraction()


    #Only possible for nodes that have >1 edge
    #So at least 1 edge is always preserved and those edges are the most important ones for that node
    #It's not possible to create new isolated nodes, so this step won't mess up the rest of the simplification
    #We use the edge weight as the utility value
    def edgeFiltering(self):
        filterTheseEdges = {}
        #check every node
        for node in self.nodeslist:
            #collect all incident edges
            incidentEdges = self.collectIncidentEdges(node)
            #if it has > 1 edge:
            if(len(incidentEdges)>1):
                #calculate which edges to filter
                candidateEdges = self.calculateWhichEdgesToFilter(incidentEdges)
                #check if the target node is OK with filtering this edge
                #check if it isnt the only incident edge on the target node -> DO NOT REMOVE


                for candidate in candidateEdges:
                    #edge already as candidate filter
                    if candidate in filterTheseEdges:
                        filterTheseEdges[candidate] = True


                    else:
                        #only when both nodes agree that the edge can be filtered, we're filtering it
                        filterTheseEdges[candidate] = False




        #now filter all the edges that have a true value
        self.filterEdges(filterTheseEdges)



    #Function that filters the edges from the edge list
    def filterEdges(self,filterTheseEdges):
        for edge,filter in filterTheseEdges.items():

            if(filter):
                self.edgeslist.remove(edge)



    #@returns list of candidate edges to filter
    def calculateWhichEdgesToFilter(self,incidentEdges):
        #collect the edge weights
        helpDict = {}
        weightlist = []
        for edge in incidentEdges:
            weightlist.append(edge.getWeight())


        #normalize the weights
        maxValue = max(weightlist)
        minValue = min(weightlist)

        #if not all edges have the same weight
        if (maxValue != minValue):
            for edge in incidentEdges:
                helpDict[edge] = (edge.getWeight() - minValue)/(maxValue-minValue)


        filterTheseEdges = []
        for edge,normWeight in helpDict.items():

            if(normWeight < self.cutoffParam):
                filterTheseEdges.append(edge)



        return filterTheseEdges

    #Collect all edges incident on the node
    #@param node = node of which we want the incident edges
    #@returns list of incident edges
    def collectIncidentEdges(self,node):
        incidentEdges = []
        for edge in self.edgeslist:
            if(edge.containsNode(node)):
                incidentEdges.append(edge)


        return incidentEdges


    #Aggregation: coherent clusters of low-level info combined to 1
    #Nodes that aren't very important but have strong relations -> cluster
    def aggregation(self):
        #Phase 1: build the inital clusters
        self.initialClusterBuilding()
        #Phase 2: merge the clusters built in phase 1
        clustersToBuild = self.clusterMerging()
        #Phase 3: build the graph cluster nodes
        self.clusterNodeslist = self.buildClusterNodes(clustersToBuild)
        self.clusterNodesCleanup()
        #clean up the edges within & that lead to a cluster
        self.clusterEdgesCleanup()

    #Delete all the nodes that are now part of a cluster from the nodes list
    def clusterNodesCleanup(self):
        for cluster in self.clusterNodeslist:
            nodes = cluster.getClusterNodes()
            #delete these from the nodes list
            self.nodeslist = [x for x in self.nodeslist if x not in nodes]


    #clean up the edges list so edges within a cluster are not included anymore
    #and edge from outside a cluster to a cluster are correctly connected
    def clusterEdgesCleanup(self):
        for cluster in self.clusterNodeslist:
            #remove edges within the cluster from the edges list
            inEdges = cluster.getInClusterEdges()
            inEdgesRemoved = [x for x in self.edgeslist if x not in inEdges]
            #now correctly connect outEdges to the cluster
            outEdges = cluster.getOutClusterEdges()
            neighbours = cluster.getNeighbours()
            #create new cluster edges
            for neighbour in neighbours:
                #################
                #check if neighbour belongs to a cluster
                neighbourClusterNode = self.belongsNodeToClusterNode(neighbour)
                if(isinstance(neighbourClusterNode,ClusterNode.ClusterNode)):
                    #this is an edge between 2 clusters
                    #this means that it will be asked 2 times, so we need to check if this edge already exists
                    interClusterEdge = self.checkIfInterClusterEdgeExists(cluster,neighbourClusterNode)
                    if(not isinstance(interClusterEdge,ClusterEdge.ClusterEdge)):
                        #no edge does not yet exist, make a new one
                        #determine the collaboration type
                        collabType = self.determineCollaborationTypeClusterEdge(neighbourClusterNode,cluster)
                        clusterEdgeWeight = self.determineClusterEdgeWeightClusterEdge(neighbourClusterNode,cluster)
                        newClusterEdge = ClusterEdge.ClusterEdge(neighbourClusterNode,cluster,True,collabType,clusterEdgeWeight)
                        self.clusterEdgeslist.append(newClusterEdge)
                #node to cluster edge
                else:
                    #determine the collaboration type of this new edge
                    collabType = self.determineCollaborationType(outEdges,neighbour)
                    clusterEdgeWeight = self.determineClusterEdgeWeight(cluster.getOutEdgesForNeighbour(neighbour))
                    newClusterEdge = ClusterEdge.ClusterEdge(neighbour,cluster,False,collabType,clusterEdgeWeight)
                    self.clusterEdgeslist.append(newClusterEdge)
                #############
            #then delete all the original edges
            inAndOutEdgesRemoved = [x for x in inEdgesRemoved if x not in outEdges]
            self.edgeslist = inAndOutEdgesRemoved


    #Calculates the weight for a clusteredge as follows:
    #Calculate the avg weight over all edges
    # add the heaviest edge again and divide by 2
    def determineClusterEdgeWeight(self,edges):
        totalWeight = 0
        maxWeight = -1
        for edge in edges:
            weight = edge.getWeight()
            totalWeight += weight
            if(weight > maxWeight):
                maxWeight = weight
        #calculate avg weight
        avgWeight = totalWeight / len(edges)
        finalWeight = (avgWeight + maxWeight)/2
        return finalWeight

    #Collect all edges between these 2 clusters and base the calculation of the final weight on this
    def determineClusterEdgeWeightClusterEdge(self,neighbourCluster, cluster):
        outEdges = cluster.getOutClusterEdges()
        nodes = neighbourCluster.getClusterNodes()
        totalWeight = 0
        maxWeight = -1
        counter = 0

        for edge in outEdges:
            tuple = edge.getTupleFormat()
            if((tuple[0] in nodes) or (tuple[1] in nodes)):
                weight = edge.getWeight()
                totalWeight += weight
                counter += 1
                if(weight > maxWeight):
                    maxWeight = weight
        avgWeight = totalWeight / counter
        finalWeight = (avgWeight + maxWeight)/2
        return finalWeight



    #Function that determines the collaboration type of a clusterEdge
    #@param outEdges = list of edges that start from a node outside the cluster and connect to a node within the cluster
    #@param node = the node outside the cluster
    #Calculation:
    #check if one of the nodes is the node we're searching for
    #check the type of the edges connected to this node
    #if 1 edge is distinct & pair -> clusterEdge = distinct & edge
    #else if all edges are distinct -> clusterEdge = distinct
    #else if all edges are pair -> clusterEdge = pair
    #else -> distinct & pair
    def determineCollaborationType(self,outEdges,node):
        numberOfPair = 0
        numberOfDistinct = 0
        for edge in outEdges:
            #check if it is a relevant edge
            if(edge.containsNode(node)):
                type = edge.getCollaborationType()
                if(type == "Pair and disjunct programming"):
                    return type
                elif(type == "Pair programming"):
                    numberOfPair += 1
                elif(type == "Disjunct programming" ):
                    numberOfDistinct += 1

        finalType = "unknown"
        #check which type it is
        if((numberOfPair > 0) and (numberOfDistinct > 0)):
            finalType = "Pair and disjunct programming"
        elif((numberOfPair > 0) and (numberOfDistinct == 0)):
            finalType =  "Pair programming"
        elif ((numberOfPair == 0) and(numberOfDistinct > 0)):
            finalType = "Disjunct programming"

        return finalType

    #Function that determines the collaboration type for the edge between these 2 clusters
    #Calculation:
    #get all the nodes from one cluster and the outedges of the other
    #for every edge check if the target node is a member of the other cluster
    #if so: take the collabtype into consideration
    def determineCollaborationTypeClusterEdge(self,cluster1,cluster2):
        numberOfPair = 0
        numberOfDistinct = 0
        nodes = cluster1.getClusterNodes()
        outEdges = cluster2.getOutClusterEdges()
        for edge in outEdges:
            tuple = edge.getTupleFormat()
            #does this edge connect the 2 clusters?
            if((tuple[0] in nodes) or (tuple[1] in nodes)):
                type = edge.getCollaborationType()
                if(type == "Pair and disjunct programming"):
                    return type
                elif(type == "Pair programming"):
                    numberOfPair += 1
                elif(type == "Disjunct programming" ):
                    numberOfDistinct += 1

        finalType = "unknown"
        #check which type it is
        if((numberOfPair > 0) and (numberOfDistinct > 0)):
            finalType = "Pair and disjunct programming"
        elif((numberOfPair > 0) and (numberOfDistinct == 0)):
            finalType =  "Pair programming"
        elif ((numberOfPair == 0) and(numberOfDistinct > 0)):
            finalType = "Disjunct programming"

        return finalType

    #function that checks wether and edge between these 2 clusters already exists in the clusterEdgelist
    def checkIfInterClusterEdgeExists(self,cluster1,cluster2):
        for edge in self.clusterEdgeslist:
            #check if it is an edge between 2 clusters
            if(edge.getIfInterClusterEdge()):
                if(edge.isBetweenTheseTwoClusters(cluster1,cluster2)):
                    return edge

        return False

    #check if node belongs to a clusternode
    #@returns the clusternode the node belongs to or False
    def belongsNodeToClusterNode(self,node):
        for clusternode in self.clusterNodeslist:
            if(clusternode.containsNode(node)):
                return clusternode
        return False



    #Function that generates cluster nodes to use in the final graph
    #@param clustersToBuild list of clusters to build nodes for
    def buildClusterNodes(self,clustersToBuild):
        finalList = []

        for cluster in clustersToBuild:
            nodelist = cluster.getNodes()
            inClusterEdges = self.getInClusterEdges(nodelist)
            outInfo = self.getOutClusterEdges(nodelist)
            outClusterEdges = outInfo[0]
            neighbours = outInfo[1]
            clusternode = ClusterNode.ClusterNode(nodelist,inClusterEdges,outClusterEdges,neighbours)
            finalList.append(clusternode)
        return finalList

    #@return tuple with list of edges with 1 node in the nodelist and the other not
    #and list of these neighbouring nodes
    def getOutClusterEdges(self,nodes):
        edges = []
        neighbours = []
        for edge in self.edgeslist:
            edgeNodes = edge.getTupleFormat()
            if((edgeNodes[0] in nodes) and (edgeNodes[1] not in nodes)):
                edges.append(edge)
                #collect this neighbour
                if(edgeNodes[1] not in neighbours):
                    neighbours.append(edgeNodes[1])
            elif((edgeNodes[0] not in nodes) and(edgeNodes[1] in nodes)):
                edges.append(edge)
                if(edgeNodes[0] not in neighbours):
                    neighbours.append(edgeNodes[0])
        return(edges,neighbours)

    #@return all edges between the nodes in the list that was given as argument
    def getInClusterEdges(self,nodes):
        edges = []
        for edge in self.edgeslist:
            #check if both source and target node is in the list
            edgeNodes = edge.getTupleFormat()
            if((edgeNodes[0] in nodes) and (edgeNodes[1] in nodes)):
                edges.append(edge)
        return edges

    def initialClusterBuilding(self):
        #first find the victim nodes
        for node in self.nodeslist:
            #check if node is unimportant enough to aggregate
            if(node.getWeight() < self.aggregationVictimParam):
                #search an edge that is strong enough to carry out the aggregation
                #using the distance significance from fuzzy mining
                aggregationEdge = self.searchAggregationableEdge(node)
                #check if we found an edge
                if(isinstance(aggregationEdge,Edge.Edge)):
                    #check if target node is a cluster
                    cluster = self.checkIfNodeIsCluster(aggregationEdge.getOtherNode(node))
                    #check if we found a cluster
                    if(isinstance(cluster,Cluster.Cluster)):
                        #add node to cluster
                        cluster.addNode(node)
                        cluster.addEdge(aggregationEdge)

                    else:
                        #if not -> make a cluster with this source node as only node
                        cluster = Cluster.Cluster(node,aggregationEdge)
                        #add to clusterlist
                        self.clusterlist.append(cluster)


    #@returns false if the node is not a cluster
    #@returns the cluster this node is a part of if true
    def checkIfNodeIsCluster(self,node):
        for cluster in self.clusterlist:
            if(cluster.containsNode(node)):
                return cluster
        return False




    #use the distance significant to determine if an edge is strong enough to carry out the aggregation
    #@param node = node for which we seek an aggregation worthy incident edge
    #@return the edge that will carry out aggregation or "" if there is no edge worthy
    def  searchAggregationableEdge(self,node):
        incidentEdges = self.collectIncidentEdges(node)
        aggrCandidates = {}
        for edge in incidentEdges:
            distanceSign = abs(edge.getWeight() - node.getWeight())
            #check if the distance significance is strong enough to aggregate
            if(distanceSign > self.aggregationCorrelationParam):
                #save candidate, cause we want the strongest one
                aggrCandidates[edge] = distanceSign

        #search strongest edge
        if aggrCandidates:
            aggrEdge = max(aggrCandidates.items(), key=operator.itemgetter(1))[0]
            return aggrEdge
        else:
            return ""


    #Merge clusters :
    #Check for every cluster is there is a neighbour cluster
    #if so -> check edge for aggregation capabilities and merge clusters
    def clusterMerging(self):
        clustersToMerge = self.getClustersToMerge()
        #check if there are clusters to merge
        clusterlist = []
        if(clustersToMerge):
            unambiguousClusterList = self.createUnambiguousClusters(clustersToMerge)
            clusterlist = self.combineClusters(unambiguousClusterList)
        return clusterlist


    #@param clustersToCombine = list containing lists of clusters that need to become 1
    #@return list of singular clusters
    def combineClusters(self,clustersToCombine):
        finalList = []
        for cluster in clustersToCombine:
            newCluster = Cluster.Cluster()
            for clusterPart in cluster:
                nodes = clusterPart.getNodes()
                edges = clusterPart.getEdges()
                for node in nodes:
                    newCluster.addNode(node)
                for edge in edges:
                    newCluster.addEdge(edge)
            finalList.append(newCluster)
        return finalList





    #Function that combines all combinations of related clusters to 1 final cluster
    def createUnambiguousClusters(self,clustersToMerge):
        #list containing lists of clusters to merge
        finalClusters = []
        alreadyUsedClusters = []
        allClustersDone = False
        while not allClustersDone:
            nextList = self.getNextClusterList(clustersToMerge,alreadyUsedClusters)
            if(nextList):
                finalClusters.append(nextList)
                alreadyUsedClusters.extend(nextList)
            else:
                allClustersDone = True

        return finalClusters

    def getNextClusterList(self,clustersToMerge,alreadyUsedClusters):
        #find the first cluster that has not been used yet
        startClusterFound = False
        for tuple in clustersToMerge:
            if(not startClusterFound):
                if(tuple[0] not in alreadyUsedClusters):
                    startCluster = tuple[0]
                    startClusterFound = True
                elif(tuple[1] not in alreadyUsedClusters):
                    startCluster = tuple[1]
                    startClusterFound = True

        clusterList = []
        if(startClusterFound):
            mergePairs = self.findMergePairs(startCluster,clustersToMerge)
            self.recursiveHelp.append(startCluster)
            self.recursive(mergePairs,clustersToMerge)
            #recursiveHelp now contains all the clusters that need to combine to 1
            for c in self.recursiveHelp:
                clusterList.append(c)
            #clear recursiveHelp
            self.recursiveHelp = []


        return clusterList

    def recursive (self,clustersToDo,clustersToMerge):
        for cluster in clustersToDo:
            recursiveMergePairs = self.findMergePairs(cluster,clustersToMerge)
            self.recursiveHelp.append(cluster)

            #only when there are still parts to do
            if(recursiveMergePairs):
                #recursive
                self.recursive(recursiveMergePairs,clustersToMerge)

    #Function that constructs a list of clusters cluster1 is supposed to merge with
    #@param cluster1 = cluster we are searching all direct pairings for
    #@param clusterPairs = list of all cluster merging pairs
    def findMergePairs(self,cluster1, clusterPairs):
        clusterList = []
        for tuple in clusterPairs:
            if(tuple[0] == cluster1):
                if((tuple[1] not in clusterList)and(tuple[1] not in self.recursiveHelp)):
                    clusterList.append(tuple[1])
            elif(tuple[1] == cluster1):
                if((tuple[0] not in clusterList)and (tuple[0] not in self.recursiveHelp)):
                    clusterList.append(tuple[0])

        return clusterList



    #@return list of tuples of clusters to merge (cluster1,cluster2)
    def getClustersToMerge(self):
        whichClustersToMerge = []
        #handle first the aggregation edges
        for cluster in self.clusterlist:
            mergingCandidates = {}
            neighbourNodes = cluster.getNeighbourAggrNodes()
            for node,edge in neighbourNodes.items():
                targetCluster = self.checkIfNodeIsCluster(node)
                #check if we found a cluster containing this node
                if(isinstance(targetCluster,Cluster.Cluster)):
                    #this is a candidate for merging, but we want the most highly correlated one
                    #now we know that both of these nodes are insignificant cause they were selected for clusters
                    #in the first place, so just check for the edge with the largest distance significance
                    mergingCandidates[node] = {"Edge":edge,"Cluster":targetCluster}


            #if we found candidates, find the edge with the greatest aggregation power
            if(mergingCandidates):
                #now we have the candidates, check for the best one:
                optimalCandidate = self.findOptimalMergingCandidate(mergingCandidates)
                #first check of this combi isn't already listed in the list
                if(((cluster,optimalCandidate[2]) not in whichClustersToMerge) and ((optimalCandidate[2],cluster)not in whichClustersToMerge)):
                    whichClustersToMerge.append((cluster,optimalCandidate[2]))

            #we found nodes, but none of these nodes are clusters, so check the non-aggr edges
            else:
                #collect the non-aggr edges that are candidates for aggregation
                nonAggrCandidates = self.getCandidateNonAggrNodes(cluster)
                #if we found candidates
                if(nonAggrCandidates):
                    #find the optimal candidate
                    optimalCandidate = self.findOptimalMergingCandidateNonAggr(nonAggrCandidates)
                    #check if there is an edge strong enough to carry out the aggregation
                    if(optimalCandidate):
                        #tuples (cluster,cluster)
                        #if not already listed, add
                        if(((cluster,optimalCandidate[2]) not in whichClustersToMerge)and ((optimalCandidate[2],cluster)not in whichClustersToMerge)):
                            whichClustersToMerge.append((cluster,optimalCandidate[2]))
                            #add this edge, cause it wasnt in the list, so i can check the algorithm
                            cluster.addEdge(optimalCandidate[1])
                            #
        return whichClustersToMerge

    #collects all the incident edges on this cluster that are not in de aggregation edges list of the cluster
    #@return dictionary with edge as key and dict with target node and cluster as value
    #is basically a collection of edges incident on the cluster, for which the target nodes are also clusters
    #and are thus candidates for aggregation
    def getCandidateNonAggrNodes(self,cluster):
        clusterNodes = cluster.getNodes()
        clusterAggrEdges = cluster.getEdges()

        candidateNonAggrNodes = {}
        for node in clusterNodes:
            #collect the incident edges
            incidentEdges = self.collectIncidentEdges(node)
            for edge in incidentEdges:
                if not edge in clusterAggrEdges:
                    if not edge in candidateNonAggrNodes:
                        #check if target node is a cluster
                        targetNode = edge.getOtherNode(node)
                        targetCluster = self.checkIfNodeIsCluster(targetNode)
                        #check if we found a cluster containing this node
                        if(isinstance(targetCluster,Cluster.Cluster)):
                            #add to the candidates
                            candidateNonAggrNodes[edge] = {"Node":targetNode,"Cluster":targetCluster}
        return candidateNonAggrNodes



    #Finds the edge with the greates aggregation power, base on the distance significance to the target node
    #@param candidates: dict with target node as key and dict with edge and cluster as value
    #@return optimal candidate tuple (node, edge, cluster)
    def findOptimalMergingCandidate(self,candidates):
        #We want the distance significance as large as possible
        maxDistSign = 0
        optimalCandidate = ()
        for node, clusterInfo in candidates.items():
            distSign = abs(clusterInfo["Edge"].getWeight() - node.getWeight())
            if (distSign > maxDistSign):
                maxDistSign = distSign
                optimalCandidate = (node,clusterInfo["Edge"],clusterInfo["Cluster"])
        return optimalCandidate


    #Finds th edge with teh greatest aggregation power, based on the distance significance to the target node
    #@param candidates: dict with edge as key and dict with node and cluster as value
    #@return optimal candidate tuple (node, edge, cluster)
    def findOptimalMergingCandidateNonAggr(self,candidates):
        maxDistSign = 0
        optimalCandidate = False
        for edge, clusterInfo in candidates.items():
            distSign = abs(edge.getWeight() - clusterInfo["Node"].getWeight())
            if ((distSign > self.aggregationCorrelationParam) and (distSign > maxDistSign)):
                maxDistSign = distSign
                optimalCandidate = (clusterInfo["Node"],edge,clusterInfo["Cluster"])
        return optimalCandidate




###################"ABSTRACTION"##################

    #Abstraction of the following:
    #insignificant nodes that does not have an edge strong enough for aggregation
    #so basically insignificant nodes wih weak relations to their neighbours
    #delete the node and the weak relationships
    def abstraction(self):
        nodesToAbstract = []
        edgesToAbstract = []
        clusterEdgesToAbstract = []
        numberTrue = 0
        candidates = 0
        #search the nodelist, this is where the non cluster nodes still reside
        for node in self.nodeslist:
            #check if node is unimportant enough to abstract
            if(node.getWeight() < self.abstractionVictimParam):
                candidates += 1
                #check if all edges are weak (not strong enough for aggregation)
                allEdgesWeak = self.checkIfAllEdgesWeak(node)

                if(allEdgesWeak[0]):
                    numberTrue += 1
                    #abstract this node
                    nodesToAbstract.append(node)
                    edgesToAbstract = self.extendListWithoutDuplicates(edgesToAbstract,allEdgesWeak[1])
                    clusterEdgesToAbstract = self.extendListWithoutDuplicates(clusterEdgesToAbstract,allEdgesWeak[2])


        #now clear all these nodes from the node list
        self.abstractionCleanup(nodesToAbstract,edgesToAbstract,clusterEdgesToAbstract)



    #Deletes all the nodes and edges in these lists from the final lists
    def abstractionCleanup(self,nodesToAbstract,edgesToAbstract,clusterEdgesToAbstract):
        #delete nodes from list
        self.nodeslist = [x for x in self.nodeslist if x not in nodesToAbstract]

        #delete edges
        self.edgeslist = [x for x in self.edgeslist if x not in edgesToAbstract]

        #delete clusterEdges
        self.clusterEdgeslist = [x for x in self.clusterEdgeslist if x not in clusterEdgesToAbstract]


    #Function that extends the first list with all the items from list2 that aren't already in list 1
    def extendListWithoutDuplicates(self,listToExtend,list2):
        for item in list2:
            if(item not in listToExtend):
                listToExtend.append(item)
        return listToExtend


    #checks if all the incident edges on this node are too weak for aggregation
    #@return tuple with
    #1.true if all edges too weak, else return false
    #2. the list of incidentEdges to delete
    #3. the list of incidentClusterEdges to delete
    #Algorithm = the same as for aggregation
    def checkIfAllEdgesWeak(self,node):
        #get all incident edges
        incidentEdges = self.collectIncidentEdges(node)
        #get all incident cluster edges
        incidentClusterEdges = self.collectIncidentClusterEdges(node)

        for edge in incidentEdges:
            distanceSign = abs(edge.getWeight() - node.getWeight())
            if(distanceSign > self.abstractionCorrelationParam):
                #we found a candidate, so not all edges are too weak
                return (False,[],[])

        #exactely the same as for the normal incident edges
        #but split up in case of future changes
        for edge in incidentClusterEdges:
            distanceSign = abs(edge.getWeight() - node.getWeight())
            if(distanceSign > self.abstractionCorrelationParam):
                #we found a candidate, so not all edges are too weak
                return (False,[],[])

        #all incident edges are weak
        return (True,incidentEdges,incidentClusterEdges)


    #@return list of all incident edges on this node that connect to a cluster
    def collectIncidentClusterEdges(self,node):
        edges = []
        for edge in self.clusterEdgeslist:
            #should be an edge between a regular node and a cluster
            if(not edge.getIfInterClusterEdge()):
                if(edge.isSourceNode(node)):
                    edges.append(edge)
        return edges
