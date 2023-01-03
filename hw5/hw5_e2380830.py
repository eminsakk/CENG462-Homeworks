import random
import copy





def input_tuple(file_name):
    lines = open(file_name,"r").readlines()

    alphaIdx = lines.index("[alpha]\n") + 1
    gammaIdx = lines.index("[gamma]\n") + 1
    epsilonIdx = lines.index("[epsilon]\n") + 1
    episodeIdx = lines.index("[episode]\n") + 1


    alphaVal = eval(lines[alphaIdx].replace('\n',''))
    gammaVal = eval(lines[gammaIdx].replace('\n',''))
    epsilonVal = eval(lines[epsilonIdx].replace('\n',''))
    episodeVal = eval(lines[episodeIdx].replace('\n',''))

    return alphaVal,gammaVal,epsilonVal,episodeVal



def SolveMDP(method_name,problem_file_name,random_seed):
    

    #(alpha,gamma,epsilon,episode)
    inputs = input_tuple(problem_file_name)
    
    

    

    pass
