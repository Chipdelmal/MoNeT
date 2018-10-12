############################################################################
# Comprehensions
############################################################################

strings=["a","as","bat","car","dove","python"]
[x.upper() for x in strings if len(x)>2]

lengths={len(x) for x in strings}
lengths
set(map(len,strings))

{index:val for val,index in enumerate(strings)}

allData=[
    ["John","Emily","Michael","Mary","Steven"],
    ["Maria","Juan","Javier","Natalia","Pilar"]
]

namesOfInterest=[]
for names in allData:
    selected=[name for name in names if name.count("e")>=2]
    namesOfInterest.extend(selected)
namesOfInterest

[name for names in allData for name in names if name.count("e")>=2]


someTuples=[(1,2,3),(4,5,6),(7,8,9)]
flattened=[x for tup in someTuples for x in tup]
flattened

flattened=[]
for tup in someTuples:
    for x in tup:
        flattened.append(x)
print(flattened)
