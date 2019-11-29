
#class that represents a Programmer
class Programmer:
    def __init__(self,name,id):
        self.name = name
        self.commitList = []
        self.ID = id
        self.aliases = [name]

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def getID(self):
        return self.ID

    #add an alias for this programmer
    def addAlias(self,name):
        if not (name in self.aliases):
            self.aliases.append(name)

    #get list of programmer names
    def getNames(self):
        return self.aliases

    #returns a string of all the programmer aliases
    def getLabel(self):
        label = ""
        count = 0
        for alias in self.aliases:
            if(count != 0):
                label += "+"
            label += alias
            count += 1
        return label


    def addToCommitList(self,commit):
        #check first if the commit already exists in the list
        for com in self.commitList:
            if(com.getRevisionNumber() == commit.getRevisionNumber()):
                return
        #it does not exist yet so add
        self.commitList.append(commit)

    def getCommitList(self):
        return self.commitList

    #@returns a list of File objects, with each file only once
    def getDistinctFileList(self):
        files = []
        for com in self.commitList:
            comFiles = com.getFiles()
            for file in comFiles:
                #if not already in the list -> add
                if not file in files:
                    files.append(file)
        return files

    #@return a distinct list of all the files that he didnt pair program on  (added and modified only)
    def getDistinctListNonPairprogrammingFiles(self):
        files = []
        pairprogrammingFiles = []
        for com in self.commitList:
            #check if the commit is a pair programming commit
            comFiles = com.getFiles()
            if(com.isPairProgramming()):
                #keep these files in a distinct list, so we can delete them out of the filelist at the end
                for file in comFiles:
                    if not file in pairprogrammingFiles:
                        pairprogrammingFiles.append(file)

            else:
                #add these files to the file list
                for file in comFiles:
                    if not file in files:
                        files.append(file)

        #now remove the pair programming files from the file list
        distinctNPFiles = [x for x in files if x not in pairprogrammingFiles]

        #of these remaining files: delete the files, this programmer did not contributed on (added and/or modified)
        #so delete the files that this programer only deleted in a commit
        filesThatWereOnlyDeleted = self.getFilesThatWereOnlyDeleted(distinctNPFiles)

        resultingFiles = [x for x in distinctNPFiles if x not in filesThatWereOnlyDeleted]

        return resultingFiles

    #Function that constructs a list of all files this programmer worked on that he didnt pair program on
    #EXCEPT if the pair programming was only with the programmers in the exception list, these files WILL be included in the list
    #@param listOfExceptionProgrammers list of programmers for with who pair programming can be ignored, and the files included in the list
    #@return a distinct list of files the programmer did not pair program on with programmers outside of the exception list
    def getDistinctListNonPairprogrammingFilesException(self,listOfExceptionProgrammers):
        files = []
        pairprogrammingFiles = []
        for com in self.commitList:
            #check if the commit is a pair programming commit
            comFiles = com.getFiles()
            if(com.isPairProgramming()):
                #if the pair programming is solely with someone in the cluster, it doesnt count
                if(not com.doesListContainAllContributors(listOfExceptionProgrammers)):
                    #The pair programming was also with someone outside of the cluster, keep the files
                    #keep these files in a distinct list, so we can delete them out of the filelist at the end
                    for file in comFiles:
                        if not file in pairprogrammingFiles:
                            pairprogrammingFiles.append(file)

            else:
                #add these files to the file list
                for file in comFiles:
                    if not file in files:
                        files.append(file)

        #now remove the pair programming files from the file list
        distinctNPFiles = [x for x in files if x not in pairprogrammingFiles]

        #of these remaining files: delete the files, this programmer did not contributed on (added and/or modified)
        #so delete the files that this programer only deleted in a commit
        filesThatWereOnlyDeleted = self.getFilesThatWereOnlyDeleted(distinctNPFiles)

        resultingFiles = [x for x in distinctNPFiles if x not in filesThatWereOnlyDeleted]

        return resultingFiles


    #@param files list of files we want to know which files were only deleted by this programmer
    #@return list of files that this programmer only deleted, not added or modified in any way
    def getFilesThatWereOnlyDeleted(self,files):
        onlyDeleted = []
        for file in files:
            listOfAddedAndModifiedCommits = file.getListOfAddedAndModifiedCommits()
            #compare this list with the commitlist of the programmer
            #if there is an element in common, do not add to the onlyDeleted list ; else do add
            sharesItems = bool(set(self.commitList) & set(listOfAddedAndModifiedCommits))
            if(not sharesItems):
                onlyDeleted.append(file)

        return onlyDeleted
