from collections import namedtuple

SIZE = 256
State = namedtuple('State', ['l', 'pos', 'skip'])


def new_state():
    return State(list(range(SIZE)), 0, 0)


def reverse_move_increase(state, length):
    l, pos, skip = state
    indices = [i % SIZE for i in range(pos, pos + length)]
    m = l[:]
    for i, j in zip(indices, reversed(indices)):
        l[i] = m[j]
    pos = (pos + length + skip) % SIZE
    skip += 1
    return State(l, pos, skip)


# part 1
state = new_state()
with open('10.input') as f:
    lengths = [int(word) for word in f.read().rstrip().split(',')]
for length in lengths:
    state = reverse_move_increase(state, length)
print(state.l[0] * state.l[1])

# part 2
state = new_state()
with open('10.input') as f:
    lengths = [ord(c) for c in f.read().rstrip()] + [17, 31, 73, 47, 23]
for n in range(64):
    for length in lengths:
        state = reverse_move_increase(state, length)

dense = []
for i in range(0, SIZE, 16):
    v = 0
    for j in range(16):
        v ^= state.l[i + j]
    dense.append(v)
print(''.join('{0:02x}'.format(n) for n in dense))
