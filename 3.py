def spiral():
    '''Generate coordinates from the square spiral.'''
    yield 0, 0
    r = 0
    while True:
        r += 1
        for y in range(-r + 1, r):
            yield r, y  # right edge
        for x in range(r, -r, -1):
            yield x, r  # top edge
        for y in range(r, -r, -1):
            yield -r, y  # left edge
        for x in range(-r, r + 1):
            yield x, -r  # bottom edge


cached = [None]
the_spiral = spiral()


def coord(n):
    '''Return coordinate for spiral position n.'''
    assert isinstance(n, int) and n >= 1
    while len(cached) <= n:
        cached.append(next(the_spiral))
    return cached[n]


def steps(coord):
    '''Count taxicab length from origin to coord (x, y).'''
    x, y = coord
    return abs(x) + abs(y)


def adjacent(coord):
    '''Generate coords adjacent to the given coord.'''
    x, y = coord
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            yield x + dx, y + dy


# part 1
print(steps(coord(361527)))

# part 2
n = 1
vals = {(0, 0): 1}
while vals[coord(n)] < 361527:
    n += 1
    assert coord(n) not in vals
    vals[coord(n)] = sum(vals.get(c, 0) for c in adjacent(coord(n)))

print(vals[coord(n)])
