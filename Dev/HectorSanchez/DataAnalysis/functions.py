############################################################################
# Functions
############################################################################

import re

def myFunction(x,y,z=1.5):
    if z>1:
        return z*(x+y)
    else:
        return z/(x+y)

myFunction(5,6,z=.7)
myFunction(3.14,7,3.5)
myFunction(10,20)
myFunction(x=1,y=2,z=3)

def f():
    a=5
    b=6
    c=7
    return a,b,c
i,j,k=f()
print(i,j,k)
returnValue=f()
print(returnValue)

def fDict():
    a=5
    b=6
    c=7
    return {"a":a,"b":b,"c":c}
dictionaryTemp=fDict()
dictionaryTemp["a"]

def cleanStrings(strings):
    result=[]
    for value in strings:
        value=value.strip()
        value=re.sub("[!#?]","",value)
        value=value.title()
        result.append(value)
    return result

states=[
    "    Alabama","Georgia","Georgia!","georgia",
    "FlOrida","shouth    Carolina###","West Virginia?"
]
cleanStrings(states)

def removePunctuation(string):
    return re.sub("[!#?]","",string)
cleanOperations=[str.strip,removePunctuation,str.title]

def cleanStrings(strings,operations):
    result=[]
    for value in strings:
        for function in operations:
            value=function(value)
        result.append(value)
    return result
cleanStrings(states,cleanOperations)
