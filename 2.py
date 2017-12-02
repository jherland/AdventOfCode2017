def rows(f):
    for line in f:
        if line.rstrip():
            yield [int(word) for word in line.split()]


def rowdiff(rows):
    for row in rows:
        yield max(row) - min(row)


def rowdivisor(rows):
    for row in rows:
        maxdiv = 1  # trivial result
        for a in row:
            for b in row:
                if a % b == 0:
                    maxdiv = max(maxdiv, a // b)
                elif b % a == 0:
                    maxdiv == max(maxdiv, b // a)
        yield maxdiv


# part 1
with open("2.input") as f:
    print(sum(rowdiff(rows(f))))

# part 2
with open("2.input") as f:
    print(sum(rowdivisor(rows(f))))
