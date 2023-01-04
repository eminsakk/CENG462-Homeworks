import random
import copy
import numpy as np

def Qlearning(board,alpha,gamma,epsilon,QTable):
    #Implement Q learning algorithm.
    if random.random() <= epsilon:
        # Epsilon-Greedy Strategy.
        
        pass
    else:
        # Actual Q learning algorithm.
        # Find the best action.



        # Find the best action.
        # bestAction = None
        # bestActionValue = -1
        # for action in range(9):
        #     if board[action] == "-":
        #         if QTable[board][action] > bestActionValue:
        #             bestActionValue = QTable[board][action]
        #             bestAction = action
        # # Update the Q table.
        # QTable[board][bestAction] = QTable[board][bestAction] + alpha*(QTable[board][bestAction] + gamma*bestActionValue - QTable[board][bestAction])
        # # Update the board.
        # board = board[:bestAction] + "X" + board[bestAction+1:]
        



        pass    


def SARSA(board,alpha,gamma,epsilon,QTable):
    # SARSA algorithm.
    pass

def playerO(board,algoType,alpha,gamma,epsilon):
    Qlearning(board,alpha,gamma,epsilon) if algoType == "Q-learning" else SARSA(board,alpha,gamma,epsilon)

def playerX(board,algoType,alpha,gamma,epsilon):
    Qlearning(board,alpha,gamma,epsilon) if algoType == "Q-learning" else SARSA(board,alpha,gamma,epsilon)


# Win Condition Functions.

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

# Win Condition Functions Ends.

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


def createQLearningTable():
    # Create Q learning table for the game.
    





    pass

def startGame(board,algoTypeX,algoTypeO,alpha,gamma,epsilon,QTable):
    # Select the first player.
    playerToPlay = np.random.choice(["X","O"])


    # Start the game.
    while True:

        if playerToPlay == "X":
            playerX(board,algoTypeX,alpha,gamma,epsilon,QTable)

        if playerToPlay == "O":
            playerO(board,algoTypeO,alpha,gamma,epsilon,QTable)


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

    return QTable



SolveMDP("Q-learning","mdp1.txt",5)
