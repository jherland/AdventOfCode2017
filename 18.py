from collections import defaultdict


def parse_assembly(f):
    for line in f:
        instr, *args = line.split()
        assert instr in {'snd', 'set', 'add', 'mul', 'mod', 'rcv', 'jgz'}
        yield instr, args


class Thread:
    def __init__(self, program, pid):
        self.program = program
        self.pid = pid
        self.outbox = []
        self.sent = 0
        self.pc = 0
        self.regs = defaultdict(lambda: 0)
        self.regs['p'] = pid

    def __str__(self):
        return 'Thread {}'.format(self.pid)

    def _value(self, val):
        try:
            return int(val)
        except ValueError:
            return self.regs[val]

    def snd(self, val):
        self.outbox.append(self._value(val))
        self.sent += 1

    def set(self, reg, val):
        self.regs[reg] = self._value(val)

    def add(self, reg, val):
        self.regs[reg] += self._value(val)

    def mul(self, reg, val):
        self.regs[reg] *= self._value(val)

    def mod(self, reg, val):
        self.regs[reg] %= self._value(val)

    def rcv(self, reg):
        assert reg in set('abcdefghijklmnopqrstuvwxyz')
        return 'rcv', reg

    def jgz(self, val, skip):
        if self._value(val) > 0:
            return 'jump', self._value(skip)

    def __call__(self):
        while True:
            if self.pc < 0 or self.pc >= len(self.program):
                raise RuntimeError('PC out of bounds: {}'.format(self.pc))
            instr, args = self.program[self.pc]
            ret = getattr(self, instr)(*args)
            if ret is not None:
                instr, val = ret
                if instr == 'rcv':
                    self.regs[val] = yield self.outbox
                    self.outbox = []
                elif instr == 'jump':
                    self.pc += val
                    continue
                else:
                    raise ValueError(ret)
            self.pc += 1


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
thr0, thr1 = Thread(program, 0), Thread(program, 1)
t0, t1 = thr0(), thr1()
to0, to1 = [None], [None]  # Initial values to start off coroutines
while to0 or to1:
    to1.extend(t0.send(to0.pop(0)) if to0 else [])
    to0.extend(t1.send(to1.pop(0)) if to1 else [])
print(thr1.sent)
