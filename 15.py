def gen(start, factor, modulo, picky=1):
    while True:
        start = (start * factor) % modulo
        if start % picky == 0:
            yield start & 0xffff


with open('15.input') as f:
    a_start = int(f.readline().split()[-1])
    b_start = int(f.readline().split()[-1])

# part 1
a_gen = gen(a_start, 16807, 2147483647)
b_gen = gen(b_start, 48271, 2147483647)
print(sum(next(a_gen) == next(b_gen) for _ in range(40000000)))

# part 2
a_gen = gen(a_start, 16807, 2147483647, picky=4)
b_gen = gen(b_start, 48271, 2147483647, picky=8)
print(sum(next(a_gen) == next(b_gen) for _ in range(5000000)))
