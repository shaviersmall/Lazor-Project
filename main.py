# 3 kinds of blocks
# opaque
# reflect
# refract

# Block
# field: position
# field: isFixed

# Game

# ParseInput()
# ...
# if line says "GRID START", call ReadInBoard()
# ...

# ReadInBoard()
# create new list to store board rows
# first row tells us how many cols board has
# while there are lines to read... (i.e. while line is not "GRID STOP")
#   create a list for the board row
#   read in the input row string
#   parse each character in input row and populate board row
#   add a blank row to board  

import numpy as np

class Block:
    '''
    Class object that defines blocks based on their type, position, and fixed/non-fixed quality.
    
    '''
    
    def __init__(self, block_type, position): 
        self.block_type = block_type
        self.position = position

    def isFixed(self):
        '''Define if blocks are fixed, return True if so'''

    def _str__(self):
        return "Block type = {self.block_type}, block position = {self.position}"
    
class GameBoard:
    ''' 
    Class to read, initialize, and create game board

    '''
    def __init__(self, grid_file, width = 500, height = 500):
        self.width = width #columns
        self.height = height #rows
        self.grid_file = grid_file #This is the text file containing the grid and board
        #self.blocktype = blocktype #fixed block types based on grid
        #self.target = target #Point that laser must go through for solution
        #self.laser_pos = laser_pos #Starting position for lasers

    def read_board(self, grid_file, height, width):
        grid_list = []
        with open(grid_file) as f:
            for entry in grid_file:
                grid_list.append(entry)

        grid = np.empty(height, width)
        for i in range(grid_list):
            grid[i] = grid_list[i]

        for block in grid:
            if block == 'A':
                blocktype = 'fixed_reflect'
            elif block == 'B':
                blocktype = 'fixed_opaque'
            elif block == 'C':
                blocktype = 'fixed_refract'
            elif block == 'x':
                blocktype = 'no_block'
            elif block == 'o':
                blocktype = 'block_allowed'

    def __str__(self):
        pass

        
    


class Solver:
    pass
        

x = GameBoard('tiny_5.bff')
print(x)