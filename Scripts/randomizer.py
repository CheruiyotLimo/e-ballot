import random


def randomizer():
    checked = set()
    user_list = 20
    rand_list = []

    while len(rand_list) < 3:
        rand = random.randint(21, 23)
        if rand in checked:
            continue
        else:
            checked.add(rand)
            rand_list.append(rand)

    return rand_list