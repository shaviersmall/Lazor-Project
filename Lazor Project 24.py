import numpy as np
import time
from itertools import permutations
from copy import deepcopy

class Block:
    '''
    Class object that dictates how block types interact with lasers. Also includes methods for whether
    they are fixed, if they are cells that hold blocks, and their position on the board.

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
    
    def holdsBlock(self):
        pass

class OpaqueBlock(Block):
    def interactions(self, laser_direction):
        return [] #Laser stops at block
    
class ReflectBlock(Block):
    def interactions(self, laser_direction):
        dx, dy = laser_direction
        # Reflect diagonally
        return [(-dy, dx)] if dx != 0 and dy != 0 else [(-dx, dy), (dx, -dy)]

    
class RefractBlock(Block):
    def interactions(self, laser_direction):
        dx, dy = laser_direction
        # Refract laser: continue forward and reflect diagonally
        return [(dx, dy), (-dy, dx), (dy, -dx)]

class OBlock(Block):
    def interactions(self, laser_direction):
        return laser_direction #Laser continues through empty block
    
    def holdsBlock(self):
        return True
    
class XBlock(Block):
    def interactions(self, laser_direction):
        return laser_direction
    
    def holdsBlock(self): 
        return False

class GameBoard: 
    ''' 
    Class to read bff file, initialize, and create game board based on the file given.

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
                    pts = list(map(int, line[1:].strip().split()))
                    self.laser_pts.append(((pts[0], pts[1]), (pts[2], pts[3])))
                elif line.startswith('P'):
                    pts = list(map(int, line[1:].strip().split()))
                    self.soln_pts.append((pts[0], pts[1]))

                if read_grid == True: #When between GRID START and GRID STOP, appends each line to the grid
                    line.split()
                    row = []
                    for char in line:
                        if char == 'A':
                            row.append(ReflectBlock())
                        elif char == 'B':
                            row.append(OpaqueBlock())
                        elif char == 'C':
                            row.append(RefractBlock())
                        elif char == 'o': 
                            row.append(OBlock())
                        elif char == 'x':
                            row.append(XBlock())

                    self.grid.append(row)

                if read_blocks == True: 
                    block_def = line.split()
                    if len(block_def) == 2:
                        block_type = block_def[0]
                        count = int(block_def[1]) 
                        self.block_dict[block_type] = count
        
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
    ''' 
    A class containing the game logic and aspectss needed to solve the game board.
    '''
    def __init__(self, game_board):
       self.grid = game_board.grid
       self.blocks = game_board.block_dict
       self.laser_pts = game_board.laser_pts
       self.soln_pts = game_board.soln_pts 

    def get_open_positions(self):
        # All available positions on board (marked with an O)
        open_positions = [(x, y) for y, row in enumerate(self.grid) for x, 
                          cell in enumerate(row) if isinstance(cell, OBlock)]
        return open_positions

    def generate_block_combinations(self):
        # Creates a list of possible block combinations to use
        blocks_to_place = []
        for block_type, count in self.blocks.items():
            blocks_to_place.extend([block_type] * count)
        return blocks_to_place

    def move_blocks(self):
        open_positions = self.get_open_positions()
        blocks_to_place = self.generate_block_combinations()
        
        # Map block type strings to their respective classes
        block_type_map = {'A': ReflectBlock, 'B': OpaqueBlock, 'C': RefractBlock}
        
        for block_placement in permutations(open_positions, len(blocks_to_place)):
            config = {}
            for block, position in zip(blocks_to_place, block_placement):
                config[position] = block_type_map[block]  # Use class reference instead of string
            yield config

    def apply_configuration(self, config):
        # Creates a copy of the board suitable for solving
        board_copy = deepcopy(self.grid)
        for pos, block_type in config.items():
            board_copy[pos[1]][pos[0]] = block_type() 
        return board_copy

    def move_laser(self, start_pos, direction, board):
        # Defines how the laser moves on the board and when interacting with blocks
        x, y = start_pos
        dx, dy = direction
        path = set()
    
        while (0 <= x < board.shape[1]) and (0 <= y < board.shape[0]):
            path.add((x, y))
            current_block = board[y][x]
            
            if isinstance(current_block, OpaqueBlock):  # Laser stops at opaque block
                break
            elif isinstance(current_block, ReflectBlock):  # Reflects laser at 90 degrees
                dx, dy = -dy, dx
            elif isinstance(current_block, RefractBlock):  # Refracts and reflects
                path.update(self.move_laser((x, y), (-dy, dx), board))  # Continue refracted beam
            x, y = x + dx, y + dy  # Move forward
    
        return path

    def solve(self):
        # APplies all the logic to solve the board
        for block_config in self.move_blocks():
            board = self.apply_configuration(block_config)
            hit_points = set()
            for laser_start, direction in self.laser_pts:
                hit_points.update(self.move_laser(laser_start, direction, board))
            if all(target in hit_points for target in self.soln_pts):
                print("Solution found!")
                self.save_solution(board, block_config)  # Call save_solution here
                return board, block_config
        print("No solution found.")
        return None, None

    def check_solution(self, hit_points):
        # Checks if all points have been hit
        return all(point in hit_points for point in self.soln_pts)

def save_solution(self, solution_grid, block_config, output_file='solution.bff'):
    # Saves solution to a bff file
    with open(output_file, 'w') as f:
        f.write("# Solution File\n\n")
        f.write("GRID START\n")
        for row in solution_grid:
            f.write(" ".join(type(cell).__name__[0] if isinstance(cell, Block) 
                             else cell for cell in row) + "\n")
        f.write("GRID STOP\n\n")
    
        # Write block counts
        for block_type, count in self.blocks.items():
            f.write(f"{block_type} {count}\n")
        
        # Write laser points
        for laser, direction in self.laser_pts:
            f.write(f"L {laser[0]} {laser[1]} {direction[0]} {direction[1]}\n")
        
        # Write solution points
        for target in self.soln_pts:
            f.write(f"P {target[0]} {target[1]}\n")

    print(f"Solution saved to {output_file}")

    

if __name__ == '__main__':
    start = time.time()
    board = GameBoard('tiny_5.bff')
    print(board)
    
    solver = Solver(board)
    solution, config = solver.solve()
    if solution:
        print("Final board configuration with solution:")
        print(np.array2string(solution))
        print("Block configuration:", config)
    end = time.time() - start
    print(end)
        
    
