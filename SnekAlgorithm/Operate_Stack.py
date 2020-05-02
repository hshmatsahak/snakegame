# import necessary files
from Stack_Moves import *
from Game_State import *
from Comp_Moves import *
from time import sleep
from snek import *

# getfirstn accepts a board and an integer n, and returns a random sequence of valid moves 
def getfirstn (board, n):
    '''
    getfirstn will be used to generate moves for the snake when no food is present. As there is no concern about optimizing score in this stage of the game, 
    the snake will obtain the first valid path of length n using a depth-first search algorithm
    '''
    count = 0
    stackofgamestates = StackMoves()
    gamestate = GameState(board)
    stackofgamestates.push(gamestate)
    while stackofgamestates.depth() <= n:
        gamestate = stackofgamestates.pop()
        if gamestate is None:
            break
        #gamestate.visited = True
        nextgamestate1 = gen_next_gamestate(1,1,gamestate, 0)
        nextgamestate2 = gen_next_gamestate(1,-1, gamestate, 0)
        nextgamestate3 = gen_next_gamestate(-1,1, gamestate, 0)
        nextgamestate4 = gen_next_gamestate(-1,-1, gamestate, 0)              

        stackofgamestates.push(nextgamestate1)
        stackofgamestates.push(nextgamestate2)
        stackofgamestates.push(nextgamestate3)
        stackofgamestates.push(nextgamestate4)
        
        #if nextgamestate1 is None and nextgamestate2 is None and nextgamestate3 is None and nextgamestate4 is None:
         #   stackofgamestates.pop()
        count+=1
    
    moves = Comp_moves()
    if gamestate is None:
        return moves
    
    tempstate = stackofgamestates.stack[-1]
    while tempstate != None and tempstate.prev != None:
        moves.insert_move(tempstate.axis, tempstate.direction)
        tempstate = tempstate.prev
    return moves     

#goforn accepts a pointer to a board(converted form c) and an integer n, and returns a sequence of computer moves of length n or less that lead to a MOOGLE
def goforn (board, n): 
    '''
    This function finds the first available path to a moogle using a heuristic DFS algorithm. 
    The stack stores all gamestates. In each iteration of the while loop, the most recently added state is explored, and neighbouring gamestates are added.
    If all immediate moves lead to a failing state, that gamestate is popped from the stack and the next gamestate at the top is explored.
    '''
    stackofgamestates = StackMoves()
    gamestate = GameState(board)
    stackofgamestates.push_all(gamestate)
    count = 0;
 
    while(True):
        if count > 25000:
            break;
        gamestate = stackofgamestates.pop()
       
        if gamestate is None:
             break
        if gamestate.end_stage == 1:
            sample = getfirstn (gamestate.myboard, 10)
            if sample.num_moves == 10:
                break
            else:
                continue
            
        nextgamestate1 = gen_next_gamestate(1,1,gamestate, 1)
        if ((nextgamestate1 is not None and distance(nextgamestate1, board) <n-stackofgamestates.depthfrom(gamestate)) or (nextgamestate1 is not None and nextgamestate1.end_stage == 1)):
            stackofgamestates.push_all(nextgamestate1) 
        
        nextgamestate2 = gen_next_gamestate(1,-1, gamestate,1)
        if ((nextgamestate2 is not None and distance(nextgamestate2, board) < (n-stackofgamestates.depthfrom(gamestate))) or (nextgamestate2 is not None and nextgamestate2.end_stage == 1)):
            stackofgamestates.push_all(nextgamestate2)
        
        nextgamestate3 = gen_next_gamestate(-1,1, gamestate,1)        
        if ((nextgamestate3 is not None and distance(nextgamestate3, board) <( n-stackofgamestates.depthfrom(gamestate))) or (nextgamestate3 is not None and nextgamestate3.end_stage == 1)):
            stackofgamestates.push_all(nextgamestate3)
        
        nextgamestate4 = gen_next_gamestate(-1,-1,gamestate,1)
        if ((nextgamestate4 is not None and distance(nextgamestate4, board) <(n-stackofgamestates.depthfrom(gamestate))) or (nextgamestate4 is not None and nextgamestate4.end_stage == 1)):
            stackofgamestates.push_all(nextgamestate4)

        count+=1

    moves = Comp_moves()
    while gamestate != None and gamestate.prev != None:
        moves.insert_move(gamestate.axis, gamestate.direction)
        gamestate = gamestate.prev   
    return moves

# distance accepts a gamestate and a board pointer, and returns distance from snek head in "nextgamestate" to moogle position as it appears in board
def distance(gamestate, board):  
    '''
    This function is useful as it sets a condition for adding game states to our stack.
    We will only add game states to our stack if it is mathematically possible to reach the food from that position, as determined by the minimum ditance        calculated below
    '''
    (moogle_x, moogle_y) = find_moogle(board)
    (curr_x, curr_y) = (gamestate.myboard[0].snek[0].head[0].coord[x],  gamestate.myboard[0].snek[0].head[0].coord[y])
    return abs(moogle_x-curr_x) + abs(moogle_y-curr_y)

# find_moogle accepts a board pointer and returns position of moogle
def find_moogle (board):
    '''
    find_moogle is used in distance() function to determine the moogle position before calculating distance to it
    '''
    for i in range (0, BOARD_SIZE):
        for j in range (0, BOARD_SIZE):
            if board[0].cell_value[i][j] > 1:
                return (j, i)
    return (0,0)
