#This class is designed to calculate the weights of the edges
import operator
class EdgeWeightCalculator:

    def __init__(self,edgeslist):
        self.edgesList = edgeslist

        #weight matrix for the metrics
        self.FSW = 0.40
        self.PCW = 0.60



    def calculateEdgeWeights(self):
        freqDict = {}
        proxDict = {}
        for edge in self.edgesList:
            freqSign = self.calculateFrequencySignificance(edge)
            proxCorr = self.calculateProximityCorrelation(edge)

            #save in dictionary cause we need to normalize the values once we have all of them
            freqDict[edge] = freqSign
            proxDict[edge] = proxCorr



        #normalize the freqSign and proxCorr for each edge
        fsMin = self.getMinValueFromDict(freqDict)
        fsMax = self.getMaxValueFromDict(freqDict)
        pcMin = self.getMinValueFromDict(proxDict)
        pcMax = self.getMaxValueFromDict(proxDict)



        for edge in self.edgesList:

            if(fsMax == fsMin):
                freqSign = 1/len(freqDict)

            else:

                freqSign = (freqDict[edge]-fsMin)/(fsMax-fsMin)

            if(pcMax == pcMin):
                proxCorr = 1/len(proxDict)
                
            else:

                proxCorr = (proxDict[edge]-pcMin)/(pcMax-pcMin)
            #weight is a combi of those metrics
            weight = self.FSW*freqSign + self.PCW*proxCorr
            edge.setWeight(weight)




    def getMinValueFromDict(self,dict):
        minValue = min(dict.items(), key=operator.itemgetter(1))[1]
        return minValue

    def getMaxValueFromDict(self,dict):
        maxValue = max(dict.items(), key=operator.itemgetter(1))[1]
        return maxValue

    #Function that calculates the frequency significance of the edge
    #From fuzzy mining: binary significance metrics
    #The more distinct files they work on together
    #Problem: less but more important files vs more but less important files
    #Solution: work with the importance of the files
    #Problem 2: are we gonna work with a timespan, to make sure the collab is relevant?
    #is also datavalue correlation !
    def calculateFrequencySignificance(self,edge):
        freqSign = 0
        #returns a dictionary with the file as key
        #and 'sourceTimestamps' 'targetTimestamps' as values (both lists of timestamps)
        files = edge.getDistinctCollabFiles()
        for file,stamps in files.items():
            #compare the timestamps
            #everything that takes place within the span of 1 week of each other is considered 1 block
            timestamps1 = stamps['sourceTimestamps']
            timestamps1.sort()

            timestamps2 = stamps['targetTimestamps']
            timestamps2.sort()



            numberOfTimes = self.calculateFreqTimestampDifferences(timestamps1,timestamps2)

            freqSign += (numberOfTimes * file.getImportance())



        return freqSign


    def calculateFreqTimestampDifferences(self,timestamps1, timestamps2):
        iterator1 = 0
        iterator2 = 0
        numberOfTimes = 0
        inBlock = False


        while ((iterator1 < len(timestamps1)) and (iterator2 < len(timestamps2))):
            if(timestamps1[iterator1] < timestamps2[iterator2]):
                stamp1 = timestamps1[iterator1]
                stamp2 = timestamps2[iterator2]
            else:
                stamp2 = timestamps1[iterator1]
                stamp1 = timestamps2[iterator2]

            daysbetween = (stamp2-stamp1).days
            if(daysbetween <= 7):
                if(not inBlock):
                    numberOfTimes += 1
                    inBlock = True
            else:
                inBlock = False
            #the first stamp -> move iterator forward
            if(timestamps1[iterator1] < timestamps2[iterator2]):
                iterator1 += 1
            else:
                iterator2 += 1

        return numberOfTimes


    #Function that calculates the proximity correlation
    #Fuzzy mining binary correlation metric
    #Pair programming is a very close collaboration
    #Sum of the importance of their pair programming files
    #every distinct file: take sum of importance
    #returning files: check if timespan between them is big enough,
    #cause you could a lot of small commits in 1 day and that would skew the results
    def calculateProximityCorrelation(self,edge):
        proxCorr = 0
        #return dictionary with 'File' as key and a list of timestamps as value
        files = edge.getPairProgrammingFiles()
        for file,timestamplist in files.items():
            if len(timestamplist) > 1:
                #order the timestamps
                timestamplist.sort()

                #check between 2 consecutive stamps if the timespan in big enough to count as a separate collab
                for iterator in range(0,len(timestamplist)-1) :
                    if(not(iterator == (len(timestamplist)-1))):
                        stamp1 = timestamplist[iterator]
                        stamp2 = timestamplist[iterator+1]
                        #only if there is at least a month in between session we could the importance double
                        #get the number of months between 2 consecutive timestamps
                        numberOfMonths = abs(stamp2.year - stamp1.year) * 12 + abs(stamp2.month - stamp1.month)



                        if(numberOfMonths >=1):
                            proxCorr += file.getImportance()

            #else:
            #No matter what: there is a least 1 file, so they have at least collabed 1 time
            proxCorr += file.getImportance()



        return proxCorr
