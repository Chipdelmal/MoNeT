############################################################################
# Lists
############################################################################
import bisect

aList=[2,3,7,None]
tup=("foo","bar","baz")
bList=list(tup)
bList[1]="Peek"
bList

gen=range(10)
list(gen)

bList.append(11)
bList

# Computationally expensive
bList.insert(1,"test")
bList

bList.pop()
bList

# Computationally expensive
[4,"foo",10]+[1,2]
# Computationally lighter
bList.extend([0,1,0,1])


aList.sort()
aList

b=["saw","small","He","foxes","six"]
b.sort(key=len)
b

c=[1,2,2,2,3,4,7]
bisect.bisect(c,2)
bisect.bisect(c,5)
c

bisect.insort(c,6)
c


seq=[1,2,3,4,5,6,7,8,9]
seq[1:5]
seq[3:4]=[1,2]
seq

seq[:3]
seq[3:]

seq[:-2]
seq[-4:]
seq[-6:-2]
seq[::2]
seq[::-1]
