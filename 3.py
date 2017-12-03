def spiral():
    '''Generate coordinates from the square spiral.'''
    yield 0, 0
    r = 0
    while True:
        r += 1
        yield from ((r, y) for y in range(-r + 1, r))  # right edge
        yield from ((x, r) for x in range(r, -r, -1))  # top edge
        yield from ((-r, y) for y in range(r, -r, -1))  # left edge
        yield from ((x, -r) for x in range(-r, r + 1))  # bottom edge


cached = [None]
the_spiral = spiral()


def coord(n):
    '''Return coordinate for spiral position n.'''
    assert isinstance(n, int) and n >= 1
    while len(cached) <= n:
        cached.append(next(the_spiral))
    return cached[n]


def steps(x, y):
    '''Count taxicab length from origin to coord (x, y).'''
    return abs(x) + abs(y)


def adjacent(x, y):
    '''Generate coords adjacent to the given coord.'''
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            yield x + dx, y + dy


# part 1
print(steps(*coord(361527)))

# part 2
n, vals = 1, {(0, 0): 1}
while vals[coord(n)] < 361527:
    n += 1
    vals[coord(n)] = sum(vals.get(c, 0) for c in adjacent(*coord(n)))

print(vals[coord(n)])
