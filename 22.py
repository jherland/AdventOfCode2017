from collections import defaultdict


# Use text file 'coordinates': i is vertical direction, increasing downwards,
# j is horizontal direction, increasing rightwards
def parse_grid(f):
    grid = defaultdict(lambda: '.')
    for i, line in enumerate(f):
        for j, c in enumerate(line.rstrip()):
            assert c in {'.', '#'}
            grid[(i, j)] = c
    return grid, (i // 2, j // 2)  # return grid and center point


def print_grid(grid, pos, dir):
    mini = min(min(p[0] for p in grid.keys()), pos[0])
    maxi = max(max(p[0] for p in grid.keys()), pos[0])
    minj = min(min(p[1] for p in grid.keys()), pos[1])
    maxj = max(max(p[1] for p in grid.keys()), pos[1])
    arrow = {'N': '^', 'E': '>', 'S': 'v', 'W': '<'}[dir]
    for i in range(mini, maxi + 1):
        for j in range(minj, maxj + 1):
            print(arrow if pos == (i, j) else ' ', end='')
            print(grid[(i, j)], end='')
            print(arrow if pos == (i, j) else ' ', end='')
        print()


def step(grid, pos, dir, rules):
    def move(pos, dir):
        i, j = pos
        return {
            'N': (i - 1, j),
            'E': (i, j + 1),
            'S': (i + 1, j),
            'W': (i, j - 1),
        }[dir]

    state, turn = rules[grid[pos]]
    grid[pos] = state
    dir = turn[dir]
    pos = move(pos, dir)
    return grid, pos, dir, state


def run_epidemic(grid, pos, dir, num_steps, rules):
    # print_grid(grid, pos, dir)
    infections = 0
    for _ in range(num_steps):
        grid, pos, dir, state = step(grid, pos, dir, rules)
        # print(state)
        # print_grid(g, pos, dir)
        if state == '#':
            infections += 1
    return infections


with open('22.input') as f:
    grid, center = parse_grid(f)
# grid, center = parse_grid(['..#', '#..', '...'])

TurnRight = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
TurnLeft = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
Reverse = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}
KeepGoing = {'N': 'N', 'E': 'E', 'S': 'S', 'W': 'W'}

Part1Rules = {'.': ('#', TurnLeft), '#': ('.', TurnRight)}
Part2Rules = {
    '.': ('W', TurnLeft),
    'W': ('#', KeepGoing),
    '#': ('F', TurnRight),
    'F': ('.', Reverse),
}

# part 1
print(run_epidemic(grid.copy(), center, 'N', 10000, Part1Rules))

# part 2
print(run_epidemic(grid.copy(), center, 'N', 10000000, Part2Rules))
