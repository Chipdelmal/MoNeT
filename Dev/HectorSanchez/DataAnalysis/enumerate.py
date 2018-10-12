############################################################################
# Enumerate
############################################################################

collection=["a","b","c"]
for i,value in enumerate(collection):
    formatString="{0}:{1}"
    print(formatString.format(i,value))

tempList=["foo","bar","baz"]
mapping={}
for i,v in enumerate(tempList):
    mapping[i]=v
print(mapping)

sorted([3,5,1,2,5,8])
sorted("This is a test")

seqA=[1,2,3]
seqB=["A","b","c","d"]
zip(seqA,seqB)
seqC=[True,False]
zip(seqA,seqB,seqC)

for i,(a,b) in enumerate(zip(seqA,seqB)):
    formatString="{0}:{1},{2}"
    print(formatString.format(i,a,b))

pitchers=[("Nolan","Ryan"),("Roger","Clemens"),("Schilling","Curt")]
firstNames,lastNames=zip(*pitchers)
firstNames

list(reversed(range(10)))
