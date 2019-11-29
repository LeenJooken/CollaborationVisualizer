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
            writer.writerow([node.getID(),label,node.getWeight(),"False"])

        #write all cluster nodes to the file
        for node in clusterNodes:
            label = node.getLabel()
            #for anonymization, uncomment the next line
            #label = self.anonymizeCluster(node.getNumberOfMembers())
            writer.writerow([node.getID(),label,node.getWeight(),"True"])

    #Function that writes the file nodes to the file
    #@prerequisite: thes base graph nodes has to be written first, so writeNodesCSV must have been valled beforehand
    #@param nodes list of file nodes to write to the file
    #@param clusterNodes list of cluster file nodes to write to the file
    #@param filename name of the file that the nodes are being written to
    def writeFileNodesCSV(self,nodes,clusterNodes,filename):
        if not filename:
            filename = "nodes.csv"
        #append nodes to file -> base graph nodes have to be written first
        writer = csv.writer(open(filename,'a+',newline=''),delimiter=";")
        #header has already been written in the writeNodesCSV function
        for node in nodes:
            writer.writerow([node.getID(),node.getLabel(),node.getWeight(),"NA"])

        #write the cluster nodes to the CSV
        for node in clusterNodes:
            writer.writerow([node.getID(),node.getLabel(),node.getWeight(),"NA"])



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

    #Function that writes the filenode edges to the file
    #@prerequisite: the base graph edges has to be written first, so writeEdgesCSV must have been called beforehand
    #@param edges the filenode edges to write to the file
    #@param clusterEdges the cluster file nodes edges to write to the file
    #@param filename the name of the edges csv file
    def writeFileEdgesCSV(self,edges,clusterEdges,filename):
        if not filename:
            filename = "edges.csv"

        writer = csv.writer(open(filename,'a+',newline=''),delimiter=";")
        #The header has already been added when the base graph edges were written (see prerequisite)
        for edge in edges:
            writer.writerow([edge.getBaseGraphNodeID(),edge.getFileNodeID(),edge.getWeight(),edge.getType(),edge.getCollaborationType()])
        for edge in clusterEdges:
            writer.writerow([edge.getBaseGraphClusterNodeID(),edge.getClusterFileNodeID(),edge.getWeight(),edge.getType(),edge.getCollaborationType()])



    #Write graph to 2 seperate CSVs: nodes and edges
    def writeGraphToCSV(self,nodes,edges,clusterNodes,clusterEdges,nodes_filename,edges_filename,fileNodesDictionary):
        self.writeNodesCSV(nodes,clusterNodes,nodes_filename)
        self.writeEdgesCSV(edges,clusterEdges,edges_filename)
        #if the graph was extended with filenodes and fileedges, write them to the csv
        if(fileNodesDictionary):
            self.writeFileNodesAndEdges(fileNodesDictionary,nodes_filename,edges_filename)

    #Function that writes the file nodes and edges to their respective files
    def writeFileNodesAndEdges(self,fileNodesDictionary,nodefile,edgesfile):
        nodes = fileNodesDictionary["nodes"]
        edges = fileNodesDictionary["edges"]
        clusternodes = fileNodesDictionary["clusternodes"]
        clusteredges = fileNodesDictionary["clusteredges"]
        self.writeFileNodesCSV(nodes,clusternodes,nodefile)
        self.writeFileEdgesCSV(edges,clusteredges,edgesfile)

    def writeFileImportanceToFile(self,listOfFiles):
        filename = "fileImportance.csv"

        writer = csv.writer(open(filename,'w+',newline=''),delimiter=";")
        writer.writerow(["filepath","importance"])

        for file in listOfFiles:
            writer.writerow([file.getPath(),file.getImportance()])
