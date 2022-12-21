import copy
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

    def findNode(self,name):
        for item in self.nodes:
            if item.getName() == name:
                return item
        return None 

    def getVars(self):
        return self.nodes
    def getSize(self):
        return len(self.nodes)

    def enumerationInference(self,query):
        variables = query["variables"]
        evidences = query["evidences"]

        Qx = []
        for x_i in [True,False]:
            tmpQx = self.enumerateAll(x_i,evidences,self.nodes)
            Qx.append(tmpQx)


        return normalizeFindings(Qx)

    def enumerateAll(self,x_i,evidences,nodes):

        if len(nodes) == 0:
            return 1.0
        
        copyNodes = copy.copy(nodes)
        
        var = copyNodes[0]
        evidenceKeys = evidences.keys()


        if var in evidenceKeys:
            return self.calcProb(var,x_i,evidences) * self.enumerateAll(self,x_i,evidences,copyNodes[1:])
    
    def calcProb(self,var,x_i,evidences):
        prob = 0
        parents = var.getParents()
        if len(parents) == 0:
            ## No parents.
            entry = findTableEntry(self.table,var)
            p = tuple(entry[2])[0]
            prob = p if evidences[var.getName()] else 1 - p

        
        else:
            ## Have at least 1 parents.
            parentEntries = []
            
            for parent in parents:
                parentEntries.append(findTableEntry(self.table,parent))
            
            tmp = []

            for entry in parentEntries:
                for pair in entry[2].keys():
                    tmp.append(entry[2][str(pair)])

            


        return prob


def findTableEntry(table,var):
    for entry in table:
        if var.getName() == entry[0]:
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

    if method_name == "ENUMERATION":
        # Inference part.
        bayesianNet.enumerationInference(parsedQuery)

        pass

    elif method_name == "GIBBS":
        # Sampling part

        pass






if __name__ == "__main__":
    DoInference("ENUMERATION","query1.txt",0)
