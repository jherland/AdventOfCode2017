from collections import defaultdict


def parse_assembly(f):
    for line in f:
        instr, *args = line.split()
        assert instr in {'snd', 'set', 'add', 'mul', 'mod', 'rcv', 'jgz'}
        yield instr, args


def snd(regs, val):
    try:
        return 'snd', int(val)
    except ValueError:
        return 'snd', regs[val]


def set_(regs, reg, val):
    try:
        regs[reg] = int(val)
    except ValueError:
        regs[reg] = regs[val]


def add(regs, reg, val):
    try:
        regs[reg] += int(val)
    except ValueError:
        regs[reg] += regs[val]


def mul(regs, reg, val):
    try:
        regs[reg] *= int(val)
    except ValueError:
        regs[reg] *= regs[val]


def mod(regs, reg, val):
    try:
        regs[reg] %= int(val)
    except ValueError:
        regs[reg] %= regs[val]


def rcv(regs, reg):
    assert reg in set('abcdefghijklmnopqrstuvwxyz')
    return 'rcv', reg


def jgz(regs, val, skip):
    try:
        val = int(val)
    except ValueError:
        val = regs[val]
    if val > 0:
        try:
            skip = int(skip)
        except ValueError:
            skip = regs[skip]
        return 'jump', skip


def run(program, pid):
    name = 't{}'.format(pid)
    instructions = {
        'snd': snd,
        'set': set_,
        'add': add,
        'mul': mul,
        'mod': mod,
        'rcv': rcv,
        'jgz': jgz,
    }
    pc = 0
    q = []
    regs = defaultdict(lambda: 0)
    regs['p'] = pid
    while True:
        if pc < 0 or pc >= len(program):
            raise RuntimeError('PC out of bounds: {}'.format(pc))
        instr, args = program[pc]
        ret = instructions[instr](regs, *args)
        print('{}: {}({}) -> {}'.format(name, instr, ', '.join(args), ret))
        if ret is not None:
            instr, val = ret
            if instr == 'snd':
                q.append((yield val))
            elif instr == 'rcv':
                incoming = None
                while incoming is None:
                    try:
                        incoming = q.pop(0)
                    except IndexError:
                        incoming = (yield None)
                regs[val] = incoming
                print('{}: ... received {} -> {}'.format(name, incoming, val))
            elif instr == 'jump':
                pc += val
                continue
            else:
                raise ValueError(ret)
        pc += 1


with open('18.input') as f:
    program = list(parse_assembly(f))

# part 1
# task = run(program, 0)
# val = None
# try:
#     while True:
#         val = task.send(val)
# except IndexError:
#     print(val)


# part 2
t0, t1 = run(program, 0), run(program, 1)

v0, v1 = None, None
progress = True
c0, c1 = 0, 0
retry = 3
while progress or retry:
    if not progress:
        retry -= 1
    v1, v0 = t0.send(v0), t1.send(v1)
    print('t0 -> {}, t1 -> {}, retry = {}'.format(v1, v0, retry))
    if v0 is not None:
        c1 += 1
    if v1 is not None:
        c0 += 1
    progress = not(v0 is None and v1 is None)

print(c0, c1)
