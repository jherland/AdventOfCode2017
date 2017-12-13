def parse_file(f):
    for line in f:
        d, r = line.split(':')
        yield int(d), int(r.strip())


def cycle(n):
    assert n > 0
    while True:
        yield from range(n)
        yield from range(n-2, 0, -1)


def firewall(ranges):
    fw = {d: cycle(r) for d, r in ranges.items()}
    while True:
        yield {d: next(r) for d, r in fw.items()}


with open('13.input') as f:
    ranges = {d: r for d, r in parse_file(f)}
max_depth = max(ranges.keys())

# part 1
fw = firewall(ranges)
print(sum(i * ranges[i] for i in range(max_depth + 1) if next(fw).get(i) == 0))

# part 2
t, fw = 0, firewall(ranges)
packets = []
while True:
    packets = [t] + packets[:max_depth]
    state = next(fw)
    for d, p in enumerate(packets):
        if p is None:
            continue
        if state.get(d) == 0:  # caught
            packets[d] = None
    if packets[-1] is not None:  # survivor!
        print(packets[-1])
        break
    t += 1
