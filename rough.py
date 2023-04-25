
def chlist(s):
    checklist = set()
    substring = ""
    running = ""
    r_count = 0
    count = 0
    for i in s:
        if i in checklist:
            if r_count > count:
                count = r_count
                substring = running
                checklist.clear()
                checklist.add(i)
            r_count = 1
            running = i
        else:
            r_count += 1
            running += i
            checklist.add(i)
    print(substring)
    return count

s = "dvdf"
print(chlist(s))