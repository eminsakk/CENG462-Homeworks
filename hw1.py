
# Node Class.
class Node:
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.edges = []

    def createEdges(self,edgeList):
        endNode = None
        for n in edgeList:
            if n.getName()[2] == "F":
                endNode = n
            if n.getName() != self.getName() and self.getName()[2] == "C" and n.getName()[2] != "S" and n.getName()[2] != "F":
                self.edges.append(n)
            elif n.getName() != self.getName() and self.getName()[2] == "S" and n.getName()[2] != "F":
                self.edges.append(n)
        
        if self.getName()[2] != "F":
            self.edges.append(endNode)
    def getIndex(self):
        return [self.getName()[0],self.getName()[1]]

    # Getter Functions.
    def getEdges(self):
        return self.edges

    def getName(self):
        return self.nodeName


# Graph Class
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

        start = self.startNode
        destination = self.endNode
        visitedNodes = set()

        priorityQueue = [[start,[start],0,0]]
        


        while priorityQueue:
            # Min cost pop
            poppedItem = popItem(priorityQueue)
            poppedNode = poppedItem[0]
            priorityQueue.remove(poppedItem)
            

            if goalTester(poppedItem,destination,minCustomer):
                print("COST = ", poppedItem[2])
                path = createPath(poppedItem[1])

                return path
            
            visitedNodes.add(poppedNode)

            for childNode in poppedNode.getEdges():
                childType = childNode.getName()[2]
                newDistance = calculateCost(childNode,poppedNode) + poppedItem[2]
                newPath = poppedItem[1] + [childNode]
                newCustomerCount = poppedItem[3]
                
                if childType == "C":
                    newCustomerCount += 1
                    if newCustomerCount > minCustomer:
                        continue

                
                newPQItem = [childNode,newPath,newDistance,newCustomerCount]

                occurence = 0

                for item in newPQItem[1]:
                    if item == childNode:
                        occurence += 1
                
                if occurence > 1:
                    continue

                if childNode not in visitedNodes and not isInPQ(priorityQueue,newPQItem):
                    if newCustomerCount == minCustomer and childType == "F":
                        priorityQueue.append(newPQItem)
                    elif childType == "C":
                        priorityQueue.append(newPQItem)

                elif isInPQ(priorityQueue,newPQItem):
                    idx = getIdx(priorityQueue,newPQItem)
                    if priorityQueue[idx][2] > newPQItem[2]:
                        priorityQueue[idx] = newPQItem
                else:
                    priorityQueue.append(newPQItem)
        return
    #UCS Function Area Ends.



def nodeInPQ(pq,pqItem):
    for item in pq:
        if item[0] == pqItem:
            return True
    return False
def getIdx(pq,pqItem):
    i = 0
    for item in pq:
        if item[0] == pqItem[0] and pqItem[3] == item[3]:
            return i
        i += 1
    return None

def isInPQ(pq,pqItem):
    
    for item in pq:
        if item[0] == pqItem[0] and item[3] == pqItem[3]:
            return True
    return False


def printPQ(pq):
    print("--------------Priority Queue Contents Starts--------------")
    for counter,item in enumerate(pq):
        print("---------- Priority Queue Item " , counter + 1, "----------")
        print("Node => " , item[0].getName())
        print("Path => ",createPath(item[1]))
        print("Cost = ", item[2])
        print("Customer Number = ", item[3])
    print("--------------Priority Queue Contents Ends--------------")

    #UCS Function Area Ends.

def createPath(nodeList):
    p = []
    for item in nodeList:
        p.append(item.getIndex())
    return p


def goalTester(pqItem,goalState,neededCustomer):
    n = pqItem[0]
    cust = pqItem[3]
    if n == goalState and neededCustomer == cust:
        return True
    return False
    

def calculateCost(node1,node2):

    xDistance = abs(node1.getName()[0] - node2.getName()[0])
    yDistance = abs(node1.getName()[1] - node2.getName()[1])
    return xDistance + yDistance

# PRIORITY QUEUE UTILIZER
def popItem(pq):
    node = None
    minVal = 99999999
    for item in pq:
        if item[2] < minVal:
            minVal = item[2]
            node = item
    return node


#Input Parser
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
        elif method_name == "UCS":
            return grid.UCS(minCustomer)

    return None


if __name__ == '__main__':
    print(UnInformedSearch("UCS", "sampleproblem.txt"))
