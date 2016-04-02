
# coding: utf-8

# In[125]:

from search import *            # The Python module for search problems
from copy import deepcopy
import sys
import math

# In[170]:

class Puzzle8Problem(Problem):
    def __init__(self, initialState, goal):
        self.initial = initialState
        self.goal = goal
        
        if (self._validate_state(initialState) != True):
            raise ValueError('Given state doesn\'t appear to be valid!!!')
        
    def _validate_state(self, state):
		totalElements = len(state)
		
		return is_perfect_square(totalElements)
    
    def goal_test(self, state):
        # print "Testing goal:"
        # printPuzzle(state)

        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    "Generates all possible combinations from the current position"
    def successor(self, currentState):        
        # Convert state to matrix since it's easier to work with it
        state = expand_state(currentState)
        
        # print "Expanded state:"
        #         print state
        #         
        #         print "Finding successors for state: "
        #         printPuzzle(currentState)
        #         print ""
        
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
            
            as_string = compress_state(new_list)
                        
            possibleCombinations.append(('L',as_string))
        
        "### Move to the right:"
        "Tile can be moved to right if it isn't in the last column"
        if col < (totalCols - 1):
            new_list = deepcopy(state)
            
            switchIndex = col + 1;
                        
            tileForSwitch = new_list[row][switchIndex]
            
            new_list[row][switchIndex] = 0
            new_list[row][col] = tileForSwitch
            
            as_string = compress_state(new_list)
                        
            possibleCombinations.append(('R', as_string))
            
        "### Move up:"
        if row != 0:
            new_list = deepcopy(state)
            
            switchIndex = row - 1;
            
            tileForSwitch = new_list[switchIndex][col]
            
            
            new_list[switchIndex][col] = 0
            new_list[row][col] = tileForSwitch
            
            as_string = compress_state(new_list)
                        
            possibleCombinations.append(('U', as_string))
            
        "### Move down:"
        if row < totalRows - 1:
            new_list = deepcopy(state)
            
            switchIndex = row + 1;
            
            tileForSwitch = new_list[switchIndex][col]
            
            new_list[switchIndex][col] = 0
            new_list[row][col] = tileForSwitch
            
            as_string = compress_state(new_list)
                        
            possibleCombinations.append(('D', as_string))
        
        # print "Returning all possible combinations"
        # print possibleCombinations
        
        # print "\n\n########\n\nFrom state:\n\n"
        #         printPuzzle(currentState)
        #         print "\n\nPossible combinations are: \n\n"
        #         
        #         for comb in possibleCombinations:
        #             printPuzzle(comb[1])
        #             print ""
        #             print ""
        
        return possibleCombinations
        
        
        
        
    def _get_empty_tile_position(self, state):
        rowNum = 0;

        for row in state:            
            if 0 in row:
                return (rowNum, row.index(0))
            
            rowNum += 1
            
        return rowNum

def printPuzzle(state):
    # I assume that all puzzles have sqrt(state)*sqrt(state) dimensions :)
    
    dimension = int(math.sqrt(len(state)))
    
    for i in range(0, len(state)):
        if i > 0 and i % dimension == 0:
            print ""
            
        print "%s " % state[i],
        
    print ""
    print ""

def is_perfect_square(n):
  if not ( isinstance(n, (int, long)) and ( n >= 0 ) ):
    return False 
  else:
    nsqrt = math.sqrt(n)
    return nsqrt == math.trunc(nsqrt)


# Expands the puzzle state (e.g. 012345678) into a n-dimensional matrix
def expand_state(state):
    dimension = int(math.sqrt(len(state)))
    
    matrix = []
    
    row = 0
    j = 0
    counter = 0
    
    elements = []
    for characterIndex in range(0, len(state)):
        if characterIndex > 0 and characterIndex % dimension == 0:
            matrix.append(elements)
            elements=[]
        element = state[characterIndex]
        elements.append(int(element))
    matrix.append(elements)

    return matrix
    
def compress_state(state):
    dimension = len(state)
    
    characters = ""
    
    for i in range(dimension):
        for j in range(dimension):
            characters += str(state[i][j])
            
    return characters

# In[174]:

initialState    = "867254301"
goalState       = "012345678"

p = Puzzle8Problem(initialState, goalState)

def silent_print():
    return
    
print "Going to solve the following puzzle:"
printPuzzle(initialState)

def depth_limited_search(problem, limit=100):
    "[Fig. 3.12]"
    def recursive_dls(node, problem, limit):
        cutoff_occurred = False
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            for successor in node.expand(problem):
                result = recursive_dls(successor, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result != None:
                    return result
        if cutoff_occurred:
            return 'cutoff'
        else:
            return None
    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)

algorithms = {
    'DepthFirstGraphSearch': depth_first_graph_search, 
    'BredthFirstGraphSearch': breadth_first_graph_search
}

for key, func in algorithms.iteritems():
    print "Using %s algorithm to solve this puzzle ... \n\n" % key
    
    solution = func(p)
    
    if solution == None:
        print "%s algorithm wasn't able to solve this puzzle :(" % key
        continue
    
    path = solution.path()
    path.reverse()
    
    # print "\n\nSolution found successfully! \n\tPath length: %s \n\tSteps to solution: %s\n\tDepth: %s\n\n" % (len(path), path, solution.depth)
    print "\n\nSolution found successfully! \n\tPath length: %s \n\tDepth: %s\n\n" % (len(path), solution.depth)

sys.exit(0)
