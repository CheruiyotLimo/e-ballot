import random


def randomizer():
    checked = set()
    user_list = 10

    while len(checked) < user_list:
        rand = random.randint(1, user_list)
        if rand in checked:
            continue
        else:
            checked.add(rand)
            yield rand