
# coding: utf-8

# In[125]:

from search import *            # The Python module for search problems
from copy import deepcopy
import sys


# In[170]:

class Puzzle8Problem(Problem):
    def __init__(self, initialState, goal):
        self.initial = initialState
        self.goal = goal
        
        if (self._validate_state(initialState) != True):
            raise ValueError('Given state doesn\'t appear to be valid!!!')
        
    def _validate_state(self, state):
		# TODO: Implement and prevent unsolveable puzzles!
        return True
        
    "Generates all possible combinations from the current position"
    def successor(self, state):
        #print "Finding successors for state: "
        #printPuzzle(state)
        #print ""
        
        index = self._get_empty_tile_position(state)
        
        row = index[0]
        col = index[1]
                
        
        totalRows = len(state)
        "I'll assume that matrix is same-dimensional ..."
        totalCols = len(state[0])
        
        #print "Tile position: (%s, %s), Matrix dimensions: (%s, %s)" % (row,col, totalRows, totalCols)

        "Generally, empty tile can move in maximum of 4 directions."
        "I'll generate all of them and filter out the invalid ones"
        
        possibleCombinations = []
        
        "### Move to the left: "
        "Tile can be moved to the left if it isn't on the first column"
        if col > 0:
            new_list = deepcopy(state)
            
            switchIndex = col - 1;
                        
            tileForSwitch = new_list[row][switchIndex]
            
            new_list[row][switchIndex] = 0
            new_list[row][col] = tileForSwitch
            
            possibleCombinations.append(('L', new_list))
        
        "### Move to the right:"
        "Tile can be moved to right if it isn't in the last column"
        if col < (totalCols - 1):
            new_list = deepcopy(state)
            
            switchIndex = col + 1;
                        
            tileForSwitch = new_list[row][switchIndex]
            
            new_list[row][switchIndex] = 0
            new_list[row][col] = tileForSwitch
            
            possibleCombinations.append(('R', new_list))
            
        "### Move up:"
        if row != 0:
            new_list = deepcopy(state)
            
            switchIndex = row - 1;
            
            tileForSwitch = new_list[switchIndex][col]
            
            new_list[switchIndex][col] = 0
            new_list[row][col] = tileForSwitch
            
            possibleCombinations.append(('U', new_list))
            
        "### Move down:"
        if row < totalRows - 1:
            new_list = deepcopy(state)
            
            switchIndex = row + 1;
            
            tileForSwitch = new_list[switchIndex][col]
            
            new_list[switchIndex][col] = 0
            new_list[row][col] = tileForSwitch
            
            possibleCombinations.append(('D', new_list))
        
        
        return possibleCombinations
        
        
        
        
    def _get_empty_tile_position(self, state):
        rowNum = 0;
        
        for row in state:            
            if 0 in row:
                return (rowNum, row.index(0))
            
            rowNum += 1
            
        return rowNum

def printPuzzle(state):
    for row in state:
        for col in row:
            print "%s " % (col if col > 0 else " "),
        print ""

# Expand the state into a String, so that we can use it as a key for a dictionary :)
def expand_state(state):
	key = ""
	for row in state:
		for col in row:
			key += str(col)
	
	return key
	


# In[174]:

initialState = [ [ 1, 0, 2 ], [ 3, 4, 5 ], [ 6, 7, 8 ] ]
goalState = [ [ 0, 1, 2 ], [ 3, 4, 5 ], [ 6, 7, 8]]

initialStateKey = expand_state(initialState) 

dictionary = Dict()
dictionary[initialStateKey] = initialState


p = Puzzle8Problem(initialState, goalState)

p.successor(initialState)

solution = breadth_first_tree_search(p)

#solution = tree_search(p)

# In[178]:

path = solution.path()
path.reverse()

print path
