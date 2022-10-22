class Node:
    def __init__(self,nodeName,edges):
        self.nodeName = nodeName
        self.edges = edges
    def getEdges(self):
        return self.edges
class Graph:
    nodeList = []
    customerList = []
    def __init__(self,grid):
        for i in range(0,len(grid)):
            row = grid[i]
            for j in range(0,len(row)):
                nodeName = (i,j)
                # Add Edges
                edges = self.createEdges(len(grid),len(row),i,j)
                tmpNode = Node(nodeName, edges)
                self.nodeList.append(tmpNode)
        for node in self.nodeList:
            xPos = node.nodeName[0]
            yPos = node.nodeName[1]
            if grid[xPos][yPos] == 'C':
                self.customerList.append(node)
            elif grid[xPos][yPos] == 'S':
                self.startNode = node
            elif grid[xPos][yPos] == 'F':
                self.endNode = node
    def printNodes(self):
        for x in self.nodeList:
            print(x.nodeName)
            print(x.getEdges())
    

    def createEdges(self,rowLen,colLen,currPosX,currPosY):
        edgeList = []
        if currPosX  + 1 < rowLen:
            edgeList.append((currPosX + 1,currPosY))
        if currPosX - 1 >= 0:
            edgeList.append((currPosX - 1,currPosY))
        if currPosY + 1 < colLen:
            edgeList.append((currPosX,currPosY + 1))
        if currPosY - 1 >= 0:
            edgeList.append((currPosX,currPosY - 1))
        return edgeList

def parseInput(file_name):
    # This function parses the input file and return as it to a dictionary.

    # Get the minimum number of customer to be arrived
    rawInput = open(file_name, "r").read()
    startIdx = rawInput.find(" ") + 1
    digitSize = rawInput[startIdx:].find(",")
    neededCustomer = int(rawInput[startIdx:startIdx + digitSize])
    # Get the grid as a list
    startIdx = startIdx + digitSize + 8

    gridString = rawInput[startIdx:len(rawInput) - 1]
    
    grid = []
    flag = False    
    tmpStr = ''

    for char in gridString:
        if char == "'" and len(tmpStr) == 0:
            flag = True
            continue
        elif char == "'" and len(tmpStr) != 0:
            flag = False
            grid.append(tmpStr)
            tmpStr = ''
        if flag:
            tmpStr += char
    
    parsedInput = { "min" : neededCustomer, "env": grid}
    return parsedInput
    

def UnInformedSearch(method_name,problem_file_name):
    dictionary = parseInput(problem_file_name)
    grid = Graph(dictionary["env"])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UnInformedSearch("DFS", "sampleproblem.txt")


# Searching Algorithms Implementations.
def BFS():
    pass
def DFS():
    pass
def UCS():
    pass