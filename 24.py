def parse_components(f):
    for line in f:
        a, b = line.rstrip().split('/')
        yield int(a), int(b)

with open('24.input') as f:
    components = list(parse_components(f))

components2 = list(parse_components("""\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10\
""".split('\n')))

components.sort(key=lambda i: -sum(i))

def build(chain, components):
    if not components:  # No components left
        yield chain
        return
    grown = False
    for i, c in enumerate(components):
        # Add c onto the chain, if possible.
        if c[0] == chain[-1]:
            yield from build(
                chain + [c[0], c[1]], components[:i] + components[i + 1:])
            grown = True
        if c[1] == chain[-1]:
            yield from build(
                chain + [c[1], c[0]], components[:i] + components[i + 1:])
            grown = True
        if not grown:  # Nothing could be added, this chain is complete
            yield chain

# part 1
max_chain = []
max_strength = 0
max_length = 0
try:
    for chain in build([0], components):
        length = len(chain)
        strength = sum(chain)
        if length > max_length:
            max_chain = chain
            max_length = length
            max_strength = strength
            print(max_length, max_strength, max_chain)
        elif length == max_length and strength > max_strength:
            max_chain = chain
            max_strength = strength
            print(max_length, max_strength, max_chain)
except:
    pass
print()
print(max_length, max_strength, max_chain)
