# 1)
doors = [False]*100
for i in range(100):
    for j in range(0,100,i+1):
        doors[j] = not doors[j]

# 2)
import numpy as np
import random

# task1
n= 1000
pardoned = 0

for rep in range(n):
    drawers = list(range(1,101))
    random.shuffle(drawers)
    found = 0
    for prisoner in range(1,101):
        for i in range(50):
            if prisoner == random.choice(drawers):
                found += 1
                break
    if found == 100:
        pardoned +=1

print(pardoned/n)


# task2
n=10000
pardoned=0

for rep in range(n):
    found=0
    drawers = list(range(1,101))
    random.shuffle(drawers)
    for nprisoner in range(1,101):
        n_to_try = nprisoner
        for ntry in range(50):
            if nprisoner == drawers[n_to_try-1]:
                found += 1
                break
            else:
                n_to_try = drawers[n_to_try-1]
    if found==100:
        pardoned+=1
print(pardoned/n)
