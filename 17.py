inp = int(open('17.input').read().strip())
buf, pos = [0], 0

# part 1
for n in range(1, 2018):
    pos = (pos + inp) % len(buf) + 1
    buf.insert(pos, n)
print(buf[(pos + 1) % len(buf)])

# part 2
for n in range(2018, 50000001):
    pos = (pos + inp) % n + 1
    if pos == 1:
        buf[1] = n
print(buf[1])
