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

    def __str__(self):
        return '<{0.x},{0.y},{0.z}>'.format(self)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __len__(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)


class Particle:
    @classmethod
    def parse(cls, line):
        # line follows form: "p=<2366,784,-597>, v=<-12,-41,50>, a=<-5,1,-2>"
        p_, p, v, a = line.rstrip().split('=')
        assert p_ == 'p'
        assert p.endswith(', v')
        assert v.endswith(', a')
        return cls(Coord.parse(p), Coord.parse(v), Coord.parse(a))

    def __init__(self, pos, vel, acc):
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def __str__(self):
        return 'p={0.pos}, v={0.vel}, a={0.acc}'.format(self)

    def tick(self):
        '''Return this particle in the next time unit.'''
        vel = self.vel + self.acc
        pos = self.pos + vel
        return Particle(pos, vel, self.acc)

    def leaving(self):
        '''Return True iff this particle will never again approach <0,0,0>.'''
        next = self.tick()
        return len(next.pos) >= len(self.pos) \
            and len(next.vel) >= len(self.vel)


with open('20.input') as f:
    particles = {n: Particle.parse(line) for n, line in enumerate(f)}

# part 1:
# In the long term, the particle closest to <0,0,0> is the one with the
# smallest acceleration.
min_acc = min(len(p.acc) for p in particles.values())
minima = [n for n, p in particles.items() if len(p.acc) == min_acc]
if len(minima) > 1:  # Multiple minima, look at velocity also
    min_vel = min(len(particles[n].vel) for n in minima)
    minima = [n for n in minima if len(particles[n].vel) == min_vel]
assert len(minima) == 1
print(minima[0])

# part 2:
# Run simulation until no particles are approaching the origin
while not all(p.leaving() for p in particles.values()):
    # Find collisions
    space = {}  # pos: {n...}
    for n, p in particles.items():
        space.setdefault(p.pos, set()).add(n)
    dead = {n for ns in space.values() for n in ns if len(ns) > 1}

    # Tick all particles into next state
    particles = {n: p.tick() for n, p in particles.items() if n not in dead}
print(len(particles))
