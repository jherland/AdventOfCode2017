from typing import Iterable, Set, Tuple


class Node:
    @classmethod
    def parse(cls, line: str):
        '''Parse lines like this: "padx (45) -> pbga, havc, qoyq".'''
        name, weight, *rest = line.split()
        assert weight.startswith('(') and weight.endswith(')')
        assert rest == [] or rest[0] == '->'
        return cls(name, int(weight[1:-1]), {c.rstrip(',') for c in rest[1:]})

    def __init__(self, name: str, weight: int, children: Set[str]) -> None:
        self.name = name
        self.weight = weight
        self.children = children

    def __contains__(self, other):
        return other.name in self.children


class Tree:
    @classmethod
    def parse(cls, f: Iterable[str]):
        def nodes():
            for line in f:
                yield Node.parse(line)
        return cls(nodes())

    def __init__(self, nodes: Iterable[Node]) -> None:
        self.nodes = {n.name: n for n in nodes}
        self.parents = {}
        for n in self.nodes.values():
            for c in n.children:
                self.parents[c] = n.name

    def root(self, node: str) -> str:
        '''Walk parents from given node up to its root.'''
        while node in self.parents:
            node = self.parents[node]
        return node

    def full_weight(self, node: str) -> int:
        '''Return weight of the given node and its children.'''
        n = self.nodes[node]
        return n.weight + sum(self.full_weight(c) for c in n.children)

    def find_odd_child(self, node: str) -> Tuple[str, int]:
        '''Find the one child whose full_weight differs from the other.

        Return the name of the child, and the adjustment needed to bring it
        into agreement with the other children.
        Return None if this node has no children, or no adjustment is needed.
        '''
        n = self.nodes[node]
        if not n.children:
            return None
        by_weight = sorted((self.full_weight(c), c) for c in n.children)
        assert len(by_weight) >= 3
        # first or last item is not like the others
        common = by_weight[1][0]
        assert all(w == common for w, _ in by_weight[2:-1])
        first, last = by_weight[0], by_weight[-1]
        if first[0] != common:
            assert last[0] == common
            return first[1], common - first[0]
        elif last[0] != common:
            return last[1], common - last[0]
        else:
            return None

    def find_imbalance(self, node: str) -> Tuple[str, int]:
        '''Descend from 'node' until the one odd node has been found.

        Return that node's name, and the weight adjustment that must be made
        to balance the tree rooted at 'node'. Return None if no imbalance is
        found in this tree.
        '''
        imbalance = self.find_odd_child(node)
        # print(node, imbalance)
        if imbalance is None:  # No imbalance in this part of the tree
            return None
        ret = self.find_imbalance(imbalance[0])  # Look further for imbalance
        return imbalance if ret is None else ret


with open('07.input') as f:
    tree = Tree.parse(f)

# part 1
root = tree.root(next(iter(tree.nodes.keys())))  # follow any node to the root
print(root)

# part 2
odd_node, adjustment = tree.find_imbalance(root)
print(tree.nodes[odd_node].weight + adjustment)
