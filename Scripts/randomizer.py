import random


# def randomizer(rand_list):
#     checked = set()
#     user_list = 20
#     rand_list = [14, 21, 22, 23, 24, 26, 27]
    
#     rand = random.shuffle(rand_list)[0]
#     rand_list.remove(rand)

#     # while len(rand_list) < 6:
#     #     rand = random.randint(21, 27)
#     #     if rand in checked:
#     #         continue
#     #     else:
#     #         checked.add(rand)
#     #         rand_list.append(rand)

#     return rand

def new_rand(applicants_list: list):
    rand_list = [1, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    random.shuffle(rand_list)
    return rand_list

# print(randomizer())