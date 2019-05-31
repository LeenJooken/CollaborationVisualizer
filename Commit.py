from time import mktime
from datetime import datetime
#class that represents 1 commit
#includes:
# Revision number
# author
# date (struct_time format)
# message
class Commit:

    def __init__(self,revision_number,author,date,contributors,message,files):
            self.revision_number = revision_number
            self.author = author
            dt = datetime.fromtimestamp(mktime(date))
            self.date = dt
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

    #function that checks whether this programmer contributed to this commit
    #@param: programmers to check for
    #returns true or false
    def hasAsContributor(self,programmer):
        return (programmer in self.contributors)
