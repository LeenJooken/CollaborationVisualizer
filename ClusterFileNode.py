#class that represents a file node that is connected to a cluster node
#Uses the same logic as the FileNode class with some alterations:
# We use the following algorithm: (see FileNode class for more details on the base algorithm)
#The cluster node can have 1 file node attached to it if the cluster as a whole works on isolated code
#   Make a list of all the files the programmers worked on (does not have to be collaboration with each other)
#   For each file: execute the algorithm but now make a list of the timestamps of the commits of all the cluster members
#   Collect the contributors but remove all the cluster members
#   Carry on with the algorithm the same way


#Is almost the same as FileNode.py, could maybe be better if inheritance was used, but for the sake of future ease of extension the file are separated
#TODO: maybe reshape this to be in the form of inheritance
import EdgeWeightCalculator

class ClusterFileNode:

    def __init__(self,id,clusternode):
        #unique node ID
        self.ID = id
        #clusternode this file node is connected to
        self.clusternode = clusternode
        self.listOfProgrammers = self.clusternode.getListOfProgrammers()
        #distinct list of all the files the programmers that belong to this clusternode worked on and did not pair program on with someone outside of the cluster
        #a dictionary with the cluster programmer as key and their file list as value
        self.distinctFileList = self.buildDistinctFileList()

        #list of files this cluster of programmers worked on alone
        self.isolatedFileList = set([])
        self.collaborationThreshold = 3
        self.clusterCollaborationThreshold = self.collaborationThreshold  #For now, set the threshold the same for regular and cluster nodes

        #construct the list of files this cluster of programmers worked on alone
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
        label = ""
        firstName = True
        for p in self.listOfProgrammers:
            if(not firstName):
                label += "+"
            label += p.getLabel()
        return(label)

    #@return a dictionary of the programmers and each their list of unique files the worked on and did not pair program on with anyone outside of the cluster
    def buildDistinctFileList(self):
        fileListByProgrammer = {}
        for programmer in self.listOfProgrammers:
            fileListByProgrammer[programmer] = programmer.getDistinctListNonPairprogrammingFilesException(self.listOfProgrammers)
        return fileListByProgrammer


    #function that initializes the isolatedFileList: distinct list of files the cluster of programmers were the only ones to work on
    def constructIsolatedFileList(self):
        #make first a set of all files all the cluster programmers worked on, based on distinctfilelist
        #completelist is to iterate over all the files in peace, the other list is the list we are going to remove things from
        completeList = set([])
        for programmer, distList in self.distinctFileList.items() :
            self.isolatedFileList |= set(distList)
            completeList |= set(distList)

        #Now we're going to remove files from this list that the cluster collaborated on with programmers outside of the cluster
        #The same way as the regular file nodes

        #go through the file list and for every file decide:
        #remove from he isolated file list or not?
        for file in completeList:
            #determine if there was collaboration of on this file
            collaboratedOn = self.wasFileCollaboratedOn(file)

            if(collaboratedOn):
                #remove file from the isolated file list
                if(file in self.isolatedFileList):
                    self.isolatedFileList.remove(file)




    #Function that determines if the programmers of this cluster collaborated on this file with programmers outside of the cluster
    #@param file : the file for which we want to determine whether the programmers collaborated on it
    #@return logical value that represents if the programmers collaborated on the file with someone outside of the cluster or not
    def wasFileCollaboratedOn(self,file):
        #We consider the programmers of the clusternode as 1; so collect all the time stamps of these programmers as the sourceTimestamps
        #For every programmer that does not belong to the cluster and worked on this file, we need a sorted list of the timestamps also
        #Compare the source list with every target list up until a collaborated on this file was found -> return TRUE
        #if no collaboration was found: check whether the period this programmer worked on the file was significant enough to include the file
        #if significant -> return FALSE

        #make list of source timestamps
        sourceTimestamps = file.getListOfCommitTimestampsForAllTheseProgrammers(self.listOfProgrammers)
        #get a set of all the programmers that worked on this file
        contributors = file.getListOfContributors()

        #remove the programmers involved in the cluster from the set
        contributors = contributors - set(self.listOfProgrammers)


        #set of timestamps of the other contributors
        otherTimestamps = set([])
        #for every programmer: check if they collaborated
        for prog in contributors:
            targetTimestamps = file.getListOfCommitTimestampsByProgrammer(prog)
            otherTimestamps |= set(targetTimestamps)
            #use the source and target timestamps to determine if collaboration took place
            #returns the number of times collaboration took place
            numberOfTimesCollaboration = self.determineNumberOfTimesCollaboration(sourceTimestamps,targetTimestamps)
            if(numberOfTimesCollaboration >= self.clusterCollaborationThreshold):
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
