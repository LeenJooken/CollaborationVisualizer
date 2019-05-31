
#class that represents a Programmer
class Programmer:
    def __init__(self,name,id):
        self.name = name
        self.commitList = []
        self.ID = id

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def getID(self):
        return self.ID

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
