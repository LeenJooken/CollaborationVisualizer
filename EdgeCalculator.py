#This class is designed to calculate where edges should be between nodes

class EdgeCalculator:
    #@param commit: list of all the commits from the log
    def __init__(self,commits,programmers):
        self.commitlist = commits
        self.programmerslist = programmers

    #function that calculates which nodes have a pair programming relation + weight
    #@returns dictionary with sourceNodeID, targetNodeID as key and weight, commits as value
    def getPairProgrammingEdges(self):
        edgeDict = {}


        for commit in self.commitlist:
            contrib = commit.getContributors()
            commitNumber = commit.getRevisionNumber()

            for source in contrib:
                for target in contrib:
                    sourceID = source.getID()
                    targetID = target.getID()
                    if(sourceID != targetID):
                        #2 situations: dict already contains this tuple or doesnt
                        if((sourceID,targetID) in edgeDict):
                            #check if it is a different commits, else ignore
                            if(not commit in edgeDict[(sourceID,targetID)]['commits']):
                                #increase the weight
                                edgeDict[(sourceID,targetID)]['weight'] += 1
                                #add commit to commitList
                                if(not commit in edgeDict[(sourceID,targetID)]['commits']):
                                    edgeDict[(sourceID,targetID)]['commits'].append(commit)

                        elif((targetID,sourceID) in edgeDict):
                            if(not commit in edgeDict[(targetID,sourceID)]['commits']):
                                #increase the weight
                                edgeDict[(targetID,sourceID)]['weight'] += 1
                                #add commit to commitList
                                if(not commit in edgeDict[(targetID,sourceID)]['commits']):
                                    edgeDict[(targetID,sourceID)]['commits'].append(commit)
                        else:
                            #tuple doesn not yet exist, make a new one
                            edgeDict[(sourceID,targetID)] = {'weight': 1,'commits':[commit]}


        return edgeDict

        #function that calculates whether or not there exists an edge between 2 programmers
        #collects all revelant commits for smoother future processing
        #@returns dictionary with sourceNodeID, targetNodeID as key and commits as value
    def getDisjunctColloborationEdges(self):
        edgeDict = {}

        #check for each pair of programmers
        for sourceIterator in range(0,len(self.programmerslist)-2):
            source = self.programmerslist[sourceIterator]
            for targetIterator in range(sourceIterator+1,len(self.programmerslist)-1):
                target = self.programmerslist[targetIterator]
                #compare source & target
                comlist = self.collectMutualCommits(source,target)

                if(len(comlist)>0):
                    #there exists an edge
                    edgeDict[(source.getID(),target.getID())] = {'commits':comlist}

        return edgeDict


    def collectMutualCommits(self,sourceProg,targetProg):
        mutualCommits = []
        sourceCommits = sourceProg.getCommitList()
        targetCommits = targetProg.getCommitList()

        for sourceCom in sourceCommits:
            for targetCom in targetCommits:
                #check if it isnt pair programming:
                #condition: pair program ifandonlyif their names are mentioned in both commits
                if (not (sourceCom.hasAsContributor(targetProg) and targetCom.hasAsContributor(sourceProg))):
                    #if they have 1 file in common it's OK
                    files1 = sourceCom.getFiles()
                    files2 = targetCom.getFiles()
                    filepaths1 = self.makeListOfFilePaths(files1)
                    filepaths2 = self.makeListOfFilePaths(files2)

                    files1_set = set(filepaths1)
                    files2_set = set(filepaths2)
                    if(files1_set & files2_set):
                        mutualCommits.append([sourceCom,targetCom])

        return mutualCommits

    def makeListOfFilePaths(self,files):
        list = []
        for file in files:
            list.append(file.getPath())
        return list
