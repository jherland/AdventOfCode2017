class Coord:
    @classmethod
    def parse(cls, s):
        assert s.startswith('<')
        x, y, z = s[1:].split('>', 1)[0].split(',')
        return cls(int(x), int(y), int(z))

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '<{0.x},{0.y},{0.z}>'.format(self)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(a, b):
        return a.x == b.x and a.y == b.y and a.z == b.z

    def distance(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def parse_file(f):
    for part, line in enumerate(f):
        p_, p, v, a = line.rstrip().split('=')
        assert p_ == 'p'
        assert p.endswith(', v')
        assert v.endswith(', a')
        yield part, Coord.parse(p), Coord.parse(v), Coord.parse(a)


def tick(particles):
    ret = []
    positions = {}  # pos -> n
    collisions = set()  # n for collided particles
    for n, pos, vel, acc in particles:
        vel += acc
        pos += vel
        if pos in positions:  # collision
            collisions.add(n)
            collisions.add(positions[pos])
        else:
            positions[pos] = n
        ret.append((n, pos, vel, acc))
    if collisions:
        print('***', collisions)
    return [p for p in ret if p[0] not in collisions]


with open('20.input') as f:
    particles = list(parse_file(f))

origo = Coord(0, 0, 0)

# part 1
n = 0
try:
    while True:
        dists = [pos.distance(origo) for _, pos, _, _ in particles]
        if n % 100 == 0:
            print(len(particles), 'left')
            print(min(particles, key=lambda part: part[1].distance(origo)))
        n += 1
        particles = tick(particles)
except KeyboardInterrupt:
    pass
