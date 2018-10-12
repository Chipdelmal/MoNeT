
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
