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
    
class GameBoard:
    ''' 
    Class to read, initialize, and create game board based on the file given.

    '''
    def __init__(self, grid_file, width = 500, height = 500):
        self.width = width #columns
        self.height = height #rows
        self.grid_file = grid_file #This is the text file containing the grid and board
        self.grid = []
        self.block_dict = {}
        self.laser_pts = []
        self.soln_pts = []
        self.read_board()
        #self.blocktype = blocktype #fixed block types based on grid
        #self.target = target #Point that laser must go through for solution
        #self.laser_pos = laser_pos #Starting position for lasers

    def read_board(self):
        ''' 
        Function that reads board from bff and creates it. Parses through grid file to extract 
        information:

        Starting game grid, types and quantities of available blocks, laser sources and paths,
        and intercept positions. This board will be used in the Solver class to automatically find solutions.

        Parameters
        grid_file : bff
            File that game board information is extracted from

        ---
        Returns
        None
        '''
        with open(self.grid_file) as f: #Open the bff file in read mode and set conditions for reading the grid or the info
            read_grid = False
            read_blocks = False
            laser_pts = []
            soln_pts = []

            for line in f:
                line = line.strip()
                if line == 'GRID START':
                    read_grid = True
                    continue
                elif line == 'GRID STOP':
                    read_grid = False
                    read_blocks = True
                    continue
                elif line.startswith('L'):
                    read_blocks == False
                    line.split()
                    pts = list(map(int, line[1:].strip().split()))
                    self.laser_pts.append(((pts[0], pts[1]), (pts[2], pts[3])))
                    continue
                elif line.startswith('P'):
                    line.split()
                    self.soln_pts.append((line[2], line[4]))

                if read_grid == True: #When between GRID START and GRID STOP, appends each line to the grid
                    self.grid.append(line.split())

                if read_blocks == True: 
                    block_def = line.split()
                    if len(block_def) == 2:
                        block_type = block_def[0]
                        counter = block_def[1]
                        self.block_dict[block_type] = counter #Saves as {block type : num blocks}, e.g. {A : 3}

        for block in self.grid: #Sets fixed block types on board
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

        return np.array(self.grid) #ERROR: Grid is being read into array twice?

        

    def __str__(self):
        grid_str = np.array2string(np.array(self.grid))
        block_dict_str = ', '.join(f"{k}: {v}" for k, v in self.block_dict.items())
        lasers_str = ', '.join(str(coord) for coord in self.laser_pts)
        solutions_str = ', '.join(str(coord) for coord in self.soln_pts)
        return (f"Grid:\n{grid_str}\n"
                f"Blocks: {block_dict_str}\n"
                f"Laser Points: {lasers_str}\n"
                f"Solution Points: {solutions_str}]\n"
                )

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
    


class Solver:
    pass
        

if __name__ == '__main__':
    x = GameBoard('tiny_5.bff')
    print(x)
    
