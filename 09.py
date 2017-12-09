def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


@coroutine
def char_source(target):
    with open('09.input') as f:
        for char in f.read().rstrip():
            target.send(char)
    target.send(chr(0))  # end marker
    (yield)


@coroutine
def parse_groups(target):
    level = 0
    while True:  # Outer loop looking for groups
        c = (yield)
        if c == '{':  # start group
            level += 1
            target.send(('group', level))  # new group at this level
        elif c == '}':  # end group
            level -= 1
        elif c == ',':  # separator
            pass
        elif c == '<':  # start garbage
            while True:  # Inner loop, looking for garbage end
                c = (yield)
                if c == '!':  # ignore next char
                    c = (yield)
                elif c == '>':  # end garbage
                    break
                else:
                    target.send(('garbage', 1))  # more garbage
        elif c == chr(0):  # end
            target.send(('end', None))
        else:
            raise ValueError(c)


@coroutine
def collect_events():
    score = 0
    garbage = 0
    while True:
        event, value = (yield)
        if event == 'group':
            score += value
        elif event == 'garbage':
            garbage += value
        elif event == 'end':
            print('score = {}'.format(score))
            print('garbage = {}'.format(garbage))
        else:
            raise ValueError(event, value)


char_source(parse_groups(collect_events()))
