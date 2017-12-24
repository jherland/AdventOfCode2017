def parse_components(f):
    for line in f:
        a, b = line.rstrip().split('/')
        yield int(a), int(b)


def build(chain, comps):
    grown = False
    for i, c in enumerate(comps):  # add c onto the chain, if possible.
        if c[0] == chain[-1]:
            yield from build(chain + [c[0], c[1]], comps[:i] + comps[i + 1:])
            grown = True
        if c[1] == chain[-1]:
            yield from build(chain + [c[1], c[0]], comps[:i] + comps[i + 1:])
            grown = True
    if not grown:  # nothing could be added, this chain is complete
        yield chain


with open('24.input') as f:
    comps = sorted(parse_components(f), key=lambda t: -sum(t))

max_strength = (0, [])  # (strength, chain)
max_length = (0, 0, [])  # (length, strength, chain)
for chain in build([0], comps):
    strength = sum(chain), chain
    length = len(chain), sum(chain), chain
    if strength > max_strength:
        max_strength = strength
    if length > max_length:
        max_length = length

# part 1
print(max_strength[0])

# part 2
print(max_length[1])
