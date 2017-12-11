# Hex grid:
#
#      \ n  /
#    nw +--+ ne
#      /    \
#    -+      +-
#      \    /
#    sw +--+ se
#      / s  \
#
# Use 2D-coordinates, with +x in NE, -x in SW, +y in N, and -y in S directions.
# Moving SE equals x + 1, y - 1; moving NW equals x - 1, y + 1.


def move(coord, move):
    '''Return new coord after move.'''
    assert move in ['n', 'ne', 'se', 's', 'sw', 'nw']
    x, y = coord
    return {
        'n': (x, y + 1),
        'ne': (x + 1, y),
        'se': (x + 1, y - 1),
        's': (x, y - 1),
        'sw': (x - 1, y),
        'nw': (x - 1, y + 1),
    }[move]


def steps(coord):
    # Coords give the number of NE/SW steps (x), and number of N/S steps (y)
    # A SW + N step can be replace by a single NW step, likewise NE + S => SE
    # Hence if x and y have the same sign, the # steps is simply their sum,
    # Otherwise, first bring one of them to 0 using the above transformations.
    x, y = coord
    if x >= 0 and y >= 0:  # Only NE and N steps needed
        return x + y
    if x < 0 and y < 0:  # Only SW and S steps needed
        return abs(x + y)
    if x < 0 and y >= 0:  # Replace SW + N => NW
        nw = min(abs(x), y)
        return abs(x) + y - nw
    if x >= 0 and y < 0:  # Replace NE + S => SE
        se = min(x, abs(y))
        return x + abs(y) - se


with open('11.input') as f:
    moves = f.read().rstrip().split(',')
    for m in moves:
        assert m in ['n', 'ne', 'se', 's', 'sw', 'nw']

coord = (0, 0)
max_steps = 0

for m in moves:
    coord = move(coord, m)
    max_steps = max(max_steps, steps(coord))

# part 1
print(steps(coord))

# part 2
print(max_steps)
