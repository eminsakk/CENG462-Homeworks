class Node:
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.edges = []
    
    def getName(self):
        return self.nodeName

    def createEdges(self,blockList,size,nodeList):
        x = self.nodeName[0]
        y = self.nodeName[1]

        # Left
        if y - 1 >= 0 and (x, y - 1) not in blockList:
            node = findNode(x, y - 1,nodeList)
            self.edges.append((node,1))

        # Up
        if x - 1 >= 0 and (x - 1,y) not in blockList:
            node = findNode(x - 1,y,nodeList)
            self.edges.append((node,1))
        
        # Right
        if y + 1 < size and (x,y + 1) not in blockList:
            node = findNode(x,y + 1,nodeList)
            self.edges.append((node,1))
        
        if x + 1 < size and (x + 1,y) not in blockList:
            node = findNode(x + 1,y,nodeList)
            self.edges.append((node,1))
        
        
    def getEdges(self):
        return self.edges
    def getIndex(self):
        return (self.nodeName[1],self.nodeName[0])
class Graph:
    nodeList = []
    blockList = []
    def __init__(self,grid):
        for i in range(0,len(grid)):
            row = grid[i]
            for j in range(0,len(row)):
                nodeType = grid[i][j]
                tmpNode = None
                if nodeType != '#':
                    nodeName = (i,j,nodeType)
                    tmpNode =  Node(nodeName)
                    self.nodeList.append(tmpNode)
                
                if nodeType == 'E':
                    self.endNode = tmpNode
                elif nodeType == 'S':
                    self.startNode = tmpNode

                if nodeType == '#':
                    self.blockList.append((i,j))

        for node in self.nodeList:
            node.createEdges(self.blockList,len(grid),self.nodeList)

    def UCS(self):
        start = self.startNode
        goal = self.endNode

        #pq structure [node,path,cost,custumerNumber]
        priorityQueue = [[start,[start],0]]
        visitedNodes = set()

        while priorityQueue:
            poppedItem = popItem(priorityQueue)
            poppedNode = poppedItem[0]
            priorityQueue.remove(poppedItem)


            if poppedNode == None:
                continue
            #Goal Test
            if poppedItem[0] == goal:
                path = createPath(poppedItem[1])
                path.reverse()
                return path

            visitedNodes.add(poppedNode)

            for edge in poppedNode.getEdges():
                
                child = edge[0]
                newDistance = edge[1] + poppedItem[2]
                newPath = poppedItem[1] + [child]

                newPQItem = [child,newPath,newDistance]
                occurence = 0

                for item in newPQItem[1]:
                    if item == child:
                        occurence += 1

                if occurence > 1:
                    continue

                if child not in visitedNodes and not isInPQ(priorityQueue,newPQItem):
                    priorityQueue.append(newPQItem)
                elif isInPQ(priorityQueue,newPQItem):
                    idx = getIdx(priorityQueue,newPQItem)
                    if priorityQueue[idx][2] > newPQItem[2]:
                        priorityQueue[idx] = newPQItem
                else:
                    priorityQueue.append(newPQItem)
        return



def findNode(x,y,nodeList):

    for node in nodeList:
        if node.getName()[0] == x and node.getName()[1] == y:
            return node
    return 

def createPath(nodeList):
    p = []
    for item in nodeList:
        p.append(item.getIndex())
    return p

# Priority Queue Utilizer Functions.
def popItem(pq):
    node = None
    minVal = 99999999
    for item in pq:
        if item[2] < minVal:
            minVal = item[2]
            node = item
    return node


def isInPQ(pq,node):

    for item in pq:
        if item[0] == node:
            return True
    return False


def getIdx(pq,pqItem):
    i = 0
    for item in pq:
        if item[0] == pqItem[0] and pqItem[2] == item[2]:
            return i
        i += 1
    return None

# Priority Queue Utilizer Functions Ends.


def UCSParser(file_name):
    rawInput = open(file_name,"r").read()
    
    grid = []
    tmp = ""

    for i in range(0,len(rawInput)):
        if rawInput[i] == '\t':
            continue
        elif rawInput[i] == '.' or rawInput[i] == 'E' or rawInput[i] == '#' or rawInput[i] == 'S':
            tmp += rawInput[i]
        elif rawInput[i] == '\n' or i == len(rawInput) - 1 :
            grid.append(tmp)
            tmp = ""

        if i == len(rawInput) - 1:
            grid.append(tmp)
            tmp = ""
    return grid

def AStarParser(file_name):
    

    return None

def InformedSearch(method_name,problem_file_name):
    if method_name == "UCS":
        gridStr = UCSParser(problem_file_name)
        grid = Graph(gridStr)
        return grid.UCS()

    elif method_name == "AStar":
        AStarParser(problem_file_name)

    

    return 




if __name__ == "__main__":
    print(InformedSearch("UCS","sampleUCS.txt"))
