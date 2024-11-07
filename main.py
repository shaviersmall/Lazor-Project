import numpy as np
import time
from itertools import permutations

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
    def __init__(self, game_board):
       self.grid = game_board.grid
        self.blocks = game_board.blocks
        self.laser_pts = game_board.laser_pts
        self.soln_pts = game_board.soln_pts

   def get_open_positions(self):
        open_positions = [(x, y) for y, row in enumerate(self.grid) for x, cell in enumerate(row) if cell == 'o']
        return open_positions

    def generate_block_combinations(self):
        blocks_to_place = []
        for block_type, count in self.blocks.items():
            blocks_to_place.extend([block_type] * count)
        return blocks_to_place

    def move_blocks(self):
        open_positions = self.get_open_positions()
        blocks_to_place = self.generate_block_combinations()
        for block_placement in permutations(open_positions, len(blocks_to_place)):
            config = {}
            for block, position in zip(blocks_to_place, block_placement):
                config[position] = block
            yield config

    def apply_configuration(self, config):
        board_copy = self.grid.copy()
        for pos, block_type in config.items():
            board_copy[pos[1]][pos[0]] = block_type
        return board_copy

     def move_laser(self, start_pos, direction, board):
        x, y = start_pos
        dx, dy = direction
        path = []
        while (0 <= x < board.shape[1]) and (0 <= y < board.shape[0]):
            path.append((x, y))
            current_block = board[y][x]
            if current_block == 'B':  # Opaque
                break
            elif current_block == 'A':  # Reflect
                dx, dy = -dy, dx
            elif current_block == 'C':  # Refract
                dx, dy = -dy, dx
            x, y = x + dx, y + dy
        return path

    def solve(self):
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

    def check_solution(self): #if laser_pos == soln_pos
        return all(point in hit_points for point in self.grid.soln_pts)

    def save_solution(self, solution_grid, block_config, output_file='solution.bff'):
        """
        Save the solution configuration to a .bff file.

        Parameters:
        - solution_grid: The grid with the blocks placed for the solution.
        - block_config: Dictionary of block positions and types.
        - output_file: Filename for the saved solution.
        """
        with open(output_file, 'w') as f:
            f.write("# Solution File\n\n")
            
            # Write the grid
            f.write("GRID START\n")
            for row in solution_grid:
                f.write(" ".join(row) + "\n")
            f.write("GRID STOP\n\n")
            
            # Write block counts (if needed)
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
        
    
