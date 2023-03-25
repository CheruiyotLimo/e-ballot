import random


def randomizer():
    checked = set()
    user_list = 20
    rand_list = []

    while len(rand_list) < 4:
        rand = random.randint(21, 24)
        if rand in checked:
            continue
        else:
            checked.add(rand)
            rand_list.append(rand)

    return rand_list