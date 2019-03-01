import numpy as np
import matplotlib.pyplot as plt

def distance(p1,p2):
    dX = p1[0]-p2[0]
    dY = p1[1]-p2[1]
    return np.hypot(dX,dY)


sides = 10
radius = 20
points = []
angles = (2*np.pi)/sides
xList = []
yList = []
cords = open(str(sides)+'_'+str(radius)+'_ring_coords.csv', 'w')
for i in range(sides):
    x = radius*np.sin(i*angles)
    y = radius*np.cos(i*angles)
    xList.append(x)
    yList.append(y)
    points.append((x,y))
    cords.write(str(x)+','+str(y)+'\n')

outFile = open(str(sides)+'_'+str(radius)+'_ring.csv', 'w')
for i in range(sides):
    res=""
    for j in range(sides-1):
        res += str(distance(points[i],points[j]))+','
    else:
        res+=str(distance(points[i],points[-1]))+'\n'
    outFile.write(res)
outFile.close()

fig, ax = plt.subplots()
ax.scatter(xList, yList, marker='s')
plt.savefig(str(sides)+'_'+str(radius)+ "_ring.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=False, bbox_inches='tight',
            pad_inches=0.05, frameon=None)
plt.close(fig)
plt.close('all')
