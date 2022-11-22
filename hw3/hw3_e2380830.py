




def inputReader(file_name):
    rawInput = open(file_name,"r").read()
    inputList = eval(rawInput)
    return inputList

def SolveGame(method_name, problem_file_name, player_type):
    input = inputReader(problem_file_name)


if __name__ == "__main__":
    SolveGame("Minimax","nim1.txt","MAX")
