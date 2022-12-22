import copy
import random
class BayesNode:
    def __init__(self,name):
        self.nodeName = name
        self.edges = []
        self.parents = []
        
    def createEdges(self,paths,nodes):
        for path in paths:
            parents = path[0]
            if self.nodeName in parents:
                node = findByName(path[1], nodes)
                self.edges.append(node)
                node.parents = parents
            
    def getName(self):
        return self.nodeName

    def getParents(self):
        return self.parents

    def getEdges(self):
        return self.edges

class BayesNet:
    def __init__(self,names,paths,table):
        self.nodes = []
        self.table = None
        for name in names:
            tmp = BayesNode(name)
            self.nodes.append(tmp)
        
        for node in self.nodes:
            node.createEdges(paths,self.nodes)
        self.table = table

        self.nodes = self.topoSort()

    def topoSort(self):
        visited = set()
        stack = []

        for node in self.nodes:
            if node.getName() not in visited:
                self.topoSortHelper(node,visited,stack)
        
        return stack

    def topoSortHelper(self,currNode,visitedSet,stack):
        visitedSet.add(currNode.getName())

        for edgeNode in currNode.getEdges():
            if edgeNode.getName() not in visitedSet:
                self.topoSortHelper(edgeNode,visitedSet,stack)

        stack.insert(0,currNode)


    def getNodeNames(self):

        tmp = []
        for node in self.nodes:
            tmp.append(node.getName())
        return tmp

    def findNode(self,name):
        for item in self.nodes:
            if item.getName() == name:
                return item
        return None 

    def getVars(self):
        return self.nodes
    def getSize(self):
        return len(self.nodes)

    def getNodeByName(self,name):

        for node in self.nodes:
            if name == node.getName():
                return node

        return None
    
    # ENUMERATION ASK FUNCTIONS.
    def enumerationAsk(self,queryVarStr,evidences):
        
        distributions = []
        possibleStates = [True,False]

        for possibleState in possibleStates:
            copyEvidence = copy.deepcopy(evidences)
            copyEvidence[queryVarStr] = possibleState

            nodeNames = self.getNodeNames()

            
            dist = self.enumerateAll(nodeNames,copyEvidence)
            distributions.append(dist)    


        return normalizeFindings(distributions)
    
    
    def enumerateAll(self,vars,evidences):
        
        if len(vars) == 0:
            return 1.0
        
        #Note V is string.
        V = vars[0]
        
        # Get evidence keys.
        eKeys = evidences.keys()


        if V in eKeys:
            # v is boolean type.
            v = evidences[V]
            retVal = self.calcProb(V,evidences) * self.enumerateAll(vars[1:],evidences)
        
        else:
            #Not in evidence first extend the evidence 
            # dictioanry.

            copyEvidence = copy.deepcopy(evidences)
            #e_v extended with V which is v
            
            possibilities = [True,False]

            retVal = 0
            for possible in possibilities:
                copyEvidence[V] = possible
                retVal += (self.calcProb(V,copyEvidence)) * self.enumerateAll(vars[1:],copyEvidence)
                
        return retVal


    

    def calcProb(self,var,evidences):
        varNode = self.getNodeByName(var)


        # Get parents of the varNode.
        parentNodes = varNode.getParents()

  
        # No parents case.
        if len(parentNodes) == 0:
            entry = self.findTableEntry(var)
            retVal = tuple(entry[2])[0] if evidences[var] else 1 - evidences[var]

        # At least 1 parent case.
        else:
            # We need to have value of the parent nodes. So,
            evidenceOfParents = []
            for parent in parentNodes:
                evidenceOfParents.append(evidences[parent])
            
            # We need to convert this list to tuple, because in the table
            # We are given it as a key of tuple.

            if len(evidenceOfParents) == 1:
                evidenceOfParents = evidenceOfParents[0]
            else:
                evidenceOfParents = tuple(evidenceOfParents)


            # Then we need to look up table 
            # given key.

            entry = self.findTableEntry(var)
            retVal = entry[2][evidenceOfParents] if evidences[var] else 1 - entry[2][evidenceOfParents]
        
        return retVal

    # ENUMERATION ASK FUNCTIONS ENDS.


    
    # GIBBS ASK FUNCTIONS.

    def findNonEvidences(self,evidences):
        

        nodeSet = []
        for node in self.nodes:
            nodeSet.append(node.getName())
        
        Z = []
        eKeys = evidences.keys()

        eKeys = set(eKeys)

        for name in nodeSet:
            if name not in eKeys:
                Z.append(name)


        return Z

    def initX(self,x,Z):
        random.seed(10)

        for notInVar in Z:
            x[notInVar] = random.choice([True,False])

        
        return x



    def initN(self):
        N = dict()
        N[True] = 0
        N[False] = 0
        return N

    def markovBlanket(self):

        pass

    def gibbsAsk(self,var,evidences,iterations):

        

        
        #Local Variable initialization.
        Z = self.findNonEvidences(evidences)
        x = copy.deepcopy(evidences)
        N = self.initN() # Must be a vector but we are tested with one variable so it is 1d.
        x = self.initX(x,Z) # Add non evidence variables with random vars.


        for i in range(0,iterations):
            for Z_i in Z:
                x[Z_i] = self.markovBlanket()
                
                key = x[var]
                N[key] = N[key] + 1
            
            

        vals = list(N.values())
        return normalizeFindings(vals)



        







    # GIBBS ASK FUNCTIONS ENDS.




    def findTableEntry(self,name):
        for entry in self.table:
            if entry[0] == name:
                return entry
        return None


