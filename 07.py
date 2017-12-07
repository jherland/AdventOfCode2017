def parse_file():
    with open('07.input') as f:
        for line in f:
            name, weight, *children = line.split()
            assert weight.startswith('(') and weight.endswith(')')
            weight = int(weight[1:-1])
            assert children == [] or children[0] == '->'
            yield name, weight, [c.rstrip(',') for c in children[1:]]


# part 1
weights = {}
children = {}
parents = {}
for name, weight, childs in parse_file():
    weights[name] = weight
    children[name] = set(childs)
    for c in childs:
        assert c not in parents
        parents[c] = name

# find root
root = name  # any name
while root in parents:
    root = parents[root]
print(root)


# part 2
def fullweight(name):
    return weights[name] + sum(fullweight(c) for c in children[name])


def odd_one_out(items, key):
    counts = {}
    for item in items:
        counts.setdefault(key(item), []).append(item)
    assert len(counts) == 2, len(counts)
    _, a = counts.popitem()
    _, b = counts.popitem()
    if len(a) == 1:
        return a[0]
    else:
        assert len(b) == 1
        return b[0]


class ChildError(Exception):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


def find_imbalance(name):
    if name not in children:
        return
    cw = [(c, fullweight(c)) for c in children[name]]
    print(cw)
    try:
        odd = odd_one_out(cw, key=lambda item: item[1])
    except AssertionError:
        print('No more imbalance under here, must be {} itself?'.format(name))
        raise ChildError(name, weights[name])
    print(odd)
    try:
        find_imbalance(odd[0])
    except ChildError as e:
        print('Found imbalance in child: {}, {}'.format(e.name, e.weight))
        odd_fweight, other_fweight = 0, 0
        for c, fw, in cw:
            if c == e.name:
                odd_fweight = fw
            elif other_fweight == 0:
                other_fweight = fw
            else:
                assert other_fweight == fw
        print('Should be {}, but is {}'.format(other_fweight, odd_fweight))
        diff = other_fweight - odd_fweight
        print('Adjust {}: {} -> {}'.format(e.name, e.weight, e.weight + diff))


find_imbalance(root)
