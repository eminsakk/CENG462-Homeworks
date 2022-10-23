class Node:
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.edges = []

    # Getter Functions.
    def getEdges(self):
        return self.edges

    def getName(self):
        return self.nodeName

class Graph:
    nodeList = []
    def __init__(self,grid):

        for i in range(0,len(grid)):
            row = grid[i]
            for j in range(0,len(row)):
                nodeType = row[j]
                if nodeType == 'S' or nodeType == 'F' or nodeType == 'C':
                    nodeName = (i,j)
                    tmpNode = Node(nodeName)
                    self.nodeList.append(tmpNode)
        
        for node in self.nodeList:
            for toBeAdd in self.nodeList:
                if node.getName() != toBeAdd.getName():
                    node.edges.append(toBeAdd.getName())



    def printNodes(self):
        for x in self.nodeList:
            print(x.getName())
            print(x.getEdges())


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
    grid.printNodes()

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