

#Represents a file that is either Modified, Added or Deleted
class File:

    def __init__(self,path, fileID):

        self.path = path
        self.fileID = fileID
        self.importance = 1
        self.modifiedInCommits = []
        self.addedInCommits = []
        self.deletedInCommits = []


    def getPath(self):
        return self.path

    def getID(self):
        return self.fileID

    def getImportance(self):
        return self.importance

    def addCommit(self,commit,modifier):

        if ((modifier == "Modified") or (modifier == "Replacing")):


            if(not commit in self.modifiedInCommits):
                self.modifiedInCommits.append(commit)
        elif modifier == "Added":
            if(not commit in self.addedInCommits):
                self.addedInCommits.append(commit)
        elif modifier == "Deleted":
            if(not commit in self.deletedInCommits):
                self.deletedInCommits.append(commit)
        else:
            print("Modifier is not correct, given modifier: ",modifier," for file: ", self.path)

    #Function that returns if the file was modifier, added or deleted in this commit
    def getModifierStatus(self,commit):
        if(commit in self.modifiedInCommits):
            return "Modified"
        elif (commit in self.addedInCommits):
            return "Added"
        elif (commit in self.deletedInCommits):
            return "Deleted"
        else:
            print("Commit could not be found in the different modifier lists, commit number = ", commit.getRevisionNumber(), " file = ", self.path)


    #file is importance if it continues to grow over time
    #so when it get modified regularly

    def calculateImportance(self):
        timestamps = []
        importance = 1

        for commit in self.modifiedInCommits:
            #get all the time stamps
            timestamps.append(commit.getDate())
        for commit in self.addedInCommits:
            timestamps.append(commit.getDate())

        #order them chronologically
        timestamps.sort()

        for iterator in range(0,len(timestamps)-1):
            if(not(iterator == (len(timestamps)-1))):
                stamp1 = timestamps[iterator]
                stamp2 = timestamps[iterator+1]

                #get the number of months between 2 consecutive timestamps
                numberOfMonths = abs(stamp2.year - stamp1.year) * 12 + abs(stamp2.month - stamp1.month)

                #if 0 < number < 7, than add +1 to the importance
                if ((0 < numberOfMonths) and (numberOfMonths < 7)):
                    importance += 1

        self.importance = importance
        return importance


    #Function that calculates the importance of a file base on a ratio:
    #the number of months in which it was changed / the number of months is exists
    #@param firstAndLastTimeStamp  = tuple with the first timestamp of the log and the last
    def calculateImportanceRatio(self,firstAndLastTimeStamp):
        addedTimestamps = []
        for commit in self.addedInCommits:
            addedTimestamps.append(commit.getDate())
        addedTimestamps.sort()
        deletedTimestamps = []
        for commit in self.deletedInCommits:
            deletedTimestamps.append(commit.getDate())
        deletedTimestamps.sort()
        timestamps = []
        for commit in self.modifiedInCommits:
            timestamps.append(commit.getDate())
        for commit in self.addedInCommits:
            timestamps.append(commit.getDate())

        numberOfMonthsExistence = 0
        numberOfMonthsChanged = 0
        iteratorAdded = 0
        iteratorDeleted = 0


        if(not addedTimestamps):
            beginstamp = firstAndLastTimeStamp[0]
            #only 2 scenarios possible : 0 or 1 deleted timestamp
            if(not deletedTimestamps):
                endstamp = firstAndLastTimeStamp[1]
            else:
                endstamp = deletedTimestamps[0]
            numberOfMonthsExistence += self.calculateNumberOfMonthsExistence(beginstamp,endstamp)
            numberOfMonthsChanged += self.calculateNumberOfMonthsChanged(beginstamp,endstamp,timestamps)


        while(iteratorAdded < len(addedTimestamps)):
            beginstamp = addedTimestamps[iteratorAdded]
            iteratorAdded += 1

            if(iteratorDeleted == len(deletedTimestamps)):
                #all deleted stamps are done
                endstamp = firstAndLastTimeStamp[1]

            else:
                endstamp = deletedTimestamps[iteratorDeleted]
                iteratorDeleted += 1

            if(endstamp < beginstamp):
                beginstamp = firstAndLastTimeStamp[0]
                iteratorAdded -= 1


            numberOfMonthsExistence += self.calculateNumberOfMonthsExistence(beginstamp,endstamp)
            numberOfMonthsChanged += self.calculateNumberOfMonthsChanged(beginstamp,endstamp,timestamps)



        importance = numberOfMonthsChanged/numberOfMonthsExistence

        self.importance = importance
        return importance





    #calculate how many months this file exists between these 2 timestamps
    def calculateNumberOfMonthsExistence(self,beginstamp, endstamp):

        numberOfMonths = abs(endstamp.year - beginstamp.year) * 12 + abs(endstamp.month - beginstamp.month)
        numberOfMonths += 1
        return numberOfMonths

    #calculate in how many months between begin and end the file was changed
    #@param timestamps = list of timestamps when the file was committed
    def calculateNumberOfMonthsChanged(self,beginstamp,endstamp,timestamps):
        timestamps.sort()
        numberOfMonths = 0
        currentMonth = -1
        currentYear = -1
        for stamp in timestamps:
            #only consider the timestamps between the timespan
            if((stamp >= beginstamp)and(stamp <= endstamp)):
                if((stamp.month != currentMonth) or (currentYear != stamp.year)):
                    currentMonth = stamp.month
                    currentYear = stamp.year
                    numberOfMonths += 1

        return numberOfMonths

    #returns a list of time stamps of the commits this programmer was involved in
    #@param programmer the programmer we're searching the commits for
    #@return a list of time stamps
    def getListOfCommitTimestampsByProgrammer(self,programmer):
        timestamps = []
        #only added and modified is important
        for commit in self.modifiedInCommits:
            if(commit.hasAsContributor(programmer)):
                timestamps.append(commit.getDate())
        for commit in self.addedInCommits:
            if(commit.hasAsContributor(programmer)):
                date = commit.getDate()
                if(not date in timestamps):
                    timestamps.append(date)

        return timestamps

    #returns a list of time stamps of the commits these programmers were involved in
    #@param listOfProgrammers a list of the programmers we're searching the commits for
    #@return a list of distinct time stamps
    def getListOfCommitTimestampsForAllTheseProgrammers(self,listOfProgrammers):
        timestamps = set([])
        for prog in listOfProgrammers:
            timestamps |= set(self.getListOfCommitTimestampsByProgrammer(prog))
        return list(timestamps)


    #@return set of all the programmers that worked on this file
    def getListOfContributors(self):
        programmers = set([])
        for commit in self.modifiedInCommits:
            contributors = commit.getContributors()
            programmers |= set(contributors)
        for commit in self.addedInCommits:
            contributors = commit.getContributors()
            programmers |= set(contributors)
        return programmers


    #Function that returns a list with all the commits in which this file was added or modified
    def getListOfAddedAndModifiedCommits(self):
        return(self.addedInCommits + self.modifiedInCommits)
