Instructions = {'set', 'sub', 'mul', 'jnz'}


def parse_assembly(f):
    for line in f:
        instr, *args = line.split()
        assert instr in Instructions
        yield instr, args


def run(program, regs):
    pc = 0
    instr_count = dict.fromkeys(Instructions, 0)

    def get_val(s):
        try:
            return int(s)
        except ValueError:
            return regs[s]

    while 0 <= pc < len(program):
        instr, args = program[pc]
        instr_count[instr] += 1
        if instr == 'set':
            regs[args[0]] = get_val(args[1])
        elif instr == 'sub':
            regs[args[0]] -= get_val(args[1])
        elif instr == 'mul':
            regs[args[0]] *= get_val(args[1])
        elif instr == 'jnz':
            if get_val(args[0]) != 0:
                pc += get_val(args[1])
                continue
        pc += 1
    return instr_count


with open('23.input') as f:
    program = list(parse_assembly(f))

# part 1
regs = dict.fromkeys('abcdefgh', 0)
instr_count = run(program, regs.copy())
print(instr_count['mul'])

# part 2
# Analyze assembly to identify conditionals and loops:
# --:   set a 1                  # debug = False
# 01:   set b 84                 # b = 84
# 02:   set c b                  # c = 84
# 03:   jnz a 2                  # if debug:
# 04:   jnz 1 5                  #     goto 09
# 05:   mul b 100                #
# 06:   sub b -100000            # b = 108400
# 07:   set c b                  #
# 08:   sub c -17000             # c = 108400 + 17000
# 09:       set f 1              # flag = True
# 00:       set d 2              # d = 2
# 11:           set e 2          # e = 2
# 12:               set g d      #
# 13:               mul g e      #
# 14:               sub g b      #
# 15:               jnz g 2      # if d * e == b:
# 16:                   set f 0  #     flag = False
# 17:               sub e -1     # e += 1
# 18:               set g e      #
# 19:               sub g b      # if e != b:
# 20:               jnz g -8     #     goto 12
# 21:           sub d -1         # d += 1
# 22:           set g d          #
# 23:           sub g b          # if d != b:
# 24:           jnz g -13        #     goto 11
# 25:       jnz f 2              # if !flag:
# 26:       sub h -1             #     h += 1
# 27:       set g b              #
# 28:       sub g c              #
# 29:       jnz g 2              # if b == c:
# 30:           jnz 1 3          #     exit!
# 31:       sub b -17            # b += 17
# 32:       jnz 1 -23            # goto 09

# Rewrite assembly into equivalent python with inner loop optimized:
debug = False
b = 84
c, d, e, h = b, 0, 0, 0
if not debug:
    b = 100000 + b * 100  # 108400
    c = b + 17000
while b <= c:
    flag, d = False, 2
    while d < b:
        if b % d == 0:
            flag = True
            break
        d += 1
    if flag:
        h += 1
    b += 17
print(h)
