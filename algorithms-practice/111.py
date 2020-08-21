import numpy as  np
import pandas as pd
import itertools
import string

# 1)
basket1=['banana','kiwifruits','grapefruits','apples','apricots',
         'nectarines','oranges','peaches','pears','lemons']
basket2=['apples','grapes','apricots','dragonfruits','peaches',
         'pears','limes','papaya']
basket2 = list(set(basket2) - set(basket1))

len(basket2)
len(basket1)

# meanFruits = int((len(basket2)+len(basket1))/2)
# toTraspase = basket1[-(len(basket1)-meanFruits):]
# basket2.extend(toTraspase)
# del basket1[-(len(basket1)-meanFruits):]

while len(basket1) > len(basket2):
    toTransfer = basket1.pop()
    basket2.append(toTransfer)


# 2)
range_x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
range_y = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

prod = list(itertools.product(range_x, range_y))
myDict = {}
for i in prod:
    myDict[i] = i[0]**2 + i[1]**2

#3)
alphabet = string.ascii_lowercase *2

def encrypt(text,key):
    newText= []
    for i in range(len(text)):
        pos = alphabet.find(text[i])
        newText.append(alphabet[pos+key])
    return "".join(newText)
result = encrypt("abc",20)
result

#4)

myString = 'StRing ObJeCts haVe mANy inTEResting pROPerTies'
myList= myString.split(" ")

# for i in range(len(myList)):
#     if (i+1)%2 == 0: # if even
#         myList[i] = myList[i].upper()
#     else:
#         myList[i] = myList[i].lower()
#
# " ".join(myList)

" ".join([myList[i].upper() if ((i+1)%2==0) else myList[i].lower() for i in range(len(myList))])


# 5)
wlist = [['Python', 'creativity', 'universe'],
         ['interview', 'study', 'job', 'university', 'lecture'],
         ['task', 'objective', 'aim', 'subject', 'programming', 'test', 'research']]


output = []
for ilist in wlist:
    longestWord = ""
    longestPos = 0
    for pos, word in enumerate(ilist):
        if len(word)> len(longestWord):
            longestWord = word
            longestPos = pos+1
    output.append((ilist,longestPos,longestWord))
output
