import Node
#class that represents an edge
class Edge:

    def __init__(self,source,target):
        self.sourceNode = source
        self.targetNode = target
        self.weight = 1
        self.type = "Undirected"
        self.pairProgrammingWeight = 0
        self.pairProgramming = False
        self.distinctProgramming = False
        #just a list of commits
        self.commitsRelevantToPairProgramming = []
        #list of lists: [[sourcecommit,targetcommit],[sourcecommit,targetcommit],...]
        self.commitsRelevantToDisjunctCollaboration = []

    #precondition: @param sourcenode must indeed be involved in this edge!
    #@returns the node on the other end of the edge
    def getOtherNode(self,sourcenode):
        if(self.sourceNode == sourcenode):
            return self.targetNode
        else:
            return self.sourceNode

    def getSourceNodeName(self):
        return self.sourceNode.getLabel()
    def getTargetNodeName(self):
        return self.targetNode.getLabel()

    def getTupleFormat(self):
        return (self.sourceNode,self.targetNode)

    def containsNode(self,node):
        return ((self.sourceNode == node) or (self.targetNode == node))

    def setPairProgrammingWeight(self,weight):
        self.pairProgrammingWeight = weight
        self.pairProgramming = True

    def setDistinctProgramming(self):
        self.distinctProgramming = True

    def getIfDistinctProgramming(self):
        return self.distinctProgramming

    def getCollaborationType(self):
        if (self.distinctProgramming and self.pairProgramming):
            return "Pair and disjunct programming"
        elif (self.pairProgramming):
            return "Pair programming"

        return "Disjunct programming"

    def resetSourceAndTargetNodes(self,source,target):
        self.sourceNode = source
        self.targetNode = target

    def getPairProgrammingWeight(self):
        return self.pairProgrammingWeight

    def setPairProgCommitList(self,commits):
        self.commitsRelevantToPairProgramming = commits

    def setDisjunctCollabCommitList(self,commits):
        self.commitsRelevantToDisjunctCollaboration = commits

    def getWeight(self):
        return self.weight

    def setWeight(self,weight):
        self.weight = weight

    def getType(self):
        return self.type

    def addPairProgrammingCommit(self,commit):
        self.commitsRelevantToPairProgramming.append(commit)

    def getSourceNodeID(self):
        return self.sourceNode.getID()

    def getTargetNodeID(self):
        return self.targetNode.getID()

    def getIfPairProgramming(self):
        return self.pairProgramming

    def getIfDistinctCollab(self):
        return (len(self.commitsRelevantToDisjunctCollaboration) > 0)

    #@returns dictionary with 'File' as key and a list of timestamps as value
    def getPairProgrammingFiles(self):
        pairProgFiles = {}

        for commit in self.commitsRelevantToPairProgramming:
            files = commit.getFiles()
            timestamp = commit.getDate()
            for file in files:
                if file in pairProgFiles:
                    pairProgFiles[file].append(timestamp)
                else:
                    pairProgFiles[file] = [timestamp]


        return pairProgFiles

    #@returns dictionary with 'File' als key and 'sourceTimestamps' 'targetTimestamps' as values (both lists of timestamps)
    def getDistinctCollabFiles(self):
        collabFiles = {}

        for commitPair in self.commitsRelevantToDisjunctCollaboration:
            filesCom1 = commitPair[0].getFiles()
            filesCom2 = commitPair[1].getFiles()
            timestamp1 = commitPair[0].getDate()
            timestamp2 = commitPair[1].getDate()
            #look which files they have in common
            filesInCommon = self.checkWhichFilesInCommon(filesCom1,filesCom2)

            for file in filesInCommon:
                if file in collabFiles:
                    if timestamp1 not in collabFiles[file]['sourceTimestamps']:
                        collabFiles[file]['sourceTimestamps'].append(timestamp1)
                    if timestamp2 not in collabFiles[file]['targetTimestamps']:
                        collabFiles[file]['targetTimestamps'].append(timestamp2)
                else:
                    collabFiles[file] = {'sourceTimestamps':[timestamp1],'targetTimestamps':[timestamp2]}
        return collabFiles

    #@returns list of file objects they have in common
    def checkWhichFilesInCommon(self,files1,files2):
        files1_set = set(files1)
        files2_set = set(files2)
        filesInCommon = list(files1_set & files2_set)

        return filesInCommon
