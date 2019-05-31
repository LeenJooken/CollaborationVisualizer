import Commit
import File
import time
import Programmer
import Output
import re
#class that represents a parsed log
#contains a list of commits and a list of programmers
#READ ME: exact parsing has been omitted as it is log type sensitive, and replaced by guidelines
class Log:

    def __init__(self,logFile):

        self.listOfCommits = []
        self.filename = logFile
        self.listOfProgrammers = []
        self.programmerIterator = 1
        self.listOfFiles = []
        self.parseSVNLog()
        self.calculateFileImportance()





    def getlistOfProgrammers(self):
        return self.listOfProgrammers

    def getListOfCommits(self):
        return self.listOfCommits


    #parses the svn log file and constructs a list of commits
    def parseSVNLog(self):
        with open(self.filename,'r') as f:
            #exact parsing is omitted as pre-processing is differs for every VCS
            #handle each revision as follows:
            #Need: revision number, author, date, message, files, collaborators,modifier
            #revision number
            rev_number = #parse the revision number
            author = #parse the author
            date = self.parseDate(#pass date in string format)
            programmers = self.getProgrammers( #pass string to parse programmers from)
            #for each file in this commit:
                modifier = #parse modifier
                path = #parse file path
                #check if file already exists
                file = self.searchFile(path)
                #file does not exist
                if(not isinstance(file,File.File)):
                    file = File.File(path)
                    #add it to the general overview list
                    self.listOfFiles.append(file)

                    #add to dictionary to add to the right list of commits later on
                    fileStatus[fileStatIterator] = {'File':file,'Status': modifier}
                    fileStatIterator += 1

                    files.append(file)


            #end of revision
            commit = Commit.Commit(rev_number,author,date,programmers,message,files)
            self.listOfCommits.append(commit)
            #add this commit to the programmers commit listOfCommits
            for p in programmers:
                p.addToCommitList(commit)

            #for each file in this commit: add the commit to the right list
            for fKey, fInfo in fileStatus.items():
                file = fInfo['File']
                file.addCommit(commit,fInfo['Status'])

            #if all the commits are handled, close the file
            f.close()



    #parses date into a struct_time format
    def parseDate(self,date):
        date = time.strptime(date,"%A %d %B %Y %H:%M:%S")
        return date


    #parse the programmers and return as list
    def getProgrammers(self,message):
        programmers = []
        #parse each collaborator and search if he already exists
        prog = self.searchProgrammer(progName)
        #no existing programmer found with this name, create one
        if(not isinstance(prog,Programmer.Programmer)):

            prog = Programmer.Programmer(progName,self.programmerIterator)
            #this iterator will also be the node number
            self.programmerIterator = self.programmerIterator +1
            #add it to the general overview list
            self.listOfProgrammers.append(prog)


        programmers.append(prog)

        return programmers


    #search if the programmer with this name already exists in the list
    #@param name = name of the programmer
    #@returns that programmer object
    def searchProgrammer(self,name):

        for elem in self.listOfProgrammers:
            #if comparison is case insensitive, use this line instead
            #if(elem.getName().lower() == name.lower()):
            if(elem.getName() == name):
                return elem
        return ""


    #search if file with this path already exists
    #@param filePath = file path
    #@returns that file object
    def searchFile(self,filePath):
        for elem in self.listOfFiles:
            if(elem.getPath() == filePath):
                return elem
        return ""

    #function that triggers each file to calculates its importance
    def calculateFileImportance(self):
        firstAndLastTimeStamp = self.getFirstAndLastCommitDate()

        for file in self.listOfFiles:
            importance = file.calculateImportanceRatio(firstAndLastTimeStamp)


    #@return tuple of time stamp of the first and last commit
    def getFirstAndLastCommitDate(self):
        listOfTimestamps = []
        for commit in self.listOfCommits:
            listOfTimestamps.append(commit.getDate())

        listOfTimestamps.sort()
        lastTimeStamp = listOfTimestamps[-1]
        firstTimeStamp = listOfTimestamps[0]

        return (firstTimeStamp,lastTimeStamp)
