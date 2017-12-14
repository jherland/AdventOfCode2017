from knothash import KnotHash
from connections import find_group


def hash_inputs(word, n):
    for i in range(n):
        yield '{}-{}'.format(word, i)


def hashes(inputs):
    for inp in inputs:
        yield KnotHash(inp).hex()


def rows(hashes):
    for h in hashes:
        assert len(h) == 32
        bits = [int(c) for d in h for c in '{:04b}'.format(int(d, 16))]
        assert len(bits) == 128
        yield bits


def connected_cells(disk, N):
    padded = [[0] * (N + 1)] + [[0] + r[:N] for r in disk[:N]]
    for i in range(1, len(padded)):
        for j in range(1, N + 1):
            if padded[i][j]:  # non-empty cell is always connected to itself
                yield (i, j), (i, j)
            if padded[i][j] and padded[i-1][j]:  # connected to the cell above?
                yield (i, j), (i - 1, j)
            if padded[i][j] and padded[i][j-1]:  # connected to the left?
                yield (i, j), (i, j - 1)


with open('14.input') as f:
    key = f.read().rstrip()
disk = [r for r in rows(hashes(hash_inputs(key, 128)))]

# part 1
print(sum(sum(row) for row in disk))

# part 2
connections, regions = {}, 0
for a, b in connected_cells(disk, 128):
    connections.setdefault(a, set()).add(b)
    connections.setdefault(b, set()).add(a)
while connections:
    region = find_group(next(iter(connections.keys())), connections)
    connections = {k: v for k, v in connections.items() if k not in region}
    regions += 1
print(regions)
