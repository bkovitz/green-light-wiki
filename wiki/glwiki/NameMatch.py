from UnsmashWords import unsmashWords


def bestName(names, target):
    best = target
    unsmashedTarget = unsmashWords(target)

    for name in names:
        if name == target:
            return name

        if name == unsmashedTarget:
            best = name
            continue

        if unsmashWords(name) == unsmashedTarget:
            best = name
            continue

    return best
