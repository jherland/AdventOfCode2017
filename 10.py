class KnotHash:
    Size = 256
    Density = 16
    assert Size % Density == 0

    def __init__(self):
        self.list = list(range(self.Size))
        self.pos = 0
        self.skip = 0

    def reverse_move_increase(self, length):
        indices = [i % self.Size for i in range(self.pos, self.pos + length)]
        m = self.list[:]
        for i, j in zip(indices, reversed(indices)):
            self.list[i] = m[j]
        self.pos = (self.pos + length + self.skip) % self.Size
        self.skip += 1

    def update(self, lengths):
        for length in lengths:
            self.reverse_move_increase(length)

    def densify(self):
        ret = []
        for i in range(0, self.Size, self.Size // self.Density):
            v = 0
            for j in range(self.Density):
                v ^= self.list[i + j]
            ret.append(v)
        return ret

    def hex(self):
        return ''.join('{0:02x}'.format(n) for n in self.densify())


# part 1
h = KnotHash()
with open('10.input') as f:
    h.update(int(word) for word in f.read().rstrip().split(','))
print(h.list[0] * h.list[1])

# part 2
h = KnotHash()
with open('10.input') as f:
    lengths = [ord(c) for c in f.read().rstrip()] + [17, 31, 73, 47, 23]
for n in range(64):
    h.update(lengths)
print(h.hex())
