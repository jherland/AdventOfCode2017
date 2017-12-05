def execute(jumps, inc_func):
    pos, steps = 0, 0
    while True:
        steps += 1
        offset = jumps[pos]
        if not 0 <= pos + offset < len(jumps):
            break
        jumps[pos] += inc_func(offset)
        pos += offset
    return steps


with open('05.input') as f:
    jumps = [int(line.rstrip()) for line in f]

# part 1
print(execute(jumps[:], lambda offset: 1))

# part 2
print(execute(jumps[:], lambda offset: 1 if offset < 3 else -1))
