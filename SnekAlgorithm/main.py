'''
Hshmat Sahak
April 5, 2020
ESC190 Project Submission
Snek Game
'''

#import necessary files
from snek import *
import time
from Comp_Moves import *
from Game_State import *
from Operate_Stack import *
from Stack_Moves import *
import random

# play_out accepts an object of class comp_moves, a board pointer and game condition (eat food or not), and commands the snake to move accordingly
def play_out (moves, board, moogle_val):
	'''
	this method allows the program to control the snake by continuously advancing the gameboard frame according to the parameter "moves", and displaying         the new position to screen
	'''
	#random.seed()
	move = moves.top
	while (move is not None and board[0].MOOGLE_FLAG == moogle_val): 
		advance_frame(move.axis, move.direction, board)
		show_board(board)	
		move = move.next_move

#*******************************************ALGORITHM************************************************
def run_dfs():
	'''
	Main function.
	'''
	start_time = time.time()
	#initialize board
	board = init_board()
	# cycle through loop as long as game is not finished
	while True:
		# while no food present
		while board[0].MOOGLE_FLAG != 1:
			#obtain any sequence of 50 moves and play it out
		#sleep(1)
			the_moves = getfirstn (board, 25)
			if the_moves.num_moves == 0:
				show_board(board)
				score = board[0].SCORE
				moogles_eaten = board[0].MOOGLES_EATEN
				end_game(board)
				#print("heooo")
				#sleep(3)
				return (BOARD_SIZE, score, moogles_eaten, time.time() - start_time) 
			play_out(the_moves, board, 0)	
		#sleep(1)
		if board[0].MOOGLE_FLAG == 1: #once food appears
			#find (any) path to food
			#print("calculating")
			#sleep(2)
			the_moves = goforn (board, TIME_OUT)
			if the_moves.num_moves == 0: #if path not found, end game
				show_board(board)
				score = board[0].SCORE
				moogles_eaten = board[0].MOOGLES_EATEN
				end_game(board)
				#sleep(0.5)
				break # exit out of while loop	
			play_out (the_moves, board, 1) # travel to food
	end_time = time.time()
	return (BOARD_SIZE, score, moogles_eaten, end_time - start_time)
		
#***************************************************MAIN**********************************************
if __name__ == "__main__":
    sleeep()
    trials = int(input("Enter number of trials: "))
    file_name = 'boardsize'
    board = int(input("Enter board size: "))
    file_name = file_name + str(board) + "_output.csv"
    with open (file_name, "a") as f:
        for i in range (trials):
            (boardsize, score, moogles, runtime) = run_dfs()
            #sleep(1)
            f.write(str(boardsize) + "," + str(score) + "," + str(moogles) + ", " + str(runtime) + "\n")
