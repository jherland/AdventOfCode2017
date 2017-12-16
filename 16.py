def spin(s, n):
    return s[-n:] + s[:-n]


def exchange(s, pos_a, pos_b):
    a, b = min(pos_a, pos_b), max(pos_a, pos_b)
    return s[:a] + s[b] + s[a + 1:b] + s[a] + s[b + 1:]


def partner(s, a, b):
    return s.replace(a, '?').replace(b, a).replace('?', b)


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
        dancers = move(dancers, *args)
    return dancers


dancers = 'abcdefghijklmnop'
with open('16.input') as f:
    moves = list(parse_moves(f.read().rstrip()))

# part 1
dancers = dance(dancers, moves)
print(dancers)

# part 2
n, repeat = 1, dancers
while n < 1000000000:
    dancers = dance(dancers, moves)
    if dancers == repeat:
        print('found repeat after {} dances'.format(n))
        period = n
        while n < 1000000000 - period:
            n += period
    n += 1
assert n == 1000000000
print(dancers)
