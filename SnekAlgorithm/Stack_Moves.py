'''
Stack Class

instance variables: stack
stack- implemented as a python list, to take advantage of append(), len() and pop() methods
'''
class StackMoves:        
    #Constructor- initialize to empty list
    def __init__(self):
        self.stack = []
    
    # obtain size of stack using built-in len method
    def size(self):
        return len(self.stack)

    # return True if stack is empty, otherwise, return Flase
    def is_empty(self):
        if self.size() == 0:
            return True
        return False
    
    # push elemment to stack using python's built-in append method, add only if snake in gamestate is yet to reach moogle
    def push(self, element):
        if element is not None and element.end_stage == -1: 
            self.stack.append(element)

    # push element to stack using python's built-in append method, add element so long as it's not None
    def push_all (self, element):
        if element is not None:
            self.stack.append(element)
	
    # uses pyhton's built-in pop method to remove and return gamestate at the top of the stack 
    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    # return most recent element pushed to the stack, under the condition that it has not been visited before  
    def top(self):
        '''
        This function is used when determining which gamestate to explore next, found in getfirstn() method of operate_stack file
        If no unvisited element is found, returns None
        '''
        if self.is_empty():
            return None
        count = self.size()-1
        curr = self.stack[count]
        while count>0 and curr.visited:
            count-=1
            curr = self.stack[count]
        if curr.visited:
            return None
        return curr
    
    # return distance from starting gamestate to top of stack, where distance is number of moves required to reach gamestate from the starting game board.
    def depth(self):
        if self.is_empty():
            return 0
        element = self.stack[-1]
        count = 1
        while element.prev is not None:
            count+=1
            element = element.prev
        return count

    # return depth from a passed-in gamestate to starting game board, where depth is the number of moves that were required to reach the gamestate               # from the starting position
    def depthfrom(self, element):
        count = 0	
        temp = element
        while temp.prev is not None:
            count+=1
            temp = temp.prev
        return count

























 
