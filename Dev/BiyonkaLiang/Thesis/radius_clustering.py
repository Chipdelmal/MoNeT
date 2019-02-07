from random import random
import matplotlib.pyplot as plt
import numpy as np
import math

def rand_cluster(n,c,r):
    """
    Returns n random points in disk of radius r centered at c
    """

    x,y = c
    points = []
    for i in range(n):
        theta = 2*math.pi*random()
        s = r*random()
        points.append((x+s*math.cos(theta), y+s*math.sin(theta)))
    return points

def rand_clusters(k,n,r, a,b,c,d):
    """Return k clusters of n points each in random disks of radius r
    where the centers of the disk are chosen randomly in [a,b]x[c,d]"""
    clusters = []
    for _ in range(k):
        x = a + (b-a)*random()
        y = c + (d-c)*random()
        clusters.extend(rand_cluster(n,(x,y),r))
    return clusters

clusters = rand_clusters(4,50,0.1,0,1,0,1)
x, y = zip(*clusters)
plt.scatter(x, y,alpha=0.5)
plt.show()

def rand_cluster_one(n,c,r):
    """Returns n random points in disk of radius r centered at c"""
    x = c
    points = []
    for i in range(n):
        theta = 2*math.pi*random()
        s = r*random()
        points.append((x+s*math.cos(theta)))
    return points

def rand_clusters_one(k,n,r, a,b,c,d):
    """Return k clusters of n points each in random disks of radius r
    where the centers of the disk are chosen randomly in [a,b]x[c,d]"""
    clusters = []
    for _ in range(k):
        x = a + (b-a)*random()
        #y = c + (d-c)*random()
        clusters.extend(rand_cluster_one(n,x,r))
    return clusters

clusters1 = rand_clusters_one(4, 10, 0.01, 0, 1, 0, 1)
#x, y = zip(*clusters)
plt.scatter(clusters1, np.zeros((len(clusters1))),alpha=0.5)
plt.show()
