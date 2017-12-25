States = {  # state machine: state -> read -> (write, move, next_state)
    'A': ((1, +1, 'B'), (0, -1, 'C')),
    'B': ((1, -1, 'A'), (1, +1, 'D')),
    'C': ((1, +1, 'A'), (0, -1, 'E')),
    'D': ((1, +1, 'A'), (0, +1, 'B')),
    'E': ((1, -1, 'F'), (1, -1, 'C')),
    'F': ((1, +1, 'D'), (1, +1, 'A')),
}
tape, state, pos = {}, 'A', 0
for _ in range(12173597):
    tape[pos], move, state = States[state][tape.get(pos, 0)]
    pos += move
print(sum(tape.values()))
