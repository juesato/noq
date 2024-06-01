
"""Usage: python -m scripts.test_yinyang."""
from solvers import yinyang
from solvers.utils import encoding
puzzle1 = """
...0.1
...0..
0.1...
11.0..
..0...
......
""".strip()
solution1 = """
000001
011011
001001
111011
100001
111111
""".strip()

puzzle2 = """
...01
....1
....0
.....
.....""".strip()
solution2 = """
00001
01111
01000
010..
000..""".strip()

puzzle3 = """
...............
....1..1...1...
..1.....11...0.
...1...0.......
..1.10.........
.1..1..1.......
.....1.1.......
1.....1........
.1.............
...1.1.........
.0.11..........
..1............
..1............
...............
...............
""".strip()

def _decode(solution: dict, filter_fn = None):
    # This is something like {'1,1': 'white_circle.png', '1,3': 'white_circle.png', ...}
    rcs = solution.keys()
    num_rows = (max([int(rc.split(',')[0]) for rc in rcs]) + 1) // 2
    num_cols = (max([int(rc.split(',')[1]) for rc in rcs]) + 1) // 2
    grid = [['.' for _ in range(num_cols)] for _ in range(num_rows)]
    output = ''
    mapping = {
        'white_circle.png': '0',
        'black_circle.png': '1',
    }
    for r in range(num_rows):
        for c in range(num_cols):
            if filter_fn is not None and not filter_fn(r, c):
                output += '.'  # Use '.' for cells which aren't part of the puzzle.
            else:
                output += mapping[solution[f'{2*r+1},{2*c+1}']]
        output += '\n'
    return output.strip()


def test_basic():
    e = yinyang.parse(puzzle1)
    sols = yinyang.solve(e)
    assert len(sols) == 1
    assert _decode(sols[0]) == solution1
    print('[test_basic] Passed')


def test_nonrectangular():
    e = yinyang.parse(puzzle2)
    filter_fn = yinyang.make_filter_fn(solution2)
    sols = yinyang.solve(e, filter_fn=filter_fn)
    assert len(sols) == 1
    assert _decode(sols[0], filter_fn=filter_fn) == solution2
    print('[test_nonrectangular] Passed')

def test_big():
    # The real puzzle.
    e = yinyang.parse(puzzle3)
    def filter_fn(r, c):
        if r < 5:
            return True
        elif 5 <= r < 10:
            return c < 10
        elif 10 <= r:
            return c < 5
    sols = yinyang.solve(e, filter_fn=filter_fn)
    assert len(sols) == 1
    print('SOLUTION:\n===')
    print(_decode(sols[0], filter_fn=filter_fn))

# Can only run 1 at a time, due to claspy limitations.
# test_basic()
# test_nonrectangular()
test_big()