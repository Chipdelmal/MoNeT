#Author: vferman
#Creates a dataset from the CalSurv Data, adapted from the previous parser to deal with the new structure
from datetime import date
import trapinfo
import sys
import matplotlib
import matplotlib.pyplot as plt
import math
from mpl_toolkits.basemap import Basemap

def parseTrapInfo(filename):
    trapFile = open(filename)
    minLat = 0
    minLong = 0
    maxLat = 0
    maxLong = 0
    trapDict = {}
    next(trapFile)
    id = 1
    allNLats = []
    allNLongs = []
    allELats = []
    allELongs = []
    for line in trapFile:
        tokens = line.split(',')
        long = float(tokens[0])
        lat = float(tokens[1])
        type = tokens[2]
        dateStr = tokens[3].split('/')
        count = tokens[7]
        month = int(dateStr[0])
        day = int(dateStr[1])
        year = 2000 + int(dateStr[2])
        trapDate = date(year,month,day)
        (_,week,_) = trapDate.isocalendar()
        if id == 1:
            minLat = lat
            minLong = long
            maxLat = lat
            maxLong = long
            id+=1

        if year not in trapDict:
            trapDict[year]={}

        if week not in trapDict[year]:
            trapDict[year][week]={'egg':[],'normal':[]}
            trapDict[year][week]['month'] = trapDate.strftime("%B")

        if 'OVI' in type:
            allELats.append(lat)
            allELongs.append(long)
            trapDict[year][week]['egg'].append((long,lat,int(count)))
        else:
            allNLats.append(lat)
            allNLongs.append(long)
            trapDict[year][week]['normal'].append((long,lat,int(count)))

        if lat <minLat:
            minLat = lat
        elif lat > maxLat:
            maxLat = lat
        else:
            pass

        if long <minLong:
            minLong = long
        elif long > maxLong:
            maxLong = long
        else:
            pass

    trapFile.close()
    id = 1
    for year in range(2013,2019):
        if year not in trapDict:
            continue

        for week in range(1,53):
            if week not in trapDict[year]:
                continue

            nlongs = [x[0] for x in trapDict[year][week]['normal']]
            nlats = [x[1] for x in trapDict[year][week]['normal']]
            ncounts = [int(math.sqrt(x[2])) for x in trapDict[year][week]['normal']]
            egglongs = [x[0] for x in trapDict[year][week]['egg']]
            egglats = [x[1] for x in trapDict[year][week]['egg']]
            eggcounts = [int(math.sqrt(x[2])*0.5)+1 for x in trapDict[year][week]['egg']]

            fig, ax = plt.subplots()
            m = Basemap(projection='merc',llcrnrlat=minLat-0.1,urcrnrlat=maxLat+0.1,llcrnrlon=minLong-0.1,urcrnrlon=maxLong+0.1,lat_ts=20,resolution='i')
            m.drawcounties(linewidth=0.3)

            m.scatter(allNLongs, allNLongs, latlon=True, marker='.', c='#EFEFEF', s=1)
            m.scatter(allELongs, allELats, latlon=True, marker='^', c='#EFEFEF', s=1)
            m.scatter(nlongs, nlats, latlon=True, marker='.', c='blue', s=ncounts)
            m.scatter(egglongs, egglats, latlon=True, marker='^', c='red', s=eggcounts)
            ax.text(1000,10000, str(year)+' '+trapDict[year][week]['month'])
            plt.savefig("./Cal_"+ str(id).zfill(5)+ ".png",
                        dpi=1024, facecolor='w',
                        edgecolor='w', orientation='portrait', papertype=None,
                        format="png", transparent=False, bbox_inches='tight',
                        pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            id+=1

    return


def main():
    clArguments=sys.argv[1:]
    trapFile = clArguments[0]
    parseTrapInfo(trapFile)

main()
