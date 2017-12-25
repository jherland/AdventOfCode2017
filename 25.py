from collections import defaultdict

state = 'A'
steps = 12173597
states = {
    'A': ((1, +1, 'B'), (0, -1, 'C')),
    'B': ((1, -1, 'A'), (1, +1, 'D')),
    'C': ((1, +1, 'A'), (0, -1, 'E')),
    'D': ((1, +1, 'A'), (0, +1, 'B')),
    'E': ((1, -1, 'F'), (1, -1, 'C')),
    'F': ((1, +1, 'D'), (1, +1, 'A')),
}
tape = defaultdict(lambda: 0)
pos = 0


def one_step(pos, state):
    write, move, new = states[state][tape[pos]]
    tape[pos] = write
    return pos + move, new


def csum():
    return sum(tape.values())


for _ in range(steps):
    pos, state = one_step(pos, state)

print(csum())
