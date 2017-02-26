def unique_integer_key(dictionary: dict) -> int:
    prev = 0
    for uid in sorted(dictionary.keys()):
        if uid - prev != 1:
            return uid - 1
        prev = uid
    return prev + 1


def expand(clock: float):
    clock = int(clock * 1000)
    ms = clock % 1000
    s = clock // 1000 % 60
    m = clock // 1000 // 60 % 60
    h = clock // 1000 // 60 // 60
    return h, m, s, ms
