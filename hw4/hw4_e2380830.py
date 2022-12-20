class BayesNode:
    def __init__(self,name):
        self.nodeName = name
        self.edges = []
        
    def createEdges(self,paths,nodes):
        for path in paths:
            parents = path[0]
            if self.nodeName in parents:
                node = findByName(path[1], nodes)
                self.edges.append(node)
    
    def getName(self):
        return self.nodeName


class BayesNet:
    def __init__(self,names,paths):
        self.nodes = []
        for name in names:
            tmp = BayesNode(name)
            self.nodes.append(tmp)
        
        for node in self.nodes:
            node.createEdges(paths,self.nodes)
        

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
    print(table[0])
    print(table[0][1])
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


    bayesianNet = BayesNet(nodeNames,paths)

    return bayesianNet,table



def DoInference(method_name,problem_file,iteration):
    parsed = parser(problem_file)

    bayesianNet = parsed[0]
    table = parsed[1]
    pass




if __name__ == "__main__":
    DoInference("ENUMERATION","query1.txt",0)
