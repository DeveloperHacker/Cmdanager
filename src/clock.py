def expand(clock: float):
    clock = int(clock * 1000)
    ms = clock % 1000
    s = clock // 1000 % 60
    m = clock // 1000 // 60 % 60
    h = clock // 1000 // 60 // 60
    return h, m, s, ms
