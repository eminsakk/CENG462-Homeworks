class Node:
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.edges = []

    def createEdges(self,edgeList):
        for n in edgeList:
            if n.getName() != self.getName() and self.getName()[2] == 'C' and n.getName()[2] != 'S':
                self.edges.append(n.getName())
            elif n.getName() != self.getName() and self.getName()[2] == 'S':
                self.edges.append(n.getName())
        # To make things easier sort the edge array.
        #self.edges = self.sortEdges()

    def sortEdges(self):
        # Quick Sort Algorithm.
        smallerThanPivot = []
        biggerThanPivot = []
        
        if len(self.edges) <= 1:
            return self.edges
        
        pivot = self.edges[0]

        for edge in self.edges:
            if abs(edge[0] - self.getName()[0]) < abs(pivot[0] - self.getName()[0]):
                smallerThanPivot.append(edge)
            elif abs(edge[1] - self.getName()[1] < abs(pivot[1] - self.getName()[1])):
                smallerThanPivot.append

    # Getter Functions.
    def getEdges(self):
        return self.edges

    def getName(self):
        return self.nodeName

class Graph:
    nodeList = [] # [c,s,f,c,c,c,c]
    def __init__(self,grid):

        for i in range(0,len(grid)):
            row = grid[i]
            for j in range(0,len(row)):
                nodeType = row[j]
                if nodeType == 'S' or nodeType == 'F' or nodeType == 'C':
                    nodeName = (i,j,nodeType)
                    tmpNode = Node(nodeName)
                    self.nodeList.append(tmpNode)


        for node in self.nodeList:
            node.createEdges(self.nodeList)

    def printNodes(self):
        for x in self.nodeList:
            print(x.getName())


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
    
    if method_name == "DFS":
        return DFS(grid)
    elif method_name == 'BFS':
        return BFS(grid)
    else:
        return UCS(grid)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UnInformedSearch("DFS", "sampleproblem.txt")

# Searching Algorithms Implementations.
def DFS(grid):
    pass
def BFS(grid):
    pass
def UCS(grid):
    pass