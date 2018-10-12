
seq=[1,2,3,4,3,10,4,5]
seq[2:5]
seq[3:]
seq[:3]
seq[::2]
seq[-1]
seq[:-1]
seq[::-1]

someList=["foo","bar","baz"]
mapping={}
for i,v in enumerate(someList):
    mapping[v]=i
mapping
enumerate(someList)

sorted([1,5,3,21,5])
sorted("horse race")

seq1=["foo","bar","baz"]
seq2=["one","two","three"]
zip(seq1,seq2)
seq3=[1,2]
zip(seq1,seq2,seq3)

for i,(a,b) in enumerate(zip(seq1,seq2)):
    stringFormat="{0}:{1},{2}"
    print(stringFormat.format(i,a,b))

pitchers=[("Nolan","Ryan"),("Roger","Clemens"),("Schilling","Curt")]
firstNames,lastNames=zip(*pitchers)
firstNames
lastNames

list(reversed(range(10)))

# Dict = Hash Map
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