def findByName(target,container):
    for item in container:
        if item.getName() == target:
            return item
    return None

def parseNodeNames(start,end,lines):
    nodes = []
    for i in range(start,end - 1):
        name = lines[i].replace('\n','')
        nodes.append(name)

    return nodes   

def parsePaths(start,end,lines):
    paths = []
    for i in range(start,end - 1):
        path = lines[i].replace('\n','')
        path = eval(path)
        paths.append(path)
    return paths

def parseTable(start,end,lines):
    table = []
    for i in range(start,end - 1):
        entry = lines[i].replace('\n','')
        entry = eval(entry)
        table.append(entry)
    return table

def parser(problem_file):
    lines = open(problem_file,"r").readlines()
    
    nodeStartIdx = lines.index("[BayesNetNodes]\n") + 1
    pathStartIdx = lines.index("[Paths]\n") + 1
    tableStartIdx = lines.index("[ProbabilityTable]\n") + 1
    queryIdx = lines.index("[Query]\n") + 1

    nodeNames = parseNodeNames(nodeStartIdx,pathStartIdx,lines)
    paths = parsePaths(pathStartIdx,tableStartIdx,lines)
    table = parseTable(tableStartIdx,queryIdx,lines)

    query = eval(lines[queryIdx])
    bayesianNet = BayesNet(nodeNames,paths,table)

    return bayesianNet,query

def queryParser(query):
    variableNames = [x for x in query if type(x) is not dict]
    evidences = None
    for item in query:
        if type(item) == dict:
            evidences = item
    return {"variables": variableNames, "evidences": evidences}



##### ENUMERATION FUNCTIONS #####


def normalizeFindings(l):
    z = sum(l)
    return tuple(x * 1/z for x in l)

##### ENUMERATION FUNCTIONS ENDS. #####


def DoInference(method_name,problem_file,iteration):
    parsed = parser(problem_file)

    bayesianNet = parsed[0]
    query = parsed[1]
    parsedQuery = queryParser(query)

    var = parsedQuery["variables"]
    evidences = parsedQuery["evidences"]

    if method_name == "ENUMERATION":
        # Inference part.
        ans = bayesianNet.enumerationAsk(var[0],evidences)
        return round(ans[0],3),round(ans[1],3)

    elif method_name == "GIBBS":
        # Sampling part

        pass






if __name__ == "__main__":
    ans = DoInference("ENUMERATION","query2.txt",0)
    print(ans)
