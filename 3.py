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

def test_coord(expect, n):
    assert expect == coord(n), '{} => {}'.format(n, coord(n))

test_coord((0, 0), 1)
test_coord((1, 0), 2)
test_coord((1, 1), 3)
test_coord((0, 1), 4)
test_coord((-1, 1), 5)
test_coord((-1, 0), 6)
test_coord((-1, -1), 7)
test_coord((0, -1), 8)
test_coord((1, -1), 9)
test_coord((2, -1), 10)
test_coord((2, 1), 12)
test_coord((-15, 16), 1024)

def steps(coord):
    x, y = coord
    return abs(x) + abs(y)

def test_steps(expect, n):
    assert expect == steps(coord(n)), '{} => {}'.format(n, steps(coord(n)))

test_steps(0, 1)
test_steps(1, 2)
test_steps(2, 3)
test_steps(1, 4)
test_steps(2, 5)
test_steps(1, 6)
test_steps(2, 7)
test_steps(1, 8)
test_steps(2, 9)
test_steps(3, 10)
test_steps(2, 11)
test_steps(3, 12)
test_steps(31, 1024)

print(steps(coord(361527)))
