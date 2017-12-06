def redistribute(banks):
    i, val = max(enumerate(banks), key=lambda t: t[1])
    banks[i], j = 0, (i + 1) % len(banks)
    while val:
        banks[j] += 1
        val -= 1
        j = (j + 1) % len(banks)


def repeat_until_same(banks, func):
    seen, rounds = set(), 0
    while tuple(banks) not in seen:
        seen.add(tuple(banks))
        rounds += 1
        func(banks)
    return rounds


with open('06.input') as f:
    banks = [int(word) for word in f.read().split()]

# part 1
print(repeat_until_same(banks, redistribute))

# part 2
print(repeat_until_same(banks, redistribute))
