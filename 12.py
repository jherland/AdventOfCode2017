def parse_conns(f):
    for line in f:
        node, arrow, conns = line.rstrip().split(' ', 2)
        assert arrow == '<->'
        yield int(node), set(int(c.rstrip(',')) for c in conns.split(' '))


def find_group(node, connections):
    seen, new = set(), {node}
    while new:
        seen, new = seen | new, {c for n in new - seen for c in connections[n]}
    return seen


def main():
    # part 1
    with open('12.input') as f:
        connections = {node: conns for node, conns in parse_conns(f)}
    group = find_group(0, connections)
    print(len(group))

    # part 2
    groups = 1
    connections = {k: v for k, v in connections.items() if k not in group}
    while connections:
        group = find_group(next(iter(connections.keys())), connections)
        connections = {k: v for k, v in connections.items() if k not in group}
        groups += 1
    print(groups)


if __name__ == '__main__':
    main()
