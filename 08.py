from collections import defaultdict

registers = defaultdict(int)

incdec = {
    'inc': lambda reg, val: reg + val,
    'dec': lambda reg, val: reg - val,
}

compare = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
}


def execute(program, observer=None):
    for line in program:
        reg, inc, val, if_, cmp_reg, cmp_op, cmp_val = line.split()
        assert if_ == 'if'
        assert inc in incdec
        assert cmp_op in compare
        val = int(val)
        cmp_val = int(cmp_val)

        if compare[cmp_op](registers[cmp_reg], cmp_val):
            registers[reg] = incdec[inc](registers[reg], val)

        observer()


class Observer:
    def __init__(self):
        self.max = 0

    def __call__(self):
        self.max = max(self.max, max(registers.values()))


observer = Observer()
with open('08.input') as f:
    execute(f, observer)

# part 1
print(max(registers.values()))

# part 2
print(observer.max)
