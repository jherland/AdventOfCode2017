def coord(n):
    assert isinstance(n, int) and n >= 1
    if n == 1:
        return 0, 0

    # Determine radius of n, and how many numbers are covered inside radius r
    r = 0
    while (r * 2 + 1) ** 2 < n:
        r += 1
    covered = (r * 2 - 1) ** 2

    # Coordinates at radius r: (r, -r+1)..(r, r)..(-r, r)..(-r, -r)..(r, -r)
    edge = 0  # 0, 1, 2, 3 = right, top, left, bottom
    pos = n - covered  # position of n along current edge
    while pos > 2 * r:
        edge += 1
        pos -= 2 * r
    assert edge in [0, 1, 2, 3], edge
    assert 0 < pos <= 2 * r, pos

    return {
        # right  ( r  , -r+1) -> ( r,  r)
        0: (r, pos - r),
        # top    ( r-1,  r  ) -> (-r,  r)
        1: (r - pos, r),
        # left   (-r  ,  r-1) -> (-r, -r)
        2: (-r, r - pos),
        # bottom (-r+1, -r  ) -> ( r, -r)
        3: (pos - r, -r),
    }[edge]


def steps(coord):
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
