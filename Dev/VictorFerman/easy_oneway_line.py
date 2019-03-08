fileOut = open('line3.csv', 'w')
houses = 10
distance = '50'
lines = []
for i in range(houses-1):
    res=['9999']*houses
    res[i] = '0'
    res[i+1] =distance
    lines.append(','.join(res))
else:
    res=res=['9999']*houses
    res[-1] = '0'
    res[0] =distance
    lines.append(','.join(res))

fileOut.write('\n'.join(lines))
fileOut.close()
