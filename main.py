import numpy as np
import time
start = time.time()

class Block:
    '''
    Class object that dictates how block types interact with lasers.

    Opaque blocks - laser stops entirely at this block
    Reflect block - laser goes through and makes 90 degree angle
    Refract block - laser makes a 90 degree angle
    
    '''
    def __init__(self):
        pass

    def interactions(self):
        #if block_type = something, laser reacts a certain way
        pass
        
    def isFixed(self):
        pass    

class OpaqueBlock(Block):
    def interactions(self, laser_direction):
        return None #Laser stops at block
    
class ReflectBlock(Block):
    def interactions(self, laser_direction):
        #Laser goes through in same direction and reflects at 90 degrees
        dx, dy = laser_direction
        slope = dy / dx
        new_slope = - dx / dy


        return (dx,dy), (dy, -dx) #Two returns: laser going in same direction and slope flipped by 90 degrees
    
class RefractBlock(Block):
    #Laser refracts 90 degrees
    def interactions(self, laser_direction):
        dx, dy = laser_direction 

        return (dy, -dx) #Laser refracts 90 degrees from original direction

class GameBoard: #Remaining work: update GameBoard to take in block types
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
        np.array(self_grid) : np array
            NumPy array that stores the game board.
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
                block_type = 'fixed_reflect'
            elif block == 'B':
                block_type = 'fixed_opaque'
            elif block == 'C':
                block_type = 'fixed_refract'
            elif block == 'x':
                block_type = 'no_block'
            elif block == 'o':
                block_type = 'block_allowed'
        
        self.grid = np.array(self.grid)

        return self.grid 

        

    def __str__(self):
        grid_str = np.array2string(self.grid, separator=', ')
        block_dict_str = ', '.join(f"{k}: {v}" for k, v in self.block_dict.items())
        lasers_str = ', '.join(str(coord) for coord in self.laser_pts)
        solutions_str = ', '.join(str(coord) for coord in self.soln_pts)
        return (f"Grid:\n{grid_str}\n"
                f"Blocks: {block_dict_str}\n"
                f"Laser Points: {lasers_str}\n"
                f"Solution Points: {solutions_str}]\n"
                )


class Solver:
    def __init__(self, grid):
        grid = self.grid

    def move_blocks(self):
        pass
        #initialize positions of open spaces and amounts of movable blocks

    def move_laser(self):
        pass
        #move laser based on fixed and movable block types -> x + dx, y + dy based on Block subclass

    def solve(self): #implement some type of algo (depth first search?) to move the blocks so that the lasers bounce off and hit solution points
        pass 
        #probably call on read_board again to print the solution board
        #include a return False if board cannot be solved and error messages

    def check_solution(self): #if laser_pos == soln_pos
        pass

        
if __name__ == '__main__':
    x = GameBoard('tiny_5.bff')
    print(x)

    #solution = Solve('tiny_5.bff')

end = time.time() - start
print(end)
    
