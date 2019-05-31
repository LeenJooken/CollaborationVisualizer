import Programmer

#class that represents a node
class Node:

    def __init__(self,programmer,weight):
        self.programmer = programmer
        self.weight = weight
        self.ID = programmer.getID()


    def getLabel(self):
        return (self.programmer.getName())

    def getID(self):
        return self.ID

    def getWeight(self):
        return self.weight

    def setWeight(self,weight):
        self.weight = weight

    def getDistinctFileList(self):
        return self.programmer.getDistinctFileList()
