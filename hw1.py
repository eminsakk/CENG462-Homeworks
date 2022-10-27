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

    def getIndex(self):
        return (self.getName()[0],self.getName()[1])

    # Getter Functions.
    def getEdges(self):
        return self.edges

    def getName(self):
        return self.nodeName

class Graph:
    nodeList = []
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
    # DFS Function Area Ends.


    # BFS Function Area Starts. 
    def BFS(self,minCustomer):

        visitedNodes = set()
        traversalPath = []
        queue = []

        queue.append(self.startNode)

        while queue:

            tmpNode = queue.pop(0)
            traversalPath.append(tmpNode.getIndex())
            minCustomer -= 1
            if minCustomer < 0:
                break

            for adjacentNode in tmpNode.getEdges():
                if adjacentNode not in visitedNodes and adjacentNode != self.endNode:
                    queue.append(adjacentNode)
                    visitedNodes.add(adjacentNode)
        return traversalPath + [self.endNode.getIndex()]
    # BFS Function Area Ends.


    #UCS Function Area Starts.


    def UCS(self,minCustomer):
        
        goalState = self.endNode
        startState = self.startNode

        if minCustomer == 0:
            return [startState.getIndex(),goalState.getIndex()]


        visitedNodes = set()

        #PQ structure => [node,path,cost]
        pq = []
        pq.append([startState,[startState],0])

        while pq:
            
            
            #Pop and remove function.
            poppedNode = pqPop(pq)
            pq.remove(poppedNode)


            if minCustomer == 0 and poppedNode[0] == goalState:
                return poppedNode[1]

            visitedNodes.add(poppedNode[0])


            for adjacentNode in poppedNode[0].getEdges():
                costBetween = calculateCost(adjacentNode,poppedNode[0])
                tmpPQItem = [adjacentNode,poppedNode[1] + adjacentNode, poppedNode[2] + costBetween]
                






    

    #UCS Function Area Ends.

def pqPop(pq):
    
    minVal = 999999999
    poppedNode = None
    for item in pq:
        if item[2] < minVal:
            minVal = item[2]
            poppedNode = item

    return poppedNode


def calculateCost(node1,node2):

    xDistance = abs(node1.getName()[0] - node2.getName()[0])
    yDistance = abs(node1.getName()[1] - node2.getName()[1])

    return xDistance + yDistance

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
    if minCustomer <= grid.customerNumber:
        if method_name == "DFS":
            return grid.DFS(minCustomer)
        
        elif method_name == "BFS":
            return grid.BFS(minCustomer)

    return None
def compareTwoNode(victimNode,node1,node2):
    node1_Idx = node1.getIndex()
    node2_Idx = node2.getIndex()

    victimNodeIdx = victimNode.getIndex()
    
    node1_victim_range = abs(victimNodeIdx[0] - node1_Idx[0]) + abs(victimNodeIdx[1] - node1_Idx[1])
    node2_victim_range = abs(victimNodeIdx[0] - node2_Idx[0]) + abs(victimNodeIdx[1] - node2_Idx[1])

    return node1_victim_range < node2_victim_range




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #Şu anlık print.
    print(UnInformedSearch("DFS", "sampleproblem.txt"))

# Searching Algorithms Implementations.
