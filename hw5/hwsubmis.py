import random
import copy
# NUMPY IMPORT ETMEYİ UNUTMA !!!!!!!!!!!!!!!!




# Hi hocam, I have tried to do my best to implement the algorithms for 5-6 days.
# I have implemented Q-learning and SARSA algorithms.
# However there are some problems with my code.
# I have tried to qtable as action:board dictionary as it is in the example output file.
# However  psuedocode is implemented the q table as board:action dictionary,
# Due to final exam week I could not implement it as it is in the psuedocode, my time is not enough to change it now.
# Sorry for the inconvenience and thank you for your understanding.



#Some issues are I observed:
# 1) Some values are not in the interval (-1,1) as it is in the example output file. I think this is because of 
#    the way I implemented the Q table. I have implemented it as action:board dictionary. So I may have some mistakes in the way 
#    I update the Q table. I am not sure about this.

# 2) When q-learning @reward local variable is find with the next board, the values that are obtained are not in the interval (-1,1).
#    When I use board instead of next_board, the values are in the interval (-1,1). I am not sure about this.




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
        # Finds the best action.
        
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
        
    reward = get_reward(next_board,player)
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
    if winCondition(board,"X" if player == "O" else "O"):
        return -1
    
    if "-" not in board:
        return 0
    
    return 0
    
#Player X and O functions.

def playerO(board,algoType,alpha,gamma,epsilon,QTable):
    return Qlearning(board,alpha,gamma,epsilon,QTable,"O") if algoType == "Q-learning" else SARSA(board,alpha,gamma,epsilon,QTable,"O")
def playerX(board,algoType,alpha,gamma,epsilon,QTable):
    return Qlearning(board,alpha,gamma,epsilon,QTable,"X") if algoType == "Q-learning" else SARSA(board,alpha,gamma,epsilon,QTable,"X")

# Player X and O functions ends.


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

# Working Permutations of the board states function.

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
    
    
    # To eliminate invalid boards.
    if abs(xCount - oCount) > 1:
        continue
    
    if winCondition(board_string,"X") or winCondition(board_string,"O"):
        continue
    
    board_strings.append(board_string)

  return board_strings


#QTable Creator.    

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

# QTAble Creator Ends.     

# Game Loop.

def startGame(board,algoTypeX,algoTypeO,alpha,gamma,epsilon,QTable):
    # Select the first player.
    #playerToPlay = np.random.choice(["X","O"])
    
    
    playerToPlay = "O"
    # Start the game.
    while True:

        if playerToPlay == "X":
            board = playerX(board,algoTypeX,alpha,gamma,epsilon,QTable)

        if playerToPlay == "O":
            board = playerO(board,algoTypeO,alpha,gamma,epsilon,QTable)


        # Check the status of the game.
        if winCondition(board,"X"):
            break
        elif winCondition(board,"O"):
            break
        elif "-" not in board:
            break
        # Change the player.
        playerToPlay = "X" if playerToPlay == "O" else "O"

# Game Loop Ends.  


# Main Function.

def SolveMDP(method_name,problem_file_name,random_seed):
    
    random.seed(random_seed)
    
    
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
    

    # Train the agent.
    while currEpisode < episode:
        # Start the game.
        
        startGame(board,xAlgorithm,oAlgorithm,alpha,gamma,epsilon,QTable)

        # Reset the board.
        board = "---------"
        # Increment the episode.
        currEpisode += 1
    
    
    
    # Create the output dictionary.
    ans = {}
    
    for key1,dict in QTable.items():
        ans[key1] = []
        for key2,value in dict.items():        
            tup = (key2,value)
            ans[key1].append(tup)
        
    
    return ans

# Main Function Ends.

SolveMDP("Q-learning","mdp1.txt",37)
