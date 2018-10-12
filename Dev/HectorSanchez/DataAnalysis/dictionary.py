############################################################################
# Dictionary (Hash Map)
############################################################################

dict={
"a":"value",
"b":[1,2,3]
}
dict[7]="Inserting"
dict["b"]
dict[5]="some value"
"b" in dict
dict["dummy"]="another value"
print(dict)

del dict[5]
dict
retValue=dict.pop("dummy")
retValue
print(dict)
list(dict.keys())
list(dict.values())

dictTemp={"b":1,"c":3}
dict.update(dictTemp)
dict

mapping=zip(
    range(5),
    reversed(range(5))
)
dict(mapping)


words=["apple","bat","bar","atom","book"]
byLetter={}
for word in words:
    letter=word[0]
    if letter not in byLetter:
        byLetter[letter] = [word]
    else:
        byLetter[letter].append(word)
print(byLetter)

byLetter={}
for word in words:
    letter = word[0]
    byLetter.setdefault(letter,[]).append(word)
print(byLetter)

from collections import defaultdict
byLetter=defaultdict(list)
for word in words:
    byLetter[word[0]].append(word)
print(byLetter)

hash("Test String")
hash((1,2,3))
hash([1,2,3])
