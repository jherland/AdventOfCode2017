with open('01.input') as f:
    iv = f.read().strip()

# part 1
print(sum(int(a) for a, b in zip(iv, iv[-1] + iv) if a == b))

# part 2
print(sum(int(a) for a, b in zip(iv, iv[int(len(iv) / 2):] + iv) if a == b))
