def get_corners(fileName):
    lats = []
    longs = []
    clusterData = open(fileName, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (lat, long) = (float(tokens[1]), float(tokens[0]))
        lats.append(lat)
        longs.append(long)

    minLat = min(lats)
    minLong = min(longs)
    maxLat = max(lats)
    maxLong = max(longs)
    return [[minLong, maxLong], [minLat, maxLat]]
