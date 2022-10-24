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
        self.edges = self.sortEdges(self.edges)


    def sortEdges(self,edgeList):
        # Quick Sort Algorithm.
        smallerThanPivot = []
        biggerThanPivot = []
        equalToPivot = []
        if len(edgeList) <= 1:
            return edgeList
        
        pivot = edgeList[0]

        for edge in edgeList:
            if compareTupleEqual(edge,pivot,self.getName()):
                equalToPivot.append(edge)
            elif compareTupleRow(edge,pivot,self.getName()):
                smallerThanPivot.append(edge)
            elif not compareTupleRow(edge,pivot,self.getName()):
                biggerThanPivot.append(edge)
            elif compareTupleCol(edge,pivot,self.getName()):
                smallerThanPivot.append(edge)
            elif not compareTupleRow(edge,pivot,self.getName()):
                biggerThanPivot.append(edge)
            
        return self.sortEdges(smallerThanPivot) + equalToPivot + self.sortEdges(biggerThanPivot)


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
            print(x.getEdges())

def compareTupleRow(tup1,tup2,nodeTuple):
    return abs(nodeTuple[0] - tup1[0]) < abs(nodeTuple[0] - tup2[0])
def compareTupleCol(tup1,tup2,nodeTuple):
    return abs(nodeTuple[1] - tup1[1]) < abs(nodeTuple[1] - tup2[1])
def compareTupleEqual(tup1,tup2,nodeTuple):
    print((abs(nodeTuple[0] - tup1[0]) == abs(nodeTuple[0] - tup2[0])) and (abs(nodeTuple[1] - tup1[1]) == abs(nodeTuple[1] - tup2[1])))
    return abs(nodeTuple[0] - tup1[0]) == abs(nodeTuple[0] - tup2[0]) and abs(nodeTuple[1] - tup1[1]) < abs(nodeTuple[1] - tup2[1])

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