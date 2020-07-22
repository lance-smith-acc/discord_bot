import json
from itertools import chain

# Open json file and append contents to array
input_file = open('banks.json')
json_array = json.load(input_file)
wordVault = []
for bank in json_array:
    wordVault.append(bank)
#####

# Using itertools chain to find a value in an array of arrays
word_to_find = "ass"
test1 = word_to_find in chain(*wordVault)

print(test1)

if(word_to_find in chain(*wordVault)):
    for bank in wordVault:
        if word_to_find in bank:
            print(wordVault.index(bank))
#####

# Splitting a string into an array
message = "This is a test message"
messageArr = message.lower().split(" ")

print(messageArr)

for word in messageArr:
    print(word)
#####

# Getting an index value of the sought after word
wordVault2 = [["A","B","C"],["D","test","E"],["F","G","H"]]

for word in messageArr:
    if word.lower() in chain(*wordVault2):
        for bank in wordVault2:
            if word.lower() in bank:
                print(wordVault2.index(bank))

if(word in chain(*wordVault2) for word in messageArr):
    print("Success")