class TreeNode:
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.childrens = []

    def setChildren(self,childrenNodes):
        self.childrens = list(childrenNodes)

    def getName(self):
        return self.nodeName

    def getChildrens(self):
        return self.childrens

def fullZeroController(l):
    flag = True
    for num in l:
        if num != 0:
            flag = False
            return flag
    return flag

def createChildrens(state):
    childrens = []
    for i in range(0,len(state)):
        currNumber = state[i]

        if currNumber == 0:
            continue

        for j in range(0,currNumber):
            childNodeName = list(state)
            childNodeName[i] = j

            

            childNode = TreeNode(childNodeName)
            childrens.append(childNode)
    return childrens

def createGameTree(input):

    node = TreeNode(input)
    childrens = createChildrens(node.getName())
    for child in childrens:
        node.getChildrens().append(createGameTree(child.getName()))
    return node





### MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING STARTS HERE ###
def pruneMinimax(state,currPlayer,iteration,alpha,beta):
    currStateSum = sum(state.getName())
    
    if currStateSum == 0:
        #Assuming utility values as 1 and -1.
        if currPlayer == "MAX":
            
            return (state,-1,iteration + 1)
        else:
            return (state,1,iteration + 1)
    
    if currPlayer == "MAX":
        return pruneMaxValue(state,iteration + 1,alpha,beta)

    if currPlayer == "MIN":
        return pruneMinValue(state,iteration + 1,alpha,beta)


def pruneMaxValue(state,iteration,alpha,beta):
    v = -9999999
    node = None
    toAdd = iteration

    for child in state.getChildrens():
        nextLevel = pruneMinimax(child,"MIN",iteration + 1,alpha,beta)
        if nextLevel[1] >= v:
            node = child
            v = nextLevel[1]
            toAdd = nextLevel[2] + 1
        
        if v > beta:
            return node,v,toAdd 
        alpha = max(v,alpha)
        

    return node,v,toAdd 
    


def pruneMinValue(state,iteration,alpha,beta):
    v = 9999999
    node = None
    toAdd = iteration

    for child in state.getChildrens():
        nextLevel = pruneMinimax(child,"MAX",iteration + 1,alpha,beta)
        if nextLevel[1] < v:
            node = child
            v = nextLevel[1]
            toAdd = nextLevel[2] + 1
        if v < alpha:
            return node,v,toAdd 

        beta = min(v,beta)
    return node,v,toAdd 
### MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING ENDS HERE ###










### MINIMAX ALGORITHM STARTS HERE ###
def maxValue(state,iteration):
    v = -99999999
    node = None
    toAdd = 0


    for child in state.getChildrens():
        nextLevel = minimax(child,"MIN",iteration + 1)
        if nextLevel[1] > v:
            node = child
            v = nextLevel[1]
            toAdd += nextLevel[2] + 1
    return node,v,toAdd + iteration


def minValue(state,iteration):
    v = 9999999
    node = None
    toAdd = 0


    for child in state.getChildrens():
        nextLevel = minimax(child,"MAX",iteration + 1)
        if nextLevel[1] < v:
            node = child
            v = nextLevel[1]
            toAdd += nextLevel[2] + 1

    return node,v,toAdd + iteration


def minimax(state,currPlayer,iteration):
    currStateSum = sum(state.getName())
    
    if currStateSum == 1:
        if currPlayer == "MAX":
            return (state,-1,iteration + 1)
        else:
            return (state,1,iteration + 1)
    
    if currPlayer == "MAX":
        return maxValue(state,iteration + 1)

    if currPlayer == "MIN":
        return minValue(state,iteration + 1)
### MINIMAX ALGORITHM ENDS HERE ###



def inputReader(file_name):
    rawInput = open(file_name,"r").read()
    inputList = eval(rawInput)
    return inputList

def SolveGame(method_name, problem_file_name, player_type):
    input = inputReader(problem_file_name)
    rootNode = createGameTree(input)

    util = None
    if method_name == "Minimax":
        util = minimax(rootNode,player_type,0)
    
    else:
        ## Alpha Beta Pruning.
        util = pruneMinimax(rootNode,player_type,0,-99999,99999)

    result = []
    result.append(tuple(util[0].getName()))
    result.append(util[2])
    return result


if __name__ == "__main__":
    print(SolveGame("AlphaBeta","nim1.txt","MAX"))
