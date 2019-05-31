# program that writes a nodes and edges CSV

import operator
import argparse
import csv

#class that handles all output
class Output:
    def __init__(self):
        self.anonymizationCounter = 1

    def anonymizeProgrammer(self):
        name = "P" + str(self.anonymizationCounter)
        self.anonymizationCounter += 1
        return name

    def anonymizeCluster(self,numberOfMembers):
        name = ""
        for i in range(numberOfMembers):
            if(i == 0):
                name += "P" + str(self.anonymizationCounter)
            else:
                name += "+P"+str(self.anonymizationCounter)
            self.anonymizationCounter += 1
        return name


    #write Id, Label and weight of the nodes to csv
    #@param nodes : list of nodes
    #@param clusterNodes: list of cluster nodes
    #@param filename: csv file
    #@returns
    def writeNodesCSV(self,nodes,clusterNodes,filename):
        #check first if the filename isnt empty
        if not filename:
            filename = "nodes.csv"

        writer = csv.writer(open(filename,'w+',newline=''),delimiter=";")
        #write the header: Id, Label and weight
        writer.writerow(["Id","Label","Weight","Cluster"])
        #write all the nodes to the file
        for node in nodes:
            label = node.getLabel()
            #for anonymization, uncomment the next line
            #label = self.anonymizeProgrammer()
            writer.writerow([node.getID(),label,node.getWeight(),False])

        #write all cluster nodes to the file
        for node in clusterNodes:
            label = node.getLabel()
            #for anonymization, uncomment the next line
            #label = self.anonymizeCluster(node.getNumberOfMembers())
            writer.writerow([node.getID(),label,node.getWeight(),True])


    #write Source, Target, Weight, Type (always undirected) of the edges to csv
    #@param edges : dictionary of edges containing for each edge: [source target ID, target node ID],{weight, type}
    #@param filename: csv file
    #@returns
    def writeEdgesCSV(self,edges,clusterEdges,filename):
        #check first if the filename isnt empty
        if not filename:
            filename = "edges.csv"

        writer = csv.writer(open(filename,'w+',newline=''),delimiter=";")
        #write the header: Source, Target, Weight, type
        writer.writerow(["Source","Target","Weight","Type","CollaborationType"])
        #write all the edges to the file
        for edge in edges:
            writer.writerow([edge.getSourceNodeID(),edge.getTargetNodeID(),edge.getWeight(),edge.getType(),edge.getCollaborationType()])

        #write all cluster edges to the file
        for edge in clusterEdges:
            writer.writerow([edge.getSourceNodeID(),edge.getTargetClusterID(),edge.getWeight(),edge.getType(),edge.getCollaborationType()])



    #Write graph to 2 seperate CSVs: nodes and edges
    def writeGraphToCSV(self,nodes,edges,clusterNodes,clusterEdges,nodes_filename,edges_filename):
        self.writeNodesCSV(nodes,clusterNodes,nodes_filename)
        self.writeEdgesCSV(edges,clusterEdges,edges_filename)


    def writeFileImportanceToFile(self,listOfFiles):
        filename = "fileImportance.csv"

        writer = csv.writer(open(filename,'w+',newline=''),delimiter=";")
        writer.writerow(["filepath","importance"])

        for file in listOfFiles:
            writer.writerow([file.getPath(),file.getImportance()])
