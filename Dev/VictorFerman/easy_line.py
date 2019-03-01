line = open('line2.csv', 'w')
houses = 20
distance = 50
l2 = range(0,(houses*distance)+distance,distance)
for i in range(houses):
    res=""
    for j in range(houses-1):
        if(i>=j):
            res+=str(l2[i-j])+','
        else:
            res+=str(l2[j-i])+','
    else:
        res+=str(l2[(houses-1)-i])+'\n'
    line.write(res)
line.close()
