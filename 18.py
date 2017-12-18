from collections import defaultdict


def parse_assembly(f):
    for line in f:
        instr, *args = line.split()
        assert instr in {'snd', 'set', 'add', 'mul', 'mod', 'rcv', 'jgz'}
        yield instr, args


def thread(program, pid=0):
    outbox = []
    sent = 0
    pc = 0
    regs = defaultdict(lambda: 0)
    regs['p'] = pid

    def get_val(s):
        try:
            return int(s)
        except ValueError:
            return regs[s]

    def do_instruction(instr, args):
        nonlocal pc, outbox, sent
        if instr == 'snd':
            outbox.append(get_val(args[0]))
            sent += 1
        elif instr == 'set':
            regs[args[0]] = get_val(args[1])
        elif instr == 'add':
            regs[args[0]] += get_val(args[1])
        elif instr == 'mul':
            regs[args[0]] *= get_val(args[1])
        elif instr == 'mod':
            regs[args[0]] %= get_val(args[1])
        elif instr == 'rcv':
            regs[args[0]] = yield outbox
            outbox = []
        elif instr == 'jgz':
            if get_val(args[0]) > 0:
                pc += get_val(args[1])
                return
        pc += 1

    while True:
        if pc < 0 or pc >= len(program):
            raise RuntimeError('PC out of bounds: {}'.format(pc))
        try:
            yield from do_instruction(*program[pc])
        except GeneratorExit:
            print(sent)
            raise


with open('18.input') as f:
    program = list(parse_assembly(f))

# part 1
print(next(thread(program))[-1])

# part 2
coros = [thread(program, n) for n in range(2)]
queues = [[None] for _ in range(len(coros))]  # Initial values to pass to coros
while any(queues):
    for coro, q, next_q in zip(coros, queues, queues[1:] + [queues[0]]):
        next_q.extend(coro.send(q.pop(0)) if q else [])
coros[-1].close()
