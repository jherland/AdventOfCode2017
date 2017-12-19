with open('19.input') as f:
    lines = [line.rstrip() for line in f]

SYMBOLS = set('|+-ABCDEFGHIKJLMNOPQRSTUVWXYZ')
DIRECTIONS = set('uplr')  # up/down/left/right
REVERSE = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
HEIGHT = len(lines)
WIDTH = max(len(line) for line in lines)
dia = {}  # map (y, x) to non-empty symbol at (y, x). (0, 0) is top left
found = []  # letters, in the order encountered

cur = None  # (dir_from, position, symbol) we're currently at
for i, line in enumerate(lines):
    assert 0 <= i < HEIGHT
    for j, c in enumerate(line):
        assert 0 <= j < WIDTH
        if c == ' ':
            continue
        assert c in SYMBOLS, c
        dia[(i, j)] = c
        # start at first encountered symbol, assume we arrive downwards
        if cur is None:
            assert c == '|'
            cur = 'd', (i, j), c


def adjacent_symbols(pos):
    y, x = pos
    adjs = [
        ('u', (y - 1, x)),
        ('d', (y + 1, x)),
        ('l', (y, x - 1)),
        ('r', (y, x + 1)),
    ]
    for dir, (y, x) in adjs:
        if 0 <= y < HEIGHT and 0 <= x < WIDTH and (y, x) in dia:
            yield dir, (y, x), dia[(y, x)]


def walk(cur):
    '''Return next (dir, pos).'''
    dir, pos, sym = cur
    adjs = {dir: (dir, pos, sym) for dir, pos, sym in adjacent_symbols(pos)}
    print(adjs)

    if sym == '+':  # turn around
        assert len(adjs) == 2  # cannot be any doubt where to turn
        del adjs[REVERSE[dir]]  # eliminate where we came from
        try:
            return adjs.popitem()[1]
        except KeyError:  # found the end!
            return None
    else:  # keep going in same dir
        assert sym in set('|-ABCDEFGHIKJLMNOPQRSTUVWXYZ')
        if sym not in set('|-'):  # found a letter!
            found.append(sym)
        try:
            return adjs[dir]
        except KeyError:  # found the end!
            return None


steps = 0
while cur:
    print(cur)
    steps += 1
    cur = walk(cur)

# part 1
print(''.join(found))

# part 2
print(steps)
