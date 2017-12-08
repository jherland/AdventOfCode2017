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

any_max = 0


def execute(program):
    for line in program:
        reg, inc, val, if_, cmp_reg, cmp_op, cmp_val = line.split()
        assert if_ == 'if'
        assert inc in incdec
        assert cmp_op in compare
        val = int(val)
        cmp_val = int(cmp_val)

        if compare[cmp_op](registers[cmp_reg], cmp_val):
            registers[reg] = incdec[inc](registers[reg], val)

        global any_max
        any_max = max(any_max, max(registers.values()))


with open('08.input') as f:
    execute(f)

# part 1
print(max(registers.values()))

# part 2
print(any_max)
