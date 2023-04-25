import random


def randomizer():
    checked = set()
    user_list = 20
    rand_list = [14, 21, 22, 23, 24, 26, 27]

    while len(rand_list) < 6:
        rand = random.randint(21, 27)
        if rand in checked:
            continue
        else:
            checked.add(rand)
            rand_list.append(rand)

    return rand_list

print(randomizer())