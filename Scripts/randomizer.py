import random

def randomn():
    return random.randint(1, 10)


def randomizer(list1):
    checker = set()
    for i in range(len(list1)):
        r = random.choice(list1)
        if r not in checker:
            checker.add(r)
            print(r)

# print(randomn())
randomizer([1, 2, 3, 4, 6, 5, 7, 8, 9])