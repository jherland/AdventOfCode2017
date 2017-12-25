with open('25.input') as f:
    begin, steps, state, value, states = None, None, None, None, {}
    for line in f:
        if line.startswith('Begin in state '):
            begin = line[15]
        elif line.startswith('Perform a diagnostic checksum after '):
            steps = int(line[36:].split(' ')[0])
        elif line.startswith('In state '):
            state = line[9]
            states[state] = [[None, None, None], [None, None, None]]
        elif line.strip().startswith('If the current value is '):
            value = int(line.strip()[24])
            assert value in {0, 1}
        elif line.strip().startswith('- Write the value '):
            write = int(line.strip()[18])
            assert state and value in {0, 1} and write in {0, 1}
            states[state][value][0] = write
        elif line.strip().startswith('- Move one slot to the '):
            move = {'left.': -1, 'right.': +1}[line.strip()[23:]]
            assert state and value in {0, 1} and move
            states[state][value][1] = move
        elif line.strip().startswith('- Continue with state '):
            new = line.strip()[22]
            assert state and value in {0, 1} and new in 'ABCDEF'
            states[state][value][2] = new

tape, state, pos = {}, begin, 0
for _ in range(steps):
    tape[pos], move, state = states[state][tape.get(pos, 0)]
    pos += move
print(sum(tape.values()))
