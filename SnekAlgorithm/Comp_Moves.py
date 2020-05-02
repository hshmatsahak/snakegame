'''
Comp_moves class

Class with instance variables num_moves and top. 
num_moves- number of moves computer will play
top- move to be played first

This allows the API to accept a sequence of moves and stores it as a class
'''

class Comp_moves:
    # Constructor
    def __init__(self):
        self.num_moves = 0
        self.top = None
       
    # Add computer move to be executed last
    def push_move (axis, direction):
        move = Comp_move(axis, direction)
        if self.top is None:
            self.top = move
            self.num_moves +=1	
            return
        curr = self.top
        while curr.next_move != NULL:
            curr = curr.next_move
        curr.next_move = move
        self.num_moves += 1
    
    # Add computer move to be executed first
    def insert_move(self, axis, direction):
        move = Comp_move(axis, direction)
        if self.top is None:
            self.top = move
            self.num_moves += 1
            return
        move.next_move = self.top
        self.top = move
        self.num_moves += 1
'''
Comp_move class

Class with instance variables axis, direction, and next_move
axis- axis in which snake must travel(x,y)
direction- direction of travel (Up, Down, Left, Right)
next_move- the next move to be executed by the snake

This class stores information regarding a single move. It will be used to give the snake instructions on where to move next
'''
class Comp_move:
    def __init__(self, axis, direction):
        self.axis = axis
        self.direction = direction
        self.next_move = None
