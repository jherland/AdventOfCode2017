def spin(dancers, n):
    for d in dancers:
        dancers[d] = (dancers[d] + n) % 16


def exchange(dancers, pos_a, pos_b):
    a, b = None, None
    for d, pos in dancers.items():
        if pos == pos_a:
            a = d
        elif pos == pos_b:
            b = d
    assert a and b
    dancers[a], dancers[b] = dancers[b], dancers[a]


def partner(dancers, a, b):
    dancers[a], dancers[b] = dancers[b], dancers[a]


def parse_moves(s):
    moves = s.split(',')
    for m in moves:
        if m[0] == 's':
            yield spin, int(m[1:])
        elif m[0] == 'x':
            a, b = m[1:].split('/')
            yield exchange, int(a), int(b)
        elif m[0] == 'p':
            a, b = m[1:].split('/')
            assert len(a) == 1 and len(b) == 1
            yield partner, a, b
        else:
            raise ValueError(m)


def dance(dancers, moves):
    for move, *args in moves:
        move(dancers, *args)


def print_dancers(dancers):
    for d in sorted(dancers, key=lambda d: dancers[d]):
        print(d, end='')
    print()


dancers = {chr(ord('a') + n): n for n in range(16)}
with open('16.input') as f:
    moves = list(parse_moves(f.read().rstrip()))

# part 1
dance(dancers, moves)
print_dancers(dancers)

# part 2
n, repeat = 1, dancers.copy()
while n < 1000000000:
    dance(dancers, moves)
    if dancers == repeat:
        print('found repeat after {} dances'.format(n))
        period = n
        while n < 1000000000 - period:
            n += period
    n += 1
assert n == 1000000000
print_dancers(dancers)
