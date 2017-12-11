def steps(move_counts):
    # Hex grid:
    #    \  N  /
    #  NW +---+ NE
    # ---<  0  >---
    #  SW +---+ SE
    #    /  S  \
    # Cancel S against N, NE against SW, NE against SE
    n = move_counts['n'] - move_counts['s']
    sw = move_counts['sw'] - move_counts['ne']
    se = move_counts['se'] - move_counts['nw']
    # These three are opposites. Cancel one against the other two.
    sw, se = sw - n, se - n
    # If the remaining two components have the same sign, we can cancel further
    if (sw >= 0) == (se >= 0):
        s = min(sw, se, key=abs)
        return abs(sw + se - s)
    # Otherwise, the shortest distance is simply the absolute sum of the two
    return abs(sw) + abs(se)


move_counts = {'n': 0, 'ne': 0, 'se': 0, 's': 0, 'sw': 0, 'nw': 0}
max_steps = 0
with open('11.input') as f:
    moves = f.read().rstrip().split(',')
    for m in moves:
        move_counts[m] += 1
        max_steps = max(max_steps, steps(move_counts))

# part 1
print(steps(move_counts))

# part 2
print(max_steps)
