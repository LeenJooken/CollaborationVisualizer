from time import mktime
from datetime import datetime
#class that represents 1 commit
#includes:
# Revision number
# author
# date (struct_time format)
# message
# contributors
# list of files
class Commit:

    def __init__(self,revision_number,author,date,contributors,message,files):
            self.revision_number = revision_number
            self.author = author
            self.date = date
            self.contributors = contributors
            self.message = message
            self.files = files

    def getRevisionNumber(self):
        return self.revision_number

    def getContributors(self):
        return self.contributors

    def getFiles(self):
        return self.files

    def getDate(self):
        return self.date

    def addContributor(self,programmer):
        if (not programmer in self.contributors):
            self.contributors.append(programmer)

    def addFile(self,file):
        if (not file in self.files):
            self.files.append(file)

    #function that checks whether this programmer contributed to this commit
    #@param: programmers to check for
    #returns true or false
    def hasAsContributor(self,programmer):
        return (programmer in self.contributors)

    #@return whether this commit is a pair programming commit or not
    def isPairProgramming(self):
        return(len(self.contributors) > 1)

    #Function that checks whether the list in args contains all the contributors on this commit
    #@param listOfContributors list of programmers
    #@return logical value that represents whether all contributors of this commit appear in the arg list
    def doesListContainAllContributors(self,listOfContributors):
        return(all(elem in listOfContributors  for elem in self.contributors))
