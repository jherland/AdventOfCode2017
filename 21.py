from math import sqrt
import numpy as np


class Square:
    '''2D square of binary pixels.'''

    @classmethod
    def parse(cls, s):
        '''Build Square instance from string like '.#./..#/###'.'''
        d = {'#': 1, '.': 0}
        return cls(np.array([[d[c] for c in row] for row in s.split('/')]))

    def __init__(self, array):
        # Any 2D square array is acceptable
        assert len(array.shape) == 2 and array.shape[0] == array.shape[1]
        self.a = array

    @property
    def size(self):
        return self.a.shape[0]

    def __hash__(self):
        return hash(self.a.tostring())

    def __str__(self):
        return str(self.a)

    def __eq__(self, other):
        return np.array_equal(self.a, other.a)

    def on(self):
        '''Return number of '#' pixels in this square.'''
        return self.a.sum()

    def permutations(self):
        for rot in range(4):
            a = np.rot90(self.a, rot)
            yield self.__class__(a)
            yield self.__class__(np.flipud(a))
            yield self.__class__(np.fliplr(a))
            yield self.__class__(np.flipud(np.fliplr(a)))

    def enhance(self, rulebook):
        return rulebook[self]

    def atoms(self):
        '''Split this square into a stream of 2x2 or 3x3 squares.'''
        assert self.size % 2 == 0 or self.size % 3 == 0
        atom_size = 2 if self.size % 2 == 0 else 3
        print('Splitting {0}x{0} square into {1} {2}x{2} squares'.format(
            self.size, (self.size // atom_size) ** 2, atom_size))

        assert self.size % atom_size == 0
        for row in np.split(self.a, self.size // atom_size, axis=0):
            for col in np.split(row, self.size // atom_size, axis=1):
                assert col.shape == (atom_size, atom_size)
                yield self.__class__(col)

    @classmethod
    def join(cls, squares):
        '''Join stream of NxN equally-sized squares into a larger square.'''
        arrays = [sq.a for sq in squares]
        ushape = arrays[0].shape
        assert len(ushape) == 2 and ushape[0] == ushape[1]
        assert all(arr.shape == ushape for arr in arrays)
        print('Joining {} {}x{} squares'.format(len(arrays), *ushape))
        n = int(sqrt(len(arrays)))
        assert len(arrays) == n ** 2  # we have NxN arrays
        return cls(np.block([arrays[i * n:(i + 1) * n] for i in range(n)]))

    def iterate(self, rulebook):
        '''Return the next iteration of self, enhanced with the given rules.'''
        return Square.join(square.enhance(rulebook) for square in self.atoms())


def parse_rule(line):
    assert ' => ' in line
    before, after = (Square.parse(s) for s in line.split(' => '))
    assert before.size + 1 == after.size
    return before, after


with open('21.input') as f:
    rules = [parse_rule(line.rstrip()) for line in f]  # [(before, after)...]

# Generate permutations of 'before' here, so square matching == dict lookup
rulebook = {p: t for f, t in rules for p in f.permutations()}

square = Square.parse('.#./..#/###')

# part 1
for _ in range(5):
    square = square.iterate(rulebook)
    print(square)
print(square.on())

# part 2
for _ in range(5, 18):
    square = square.iterate(rulebook)
print(square.on())
