import fiona
import numpy as np

def main():
    shape = fiona.open("/Users/vferman/MoNeT/Dev/VictorFerman/SHP/Buildings/Moroni/Moroni.shp", 'r')
    csvfile=open("/Users/vferman/MoNeT/Dev/VictorFerman/SHP/Buildings/Moroni/Moroni_latlongs.csv", 'w')
    #csvfile.write("latitude,longitude\n")
    for poligon in shape:
        building = poligon['geometry']['coordinates']
        lats = []
        longs = []
        for coordinateList in building:
            for (lat,long) in coordinateList:
                lats.append(float(lat))
                longs.append(float(long))
        meanLat = np.mean(lats)
        meanLong = np.mean(longs)
        csvfile.write(str(meanLat)+","+str(meanLong)+"\n")
    csvfile.close()
    shape.close()

main()
