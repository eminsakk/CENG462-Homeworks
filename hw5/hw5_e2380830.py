import random
import copy


def Qlearning(board,alpha,gamma,epsilon,QTable,player):
    #Implement Q learning algorithm.
    if random.random() <= epsilon:
        # Epsilon-Greedy Strategy.
        while True:
            random_number = random.randint(0, 8)
            if board[random_number] == "-":
                next_board = board[:random_number] + player + board[random_number+1:]
                next_action = (random_number // 3,random_number % 3)
                break
        
    else:
        # Actual Q learning algorithm.
        # Find the best action.
        
        best_action = None
        best_action_value = -1
        
        for i in range(3):
            for j in range(3):
                action = (i,j)
                if board[i * 3 + j] == "-" and QTable[action][board] > best_action_value:
                        best_action_value = QTable[action][board]
                        best_action = action
        next_board = board[:best_action[0] * 3 + best_action[1]] + player + board[best_action[0] * 3 + best_action[1] + 1:]
        next_action = best_action
        
    reward = get_reward(board,player)
    
    QTable[next_action][board] = QTable[next_action][board] + alpha*(reward + gamma*max(QTable[next_action].values()) - QTable[next_action][board])
    
    return next_board


def SARSA(board,alpha,gamma,epsilon,QTable,player):
    # SARSA algorithm.
    
    if random.random() <= epsilon:
        # Epsilon-Greedy Strategy.
        while True:
            random_number = random.randint(0, 8)
            if board[random_number] == "-":
                next_board = board[:random_number] + player + board[random_number+1:]
                next_action = (random_number // 3,random_number % 3)
                break
    else:
        max_q = -float("inf")

        for i in range(3):
            for j in range(3):
                action = (i,j)
                if board[i * 3 + j] == "-":
                    if QTable[action][board] > max_q:
                        max_q = QTable[action][board]
                        best_action = action      
        
        next_board = board[:best_action[0] * 3 + best_action[1]] + player + board[best_action[0] * 3 + best_action[1] + 1:]                
        next_action = best_action
        
    reward = get_reward(board,player)
    next_reward = get_reward(next_board,player)
        
    QTable[next_action][board] = QTable[next_action][board] + alpha*(reward + gamma*next_reward - QTable[next_action][board])
        
        
    return next_board

def get_reward(board,player):
    
    if winCondition(board,player):
        return 1
    
    if "-" not in board:
        return 0
    
    return 0
    

def playerO(board,algoType,alpha,gamma,epsilon,QTable):
    return Qlearning(board,alpha,gamma,epsilon,QTable,"O") if algoType == "Q-learning" else SARSA(board,alpha,gamma,epsilon,QTable,"O")

def playerX(board,algoType,alpha,gamma,epsilon,QTable):
    return Qlearning(board,alpha,gamma,epsilon,QTable,"X") if algoType == "Q-learning" else SARSA(board,alpha,gamma,epsilon,QTable,"X")


# Win Condition Checkers.

def checkRows(board,player):
    # Check rows for win condition.
    if board[0:3] == player*3 or board[3:6] == player*3 or board[6:9] == player*3:
        return True
    return False
def checkCols(board,player):
    # Check columns for win condition.
    if board[0] + board[3] + board[6] == player*3:
        return True
    elif board[1] + board[4] + board[7] == player*3:
        return True
    elif board[2] + board[5] + board[8] == player*3:
        return True
    return False
def checkDiagonals(board,player):
    # Check diagonals for win condition.
    if board[0] + board[4] + board[8] == player*3:
        return True
    elif board[2] + board[4] + board[6] == player*3:
        return True
    return False
def winCondition(board,player):
    # Check win condition for X and O.
    return checkRows(board,player) or checkCols(board,player) or checkDiagonals(board,player)

# Win Condition checkers Ends.




# Input file parser.

def input_tuple(file_name):
    lines = open(file_name,"r").readlines()

    alphaIdx = lines.index("[alpha]\n") + 1
    gammaIdx = lines.index("[gamma]\n") + 1
    epsilonIdx = lines.index("[epsilon]\n") + 1
    episodeIdx = lines.index("[episode count]\n") + 1


    alphaVal = eval(lines[alphaIdx].replace('\n',''))
    gammaVal = eval(lines[gammaIdx].replace('\n',''))
    epsilonVal = eval(lines[epsilonIdx].replace('\n',''))
    episodeVal = eval(lines[episodeIdx].replace('\n',''))

    return alphaVal,gammaVal,epsilonVal,episodeVal

# Input file parser ends.


# Permutations of the board states function.

def createBoardStates():
    init = "---------"
    boardStates = [init]
    for i in range(9):
        for board in boardStates:
            if board[i] == "-":

                tmpBoard1 = board[:i] + "X" + board[i+1:]
                tmpBoard2 = board[:i] + "O" + board[i+1:]
                tmpBoard3 = board[:i] + "-" + board[i+1:]
                
                

                xCount1 = tmpBoard1.count("X")
                oCount1 = tmpBoard1.count("O")
                
                xCount2 = tmpBoard2.count("X")
                oCount2 = tmpBoard2.count("O")
                
                
                if not winCondition(tmpBoard1,"X") and abs(xCount1 - oCount1) <= 1:
                    boardStates.append(tmpBoard1)
                
                if not winCondition(tmpBoard2,"O") and abs(xCount2 - oCount2) <= 1: 
                    boardStates.append(tmpBoard2)
                
                              
                    
    return boardStates


def createPermutations():
    board = "---------"
    # Create all possible permutations of the board.
    permutations = [board]
    for i in range(9):
        for board in permutations:
            if board[i] == "-":
                
                
                permutations.append(board[:i] + "X" + board[i+1:])
                permutations.append(board[:i] + "O" + board[i+1:])
                
                
    return permutations 
    

def createQLearningTable():
    QTable = {}

    states = generate_boards()

    for i in range(3):
        for j in range(3):
            action = (i,j)
            idx = i * 3 + j

            actionPerState = {}
            filtered = list(filter(lambda x: x[idx] == "-", states))
            
            for state in filtered:
                actionPerState[state] = 0

            QTable[action] = actionPerState


    return QTable

            

def generate_boards():
  # Generate all possible boards
  boards = []
  for i in range(3**9):
    board = []
    for j in range(9):
      board.append(i // 3**j % 3)
    boards.append(board)

  # Convert boards to strings
  board_strings = []
  for board in boards:
    board_string = ''
    for cell in board:
      if cell == 0:
        board_string += '-'
      elif cell == 1:
        board_string += 'X'
      elif cell == 2:
        board_string += 'O'
    
    xCount = board_string.count("X")
    oCount = board_string.count("O")
    
    if abs(xCount - oCount) > 1:
        continue
    board_strings.append(board_string)

  return board_strings
    


    

def startGame(board,algoTypeX,algoTypeO,alpha,gamma,epsilon,QTable):
    # Select the first player.
    #playerToPlay = np.random.choice(["X","O"])

    playerToPlay = "X"
    # Start the game.
    while True:

        if playerToPlay == "X":
            board = playerX(board,algoTypeX,alpha,gamma,epsilon,QTable)

        if playerToPlay == "O":
            board = playerO(board,algoTypeO,alpha,gamma,epsilon,QTable)


        # Check the status of the game.
        if winCondition(board,"X"):
            # X wins. Utility = 1.
            
            

            print("X wins!")
            break
        elif winCondition(board,"O"):
            # O wins. Utility = -1.
            
            


            print("O wins!")
            break
        elif "-" not in board:
            # Draw. Utility = 0.

            print("Draw!")
            break
        # Change the player.
        playerToPlay = "X" if playerToPlay == "O" else "O"

    

    



    pass
    
    

def SolveMDP(method_name,problem_file_name,random_seed):
    
    random.seed(random_seed)
    #playerToPlay = np.random.choice(["X","O"])
    #(alpha,gamma,epsilon,episode)
    inputs = input_tuple(problem_file_name)
    # Tuple unrolling.
    alpha,gamma,epsilon,episode = inputs

    # Initial state of the board.
    board = "---------"
    # Adjust Algorithms of the X and O players.
    xAlgorithm,oAlgorithm = ("Q-learning","SARSA") if method_name == "Q-learning" else ("SARSA","Q-learning")



    # Create Q learning table.
    QTable = createQLearningTable()

    # Reinforcement learning iterator.
    currEpisode = 0
    

    # Train the Q learning table.
    while currEpisode < episode:
        # Start the game.
        
        startGame(board,xAlgorithm,oAlgorithm,alpha,gamma,epsilon,QTable)

        # Reset the board.
        board = "---------"
        # Increment the episode.
        currEpisode += 1
    
    ans = {}
    
    
    
    for key1,dict in QTable.items():
        ans[key1] = []
        for key2,value in dict.items():
            if key1 == (0,0) and value != 0:
                print(key1,value)
                
                
            tup = (key2,value)
            ans[key1].append(tup)
        
    
    return ans

SolveMDP("SARSA","mdp1.txt",37)

