

#Represents a file that is either Modified, Added or Deleted
class File:

    def __init__(self,path):

        self.path = path
        self.importance = 1
        self.modifiedInCommits = []
        self.addedInCommits = []
        self.deletedInCommits = []


    def getPath(self):
        return self.path

    def getImportance(self):
        return self.importance

    def addCommit(self,commit,modifier):
        if modifier == "Modified":
            self.modifiedInCommits.append(commit)
        elif modifier == "Added":
            self.addedInCommits.append(commit)
        elif modifier == "Deleted":
            self.deletedInCommits.append(commit)

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
