from .claspy import *
from . import utils
from .utils.solutions import *
from .utils.encoding import Encoding

def encode(string):
    return utils.encode(string, clue_encoder = lambda s: s)
    
def solve(E, filter_fn = None):
    set_max_val(2)

    s = utils.shading.RectangularGridShadingSolver(E.R, E.C, filter_fn=filter_fn)

    # Optimize solving by providing known roots for white and black parts
    white_root, black_root = None, None
    for (r, c) in E.clues:
        if E.clues[(r,c)] == 'w':
            white_root = (r,c)
        else:
            black_root = (r,c)
        if white_root and black_root:
            break

    s.white_connectivity(white_root)
    s.black_connectivity(black_root)
    s.no_white_2x2()
    s.no_black_2x2()

    for (r, c) in E.clues:
        require(s.grid[r][c] == (E.clues[(r,c)] == 'b'))
    
    def format_function(r, c):
        return ('black' if s.grid[r][c].value() else 'white') + '_circle.png'

    return get_all_grid_solutions(s.grid, format_function = format_function)
   
def decode(solutions):
    return utils.decode(solutions)

def parse(board_str):
    board = board_str.strip().split('\n')
    num_rows = len(board)
    num_cols = len(board[0])
    bw_mapping = {
        '1': 'b',
        '0': 'w',
    }
    clues = {}
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] in bw_mapping:
                clues[(r, c)] = bw_mapping[board[r][c]]
    return Encoding(rows=num_rows, cols=num_cols, clue_cells=clues)

def make_filter_fn(solution_str):
    board = solution_str.strip().split('\n')
    num_rows = len(board)
    num_cols = len(board[0])
    clue_chars = ['0', '1']
    clue_cells = []
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] in clue_chars:
                clue_cells.append((r, c))
    clue_cells = set(clue_cells)
    return lambda r, c: (r, c) in clue_cells
