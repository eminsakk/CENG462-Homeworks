class Node:
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.edges = []

    def createEdges(self,edgeList):
        for n in edgeList:
            if n.getName() != self.getName() and self.getName()[2] == 'C' and n.getName()[2] != 'S':
                self.edges.append(n)
            elif n.getName() != self.getName() and self.getName()[2] == 'S':
                self.edges.append(n)
        # To make things easier sort the edge array.
        #self.edges = self.sortEdges(self.edges)
    def getIndex(self):
        return (self.getName()[0],self.getName()[1])

    # Getter Functions.
    def getEdges(self):
        return self.edges

    def getName(self):
        return self.nodeName

class Graph:
    nodeList = [] # [c,s,f,c,c,c,c]
    def __init__(self,grid):
        self.customerNumber = 0
        for i in range(0,len(grid)):
            row = grid[i]
            for j in range(0,len(row)):
                nodeType = row[j]
                if nodeType == 'S' or nodeType == 'F' or nodeType == 'C':
                    nodeName = (i,j,nodeType)
                    tmpNode = Node(nodeName)
                    self.nodeList.append(tmpNode)

                    if nodeType == 'F':
                        self.endNode = tmpNode
                    if nodeType == 'S':
                        self.startNode = tmpNode
                    if nodeType == 'C':
                        self.customerNumber += 1

        for node in self.nodeList:
            node.createEdges(self.nodeList)

    def printNodes(self):
        for x in self.nodeList:
            print(x.getName())
            nodeEdges = []
            for edge in x.getEdges():
                nodeEdges.append(edge.getName())
            print(nodeEdges)


    # DFS Traversal Function Area
    def DFS(self,minCustomer):
        visitedNodes = set()
        return [self.startNode.getIndex()] + self.DFSHelper(visitedNodes,self.startNode,minCustomer) + [self.endNode.getIndex()]


    def DFSHelper(self,visitedNodes,s_node,min):
        if min == 0:
            return []

        visitedNodes.add(s_node)

        for adjacentNode in s_node.getEdges():
            if adjacentNode not in visitedNodes and adjacentNode != self.endNode:
                newMin = min - 1
                return [adjacentNode.getIndex()] + self.DFSHelper(visitedNodes,adjacentNode,newMin)
    # DFS Traversal Function Area Ends.


    def BFS(self,minCustomer):
        visitedNodes = set()
        traversalPath = []
        queue = []

        queue.append(self.startNode)

        while queue:

            tmpNode = queue.pop(0)
            traversalPath.append(tmpNode.getIndex())

            if minCustomer == 0:
                break

            for adjacentNode in tmpNode.getEdges():
                if adjacentNode not in visitedNodes and adjacentNode != self.endNode:
                    queue.append(adjacentNode)
                    visitedNodes.add(adjacentNode)
                    minCustomer -= 1
        return traversalPath + [self.endNode.getIndex()]
    
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
    inp  = parseInput(problem_file_name)
    grid = Graph(inp["env"])
    #grid.printNodes()
    minCustomer = inp["min"]
    
    if method_name == "DFS":
        print("DFS Traversal:")
        print(grid.DFS(minCustomer))
    
    elif method_name == "BFS":
        print("BFS Traversal:")
        print(grid.BFS(minCustomer))


def compareTwoNode(victimNode,node1,node2):
    node1_Idx = node1.getIndex()
    node2_Idx = node2.getIndex()

    victimNodeIdx = victimNode.getIndex()
    
    node1_victim_range = abs(victimNodeIdx[0] - node1_Idx[0]) + abs(victimNodeIdx[1] - node1_Idx[1])
    node2_victim_range = abs(victimNodeIdx[0] - node2_Idx[0]) + abs(victimNodeIdx[1] - node2_Idx[1])

    return node1_victim_range < node2_victim_range



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UnInformedSearch("BFS", "sampleproblem.txt")

# Searching Algorithms Implementations.
