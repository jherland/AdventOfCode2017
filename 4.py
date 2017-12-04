def phrases():
    with open('4.input') as f:
        for line in f:
            yield line.split()


def no_repeats(phrase):
    return len(set(phrase)) == len(phrase)


def no_anagrams(phrase):
    sorted_words = [str(sorted(w)) for w in phrase]
    return len(sorted_words) == len(set(sorted_words))


# part 1
print(len([p for p in phrases() if no_repeats(p)]))

# part 2
print(len([p for p in phrases() if no_anagrams(p)]))
