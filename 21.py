from math import sqrt


class Picture:
    @classmethod
    def parse(cls, s):
        '''Build Picture instance from string like '.#./..#/###'.'''
        return cls(tuple(s.split('/')))

    def __init__(self, lines):
        self.lines = tuple(lines)
        assert all(len(line) == len(self.lines) for line in self.lines)
        self.size = len(self.lines)

    def __hash__(self):
        return hash(self.lines)

    def __eq__(self, other):
        return self.lines == other.lines

    def on(self):
        '''Return number of '#' pixels in this picture.'''
        return sum(c == '#' for line in self.lines for c in line)

    def atoms(self):
        '''Split this picture into a stream of 2x2 or 3x3 atoms.'''
        assert self.size % 2 == 0 or self.size % 3 == 0
        AtomX = Atom2 if self.size % 2 == 0 else Atom3
        yield from AtomX.extract(self)

    @classmethod
    def join(cls, pictures):
        '''Join stream of NxN equally-sized pictures into a larger picture.'''
        pictures = list(pictures)
        unit_size = pictures[0].size
        assert all(pic.size == unit_size for pic in pictures)
        n = int(sqrt(len(pictures)))
        assert len(pictures) == n ** 2  # we have NxN pictures
        result = [''] * n * unit_size
        for i in range(0, n * unit_size, unit_size):
            for pic in pictures[:n]:
                for j in range(unit_size):
                    result[i + j] += pic.lines[j]
            pictures = pictures[n:]
        assert not pictures
        return cls(result)

    def iterate(self, rulebook):
        '''Return the next iteration of self, enhanced with the given rules.'''
        return Picture.join(atom.enhance(rulebook) for atom in self.atoms())


class Atom(Picture):
    Size = NotImplemented

    def __init__(self, lines):
        super().__init__(lines)
        assert self.size == self.Size

    def flip_vert(self):
        return self.__class__(tuple(reversed(self.lines)))

    def flip_horiz(self):
        return self.__class__(tuple(line[::-1] for line in self.lines))

    def rotate_cw(self):
        raise NotImplementedError()

    def rotations(self):
        yield self
        yield self.rotate_cw()
        yield self.rotate_cw().rotate_cw()
        yield self.rotate_cw().rotate_cw().rotate_cw()

    def flips(self):
        yield self
        yield self.flip_horiz()
        yield self.flip_vert()
        yield self.flip_vert().flip_horiz()

    def permutations(self):
        for rot in self.rotations():
            yield from rot.flips()

    def enhance(self, rulebook):
        key = self.size, self.on()
        assert key in rulebook, key
        assert self in rulebook[key], rulebook[key]
        return rulebook[key][self]


class Atom2(Atom):
    Size = 2

    @classmethod
    def extract(cls, pic):
        assert pic.size % cls.Size == 0
        lines = pic.lines
        while lines:
            l1, l2, *lines = lines
            while l1 or l2:
                (a, b, *l1), (c, d, *l2) = l1, l2
                yield cls((a + b, c + d))

    def rotate_cw(self):
        (a, b), (c, d) = self.lines
        return self.__class__((c + a, d + b))


class Atom3(Atom):
    Size = 3

    @classmethod
    def extract(cls, pic):
        assert pic.size % cls.Size == 0
        lines = pic.lines
        while lines:
            l1, l2, l3, *lines = lines
            while l1 or l2 or l3:
                (a, b, c, *l1), (d, e, f, *l2), (g, h, i, *l3) = l1, l2, l3
                yield cls((a + b + c, d + e + f, g + h + i))

    def rotate_cw(self):
        (a, b, c), (d, e, f), (g, h, i) = self.lines
        return self.__class__((g + d + a, h + e + b, i + f + c))


def parse_rule(line):
    assert ' => ' in line
    before, after = (Picture.parse(s) for s in line.split(' => '))
    assert before.size + 1 == after.size
    return before, after


with open('21.input') as f:
    rules = [parse_rule(line.rstrip()) for line in f]  # [(before, after)...]

# Index rules by (before.size, before.on()).
rulebook = {}  # (before.size, before.on()) -> {before.permutations() -> after}
for before, after in rules:
    assert before.size in {2, 3}
    before = Atom2(before.lines) if before.size == 2 else Atom3(before.lines)
    key = before.size, before.on()
    match = rulebook.setdefault(key, {})
    # Also generate all matching input permutations up front
    for perm in before.permutations():
        match[perm] = after

pic = Picture.parse('.#./..#/###')

# part 1
for _ in range(5):
    pic = pic.iterate(rulebook)
print(pic.on())

# part 2
for _ in range(5, 18):
    pic = pic.iterate(rulebook)
print(pic.on())
