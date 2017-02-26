def unique_integer_key(dictionary: dict) -> int:
    prev = 0
    for uid in sorted(dictionary.keys()):
        if uid - prev != 1:
            return uid - 1
        prev = uid
    return prev + 1
