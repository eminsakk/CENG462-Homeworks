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

def inputReader(file_name):
    rawInput = open(file_name,"r").read()
    inputList = eval(rawInput)
    return inputList

def SolveGame(method_name, problem_file_name, player_type):
    input = inputReader(problem_file_name)
    rootNode = createGameTree(input)
    print("GAME TREE DEBUG POINT!")

if __name__ == "__main__":
    SolveGame("Minimax","nim1.txt","MAX")
