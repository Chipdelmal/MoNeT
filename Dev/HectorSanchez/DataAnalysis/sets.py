############################################################################
# Sets
############################################################################

setA=set([2,2,2,1,3,3])
setB={2,2,2,1,3,3,6,2}
setA.union(setB)
setA | setB
setA.intersection(setB)
setA & setB

# In place
setC=setA.copy()
setC.intersection_update(setB)
setC
