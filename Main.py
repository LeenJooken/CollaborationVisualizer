import Output
import argparse
import Graph
import Log
import GraphExpansionPack

#main function of the program
def main(log_file,nodes_file,edges_file):
    #read and parse the log
    log = Log.Log(log_file)
    #construct the graph
    print("Building the graph:")
    socialgraph = Graph.Graph(log.getlistOfProgrammers(),log.getListOfCommits(),log.getNodeIterator())#,log.getTotalImportanceAllFiles())
    nodes = socialgraph.getNodesList()
    edges = socialgraph.getEdgesList()
    clusterNodes = socialgraph.getClusterNodesList()

    clusterEdges = socialgraph.getClusterEdgesList()

    #expand the graph with filenodes
    graphExpansionBuilder = GraphExpansionPack.GraphExpansionPack(socialgraph)
    fileNodesDictionary = graphExpansionBuilder.expandWithFileNodes()

    print("Writing the output files")
    writeOutput = Output.Output()
    writeOutput.writeGraphToCSV(nodes,edges,clusterNodes,clusterEdges,nodes_file,edges_file,fileNodesDictionary)
    print("Done")



########################################
#parse the command line arguments
print("Parsing the arguments")
parser = argparse.ArgumentParser()
parser.add_argument("-s","--source",help="pass the sourcefile to be read")
parser.add_argument("-nf","--nodes_filename",help="pass the nodes CSV filename")
parser.add_argument("-ef","--edges_filename",help="pass the edges CSV filename")

args = parser.parse_args()
log_file = args.source
nodes_file = args.nodes_filename
edges_file = args.edges_filename

#run the program
main(log_file,nodes_file,edges_file)
