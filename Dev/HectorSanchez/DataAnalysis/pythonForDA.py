import numpy as np

# Creating a dictionary
data={
    i: np.random.rand() for i in range(7)
}
print(data)

# No copy, but reference
a=[1,2,3]
b=a
a.append(4)
print(b)

def appendElement(tempList,element):
    tempList.append(element)

data=[1,2,3]
appendElement(data,4)
print(data)
type(data)

a=5
isinstance(a,int)

#
iter("String")


# Modules
#import testModule
a = [1,2,3]
b=a
c=list(a)
a is b
a is c
a == c
a is None

# Mutable and immutable objects
aList=['foo',2,[4,5]]
aList[2]=1

aTuple=('foo',2,[4,5])
#aTuple[2]=1

# Scalar
None #Python's NULL

stringTest="""
this is a multi
line string
"""
stringTest.count('\n')

stringTestB="Testing as array"
stringTestB[2]
#stringTestB[2]="a"
stringConverted=str(100)
print(list(stringTestB))
stringTestB[:3]
stringTestB[3:]

s="12\\23"
print(s)

#raw string
s=r"testing\this\string"
print(s)

# Loops
total=0
sequence=[1,2,None,4,None,5]
for i in sequence:
    if i==None:
        continue
    total=total+i
print(total)

sequenceA=[1,2,0,4,6,5,2,1]
total=0
for i in sequenceA:
    if i==5:
        break
    total=total+i
print(total)

#Ternary
x=4
"Positive" if x>=0 else "Negative"

total=0
for i in range(9999):
    if (i % 3 == 0) or (i % 5 == 0):
        total=total+i
print(total)


# Tuples
nestedTuple=((4,5,6),(7,8))

tupleTemp=("foo",[1,2],True)
tupleTemp[1].append(4)
print(tupleTemp)
a,b,c=(1,2,3)
b
a,b,(c,d)=(1,2,(3,4))
c

seq=[(1,2,3),(4,5,6),(7,8,9)]
for a,b,c in seq:
    print("a={0},b={1},c={2}".format(a,b,c))

values=1,2,3,4,5
#a, b, *rest = values
a,b, *_=values

# Lists
bList=[2,3,4,1,2,3]
bList.append(10)
bList.insert(1,10)
print(bList)
bList.pop(2)
print(bList)
bList.remove(10)
print(bList)

bList.sort()
bList
cList=["saw","small","He","foxes"]
cList.sort(key=len)
cList

# Sorted insertion
import bisect
bisect.bisect(cList,2)
