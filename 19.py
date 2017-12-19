class Diagram:
    SYMBOLS = set('|+-ABCDEFGHIKJLMNOPQRSTUVWXYZ')
    REVERSE = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}  # up/down/left/right

    @classmethod
    def build(cls, lines):
        '''Return Diagram instance and starting point.'''
        lines = [line.rstrip() for line in lines]
        d = {}  # map (y, x) to symbol at (y, x). (0, 0) is top left
        start = None  # starting point (dir_from, position, symbol)
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == ' ':
                    continue
                assert c in cls.SYMBOLS, c
                d[(i, j)] = c
                # start at first encountered symbol, assume we arrive from top
                if start is None:
                    assert i == 0 and c == '|'
                    start = 'd', (i, j), c
        return cls(d), start

    def __init__(self, d):
        self.d = d

    def adjacent(self, y, x):
        adjs = [
            ('u', (y - 1, x)),
            ('d', (y + 1, x)),
            ('l', (y, x - 1)),
            ('r', (y, x + 1)),
        ]
        for dir, (y, x) in adjs:
            if (y, x) in self.d:
                yield dir, (y, x), self.d[(y, x)]

    def step(self, cur):
        '''Walk one step from the current to the next (dir, pos, sym).'''
        dir, pos, sym = cur
        adjs = {dir: (dir, pos, sym) for dir, pos, sym in self.adjacent(*pos)}
        try:
            if sym == '+':  # change directions
                assert len(adjs) == 2 and self.REVERSE[dir] in adjs
                del adjs[self.REVERSE[dir]]  # eliminate where we came from
                return adjs.popitem()[1]
            else:  # keep going in same direction
                return adjs[dir]
        except KeyError:  # found the end!
            return None

    def walk(self, cur):
        steps, found = 0, []
        while cur:
            steps += 1
            sym = cur[2]
            if sym not in set('|-+'):
                found.append(sym)
            cur = self.step(cur)
        return steps, found


with open('19.input') as f:
    d, start = Diagram.build(f)
steps, found = d.walk(start)

# part 1
print(''.join(found))

# part 2
print(steps)
