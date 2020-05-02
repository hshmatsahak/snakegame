# import snek file
from snek import *
import random
# define MACROS for game being at a finished or unfinished state
END = 1
NOT_DONE = -1

'''
GameState class

instance variables: myboard, end_stage, axis, direction, visited, prev
myboard- pointer to board containing all relevant board information
end_stage- 1 if game at finished position(successfully ate MOOGLE), -1 if not done(yet to eat MOOGLE)
axis- specify motion as either horizontal or vertical direction to reach gamestate
direction- 1 for down, right; -1 for up, left
visited- required in stack implementation, to determine if gamestate has been explored or not
prev- required in stack implementation, stores previous gamestate (to get to current state)

This class stores information on a potential game position. When initialized, it stores a copy of the playing board, and in our stack implementation, possible gamestates will be stored as stack elements to determine a path for the snake to the food 
'''
class GameState:
    #Constructor
    def __init__(self, board):
        self.myboard = copy_board(board)
        self.end_stage = -1
        self.axis = AXIS_INIT
        self.direction = DIR_INIT
        #self.visited = False
        self.prev = None

# copy_board returns a pointer to a GameBoard struct(converted from c)
def copy_board(board):
    '''
    accepts a pointer to a board and returns a pointer to a copy of the board 
    when initializing gamestate, we want to create a copy pointer to the board to use for computing future moves
    '''
    tempboard = init_board()
    tempboard[0].cell_value = board[0].cell_value
    tempboard[0].occupancy = board[0].occupancy
    tempboard[0].snek = copy_snake(board[0].snek)
    tempboard[0].CURR_FRAME = board[0].CURR_FRAME
    tempboard[0].SCORE = board[0].SCORE
    tempboard[0].MOOGLE_FLAG = board[0].MOOGLE_FLAG
    tempboard[0].MOOGLES_EATEN = board[0].MOOGLES_EATEN
    return tempboard

#copy_snake returns a pointer to a snek struct(converted from c)
def copy_snake(snake):
    '''
    When copying gameboard, we need to copy snake pointer as a separate unit
    snake is not an immutable type, so we will copy snake body and return pointer to achieve effects of deepcopy
    '''
    copy = init_snek(snake[0].head[0].coord[x], snake[0].head[0].coord[y])
    snekblock = snake[0].head[0].nextblock
    while(copy[0].length < snake[0].length):
        if copy[0].length == 1:
            copy[0].tail[0].coord[x] = snekblock[0].coord[x]
            copy[0].tail[0].coord[y] = snekblock[0].coord[y]
        else:
            copy[0].tail[0].nextblock = init_block(snekblock[0].coord[x], snekblock[0].coord[y])
            copy[0].tail = copy[0].tail[0].nextblock
        copy[0].length+=1
        snekblock = snekblock[0].nextblock
    return copy

# gen_next_gamestate accepts a gamestate, an axis and a direction, and returns a new game state that is the result of the snake in the
# curent gamestate moving in the specified axis and direction
def gen_next_gamestate (axis, direction, curr_state, moogle_val):
    '''
    This function is used to determine what to add into our game stack in each iteration of the while loop found in operate_stack()
    We will use this method to determine whether moving to the right, left, up, or down is legal and include or ignore them accordingly
    when updating our stack
    '''
    if (is_failure_state(axis, direction, curr_state.myboard)):
        return None
    #random.seed()
    next_state = GameState(curr_state.myboard)
    next_state.axis = axis
    next_state.direction = direction
    next_state.prev = curr_state

    advance_frame(axis, direction, next_state.myboard)
    if moogle_val == 0 and next_state.myboard[0].MOOGLE_FLAG == 1:
        next_state.myboard[0].MOOGLE_FLAG = 0
        for i in range (BOARD_SIZE):
                for j in range (BOARD_SIZE):
                        next_state.myboard[0].cell_value[i][j] = 0
        
    if next_state.myboard[0].SCORE - curr_state.myboard[0].SCORE > 1:
        next_state.end_stage = 1
    return next_state
