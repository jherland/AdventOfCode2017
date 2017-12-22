from collections import defaultdict


def print_grid(grid, pos, dir):
    dim = max(abs(coord) for p in set(grid.keys()) | {pos} for coord in p)
    dir = {'N': '^', 'E': '>', 'S': 'v', 'W': '<'}[dir]
    for i in range(+dim, -dim - 1, -1):
        for j in range(-dim, +dim + 1, 1):
            print(dir if pos == (i, j) else ' ', end='')
            print(grid[(i, j)], end='')
            print(dir if pos == (i, j) else ' ', end='')
        print()


def parse_grid(f):
    grid = set()
    for i, line in enumerate(f):
        for j, c in enumerate(line.rstrip()):
            assert c in {'.', '#'}
            if c == '#':
                grid.add((i, j))

    center = i // 2, j // 2
    # Move center of grid to 0,0 and flip y direction
    ret = defaultdict(lambda: '.')
    for y, x in grid:
        pos = center[0] - y, x - center[1]
        ret[pos] = '#'
    return ret


def step1(grid, pos, dir):
    if grid[pos] == '#':  # infected
        dir = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[dir]  # turn right
        grid[pos] = '.'  # clean
        ret = False
    else:  # clean
        dir = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[dir]  # turn left
        grid[pos] = '#'  # infect
        ret = True
    y, x = pos
    move = {'N': (y + 1, x), 'E': (y, x + 1), 'S': (y - 1, x), 'W': (y, x - 1)}
    pos = move[dir]
    return grid, pos, dir, ret


def step2(grid, pos, dir):
    # clean -> weakened -> infected -> flagged -> clean
    next_state = {'.': 'W', 'W': '#', '#': 'F', 'F': '.'}[grid[pos]]
    if grid[pos] == '#':  # infected
        dir = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[dir]  # turn right
    elif grid[pos] == 'F':  # flagged
        dir = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}[dir]  # reverse
    elif grid[pos] == '.':  # clean
        dir = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[dir]  # turn left
    else:  # weakened
        assert grid[pos] == 'W'
        # no turn
    grid[pos] = next_state
    y, x = pos
    move = {'N': (y + 1, x), 'E': (y, x + 1), 'S': (y - 1, x), 'W': (y, x - 1)}
    pos = move[dir]
    return grid, pos, dir, next_state


# part 1
with open('22.input') as f:
    grid = parse_grid(f)

# grid = parse_grid(['..#', '#..', '...'])
pos, dir = (0, 0), 'N'
print_grid(grid, pos, dir)
infections = 0
for _ in range(10000):
    grid, pos, dir, ret = step1(grid, pos, dir)
#    print(ret)
#    print_grid(grid, pos, dir)
    if ret:
        infections += 1
print(infections)

# part 2
with open('22.input') as f:
    grid = parse_grid(f)

# grid = parse_grid(['..#', '#..', '...'])
pos, dir = (0, 0), 'N'
print_grid(grid, pos, dir)
infections = 0
for _ in range(10000000):
    grid, pos, dir, state = step2(grid, pos, dir)
#    print(state)
#    print_grid(grid, pos, dir)
    if state == '#':
        infections += 1
print(infections)
