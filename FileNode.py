#Class that represents a file node
#The idea is the following:
# A programmer can collaborate on many topics, but still have files that he didnt collaborate on
# This will not be visible in the collaboration graph, since the collaboration on other aspects
# induces strong relationship between the programmers involved in the collaboration.
# To facilitate the discovery of programmers that work on an isolated part of the code as
# a small part of their tasks, we want to visualize this as a separate  'file node'.
# The file node is connected to a certain programmer and holds a list of all the files that were
# only altered by this programmer. The node has a weight = weighted sum of the importance values of all these files.
#
# We use the following algorithm:
#   Every programmer node in the final graph, has a file node connected to it
#   This file node contains a distinct list of all the files this programmer worked on
#   Remove the files on which the programmer did pair programming
#   Remove the files on which the programmer collaborated with another programmer
#           Take into account: timing constraints, a threshold of a min number of collabs
#   Calculate the weight of the file node as the sum of the file importances of the remaining files
#   File nodes will be shown in the final visualization if they have a weight larger than a set threshold
import EdgeWeightCalculator

class FileNode:

    def __init__(self,id,node):
        #unique node ID
        self.ID = id
        #the base grpah node this file node is connected to
        self.baseGraphNode = node
        #the programmer this baseGraphNode contains and thus this file node is connected to
        self.programmer = node.getProgrammer()
        #distinct list of files this programmer worked on and did NOT pair program on!
        self.distinctFileList = self.buildDistinctFileList()
        #copy by value
        self.isolatedFileList = self.distinctFileList[:]
        self.collaborationThreshold = 3


        #construct the list of files this programmer worked on alone
        self.constructIsolatedFileList()

        #weight of the file node
        self.weight = self.calculateWeight()

    def getID(self):
        return self.ID

    def getWeight(self):
        return self.weight

    def setWeight(self,weight):
        self.weight = weight

    #the label is just the number of distinct files in the isolatedFileList
    def getLabel(self):
        return(str(len(set(self.isolatedFileList))))

    def getProgrammerLabel(self):
        return(self.programmer.getLabel())

    #@return a list of unique files this programmer worked on and did not pair program on with anyone
    def buildDistinctFileList(self):
        return self.programmer.getDistinctListNonPairprogrammingFiles()

    #function that initializes the isolatedFileList: distinct list of files this programmer was the only one to work on
    def constructIsolatedFileList(self):
        #go through the distinct file list and for every file decide:
        #remove from he isolated file list or not?
        for file in self.distinctFileList:
            #determine if this programmer collaborated on this file
            collaboratedOn = self.wasFileCollaboratedOn(file)

            if(collaboratedOn):
                #remove file from the isolated file list
                if(file in self.isolatedFileList):
                    self.isolatedFileList.remove(file)


    #Function that determines if the programmer of this file node collaborated with another programmer on this file
    #@param file : the file for which we want to determine whether the programmer collaborated on it
    #@return logical value that represents if the programmer collaborated on the file or not
    def wasFileCollaboratedOn(self,file):
        #we need a list of sorted sourceTimestamps: the timestamps of the commits where this programmer worked on this file
        #For every other programmer that worked on this file we need a sorted list of timestamps also
        #Compare the source list with every target list up until a collaborated on this file was found -> return TRUE
        #if no collaboration was found: check whether the period this programmer worked on the file was significant enough to include the file
        #if significant -> return FALSE

        #make list of source timestamps
        sourceTimestamps = file.getListOfCommitTimestampsByProgrammer(self.programmer)
        #get a set of all the programmers that worked on this file
        contributors = file.getListOfContributors()

        #remove this programmer from the set
        contributors.remove(self.programmer)

        #set of timestamps of the other contributors
        otherTimestamps = set([])
        #for every programmer: check if they collaborated
        for prog in contributors:
            targetTimestamps = file.getListOfCommitTimestampsByProgrammer(prog)
            otherTimestamps |= set(targetTimestamps)
            #use the source and target timestamps to determine if collaboration took place
            #returns the number of times collaboration took place
            numberOfTimesCollaboration = self.determineNumberOfTimesCollaboration(sourceTimestamps,targetTimestamps)
            if(numberOfTimesCollaboration >= self.collaborationThreshold):
                #collaboration took place, stop the calculations here
                return True

        #if the function reaches this part it means that the programmer did not collab with anyone on this file (>= collaborationThreshold)
        #determine if his contribution on this file was significant
        significantContribution = self.isContributionSignificant(set(sourceTimestamps),otherTimestamps)
        return(not significantContribution)


    #Function that determines the number of times 2 programmers collaborated on a file
    #Uses the same principle as the binary frequency significance of the Edge weight -> works with blocks (see EdgeWeightCalculator.py)
    #@param sourceTimestamps list of timestamps programmer 1 committed the file
    #@param targetTimestamps list of timestamps programmer 2 committed the file
    #@returns the number of times the 2 worked together on the file
    def determineNumberOfTimesCollaboration(self,sourceTimestamps,targetTimestamps):
        #sort the timestamps
        sourceTimestamps.sort()
        targetTimestamps.sort()

        #use a function of the EdgeWeightCalculator, but note that the calculator misses an init arg
        #so be careful about using other functionalities, cause they will not necesarilly work
        collaborationCalculator = EdgeWeightCalculator.EdgeWeightCalculator([])
        #calculate the number of times the 2 programmers collaborated on this file
        numberOfTimes = collaborationCalculator.calculateFreqTimestampDifferences(sourceTimestamps,targetTimestamps)
        return numberOfTimes


    #Function that determines if the contribution on this file was significant
    #@param sourceSet sorted set of timestamps the programmer committed the file
    #@param targetSet sorted set of timestamps other programmers committed the file
    #@return logical value whether the contribution of the programmer on this file is significant
    def isContributionSignificant(self,sourceSet,targetSet):
        #TODO : fill in this function
        #at the moment, any contribution is significant enough
        return True


    #Function that calculates the sum of the file importances of the files in the isolatedFileList
    def calculateWeight(self):
        weight = 0
        for file in self.isolatedFileList:
            weight += file.getImportance()

        return weight
