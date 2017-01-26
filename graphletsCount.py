import os
import sys

def readLeda(networkFile):
    nodeList = []
    edgeList = []

    fRead = open(networkFile, 'r')

    mode = 0

    for line in fRead:
        if mode == 0 and line.startswith('|'):
            mode = 1

        if mode == 1 and line.startswith('|'):
            nodeList.append(line.strip().strip('|').strip('{').strip('}'))
        elif mode == 1 and not line.startswith('|'):
            mode = 2
        elif mode == 2 and line.strip().endswith('}|'):
            splitted = line.strip().split(' ')
            edgeList.append( [ int(splitted[0]) - 1, int(splitted[1]) - 1] )

    fRead.close()

    return (nodeList, edgeList)

# Write the network in a format that is ready to get executed by ORCA
def writeORCA(edgeList, nodeCount, outputFile):

    fWrite = open(outputFile, 'w')

    fWrite.write(str(nodeCount) + ' ' + str(len(edgeList)) + '\n')

    for edge in edgeList:
        fWrite.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')

    fWrite.close()

# Read the temporary ndump2 file and create the original one
def formatNdump2(tempNdump2File, originalNdump2, nodeList):
    # Read the temporary result file
    fRead = open(tempNdump2File, 'r')
    fWrite = open(originalNdump2, 'w')

    lineID = 0
    for line in fRead:
        fWrite.write(str(nodeList[lineID]) + ' ' + line)

        lineID += 1

    fRead.close()
    fWrite.close()


# Function to compute the graphlet counts from ndump2 files
def getGraphletFreq(signList):
    orbits = [0, 2, 3, 5, 7, 8, 9, 12, 14, 17, 18, 23, 25, 27, 33, 34, 35, 39, 44, 45, 50, 52, 55, 56, 61, 62, 65, 69, 70, 72]
    weights = [2, 1, 3, 2, 1, 4, 1, 2, 4, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 5]


    # Derive the graphlet counts from the orbit degrees
    graphletCounts = []

    for i in range(len(orbits)):
        orbit = orbits[i]
        sumCount = sum([val[orbit] for val in signList])
        graphletCounts.append(sumCount / weights[i])

    return graphletCounts

# Read the ndump2 files and compute the number of graphlets from it
def getGraphletCounts(filePath):
    fRead = open(filePath, 'r')

    signatureList = []
    for line in fRead:
        signatureList.append([float(val) for val in line.strip().split(' ')[1:]])

    fRead.close()

    return getGraphletFreq(signatureList)

    # Output the graphlet counts into the outputPath gr_freq file
def outputGrCounts(grCounts, outputPath):

    fWrite = open(outputPath, 'w')
    for i in range(30):
        fWrite.write(str(i) + '\t' + str(int(grCounts[i])) + '\n')
    fWrite.close()

def count(netFileName):
    # Read the LEDA formatted network
    (nodeList, edgeList) = readLeda(netFileName)

    # Write in ready to ORCA counting format
    outputFileName=netFileName.rsplit('.', 1)[0]+'_orca.txt'

    writeORCA(edgeList, len(nodeList), outputFileName)


    # Run the ORCA graphlet counting code with the resulting file
    tempNdump2File = netFileName.rsplit('.', 1)[0] + '_temp.ndump2'
    cmd = './orca 5 ' + outputFileName + ' ' + tempNdump2File
    os.system(cmd)

    # Format the temp file to original format
    originalNdump2 = netFileName.rsplit('.', 1)[0] + '.ndump2'
    formatNdump2(tempNdump2File, originalNdump2, nodeList)

    # Counting finished remove the temp network file
    os.remove(outputFileName)
    os.remove(tempNdump2File)

    # Count the graphlets
    grCounts = getGraphletCounts(originalNdump2)
    grFile = originalNdump2.rsplit('.', 1)[0] + '.gr_freq'
    outputGrCounts(grCounts, grFile)


if __name__ == "__main__":
    # Process the program parameters
    #ndumpFolder = sys.argv[1]

    #directory = os.walk(ndumpFolder)

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        #path = file[0]

        for fileName in file[2]:
            if fileName.endswith('.gw'):
                count(fileName)

