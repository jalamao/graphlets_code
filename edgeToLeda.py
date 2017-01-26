#!/usr/bin/env python

"""
	A script to convert an metabolic network edgelist to a LEDA formatted file
	The LEDA file will be written next to the edge_list file with '.gw' extension

	Run as:
		./list2leda.py <edge_list_file>
"""
import os
import sys


def edgeToLeda(inputFile):


    outputFile = inputFile.rsplit('.',1)[0] + '.gw'

    listOfInteractions = []
    listOfNodes = []
    nodeIndexes = {}

    # Read the txt file and identify the nodes and edges
    fRead = open(inputFile, 'r')

    for line in fRead:
        splitted = line.strip().split('\t')

        if splitted[0] <> splitted[1]:
            listOfInteractions.append((splitted[0], splitted[1]))

    fRead.close()


    nodeCount = 1
    for interaction in listOfInteractions:
        if interaction[0] not in nodeIndexes:
            listOfNodes.append(interaction[0])
            nodeIndexes[interaction[0]] = nodeCount
            nodeCount += 1

        if interaction[1] not in nodeIndexes:
            listOfNodes.append(interaction[1])
            nodeIndexes[interaction[1]] = nodeCount
            nodeCount += 1


    # Write the output file in leda format
    fWrite = open(outputFile, 'w')

    fWrite.write('LEDA.GRAPH\n')
    fWrite.write('string\n')
    fWrite.write('short\n')
    fWrite.write(str(len(listOfNodes)) + '\n')

    for node in listOfNodes:
        fWrite.write('|{' + node + '}|\n')

    fWrite.write(str(len(listOfInteractions)) + '\n')
    for edge in listOfInteractions:
        fWrite.write(str(nodeIndexes[edge[0]]) + ' ' + str(nodeIndexes[edge[1]]) + ' 0 |{}|\n')

    fWrite.close()

if __name__ == "__main__":
    # Process the program parameters
    ndumpFolder = sys.argv[1]

    directory = os.walk(ndumpFolder)

    # Pick the relevant files based on ndump2 extensions
    for file in directory:
        path = file[0]

        for fileName in file[2]:
            if fileName.endswith('.txt'):
                edgeToLeda(fileName)
