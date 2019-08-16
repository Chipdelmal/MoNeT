#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os

def writeLatLongsToFileWithID(latlongs, path):
    with open(path, 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(['ID', 'Latitude', 'Longitude'])
        for (i, row) in enumerate(latlongs):
            writer.writerow([i, row[0], row[1]])
    return True


def createFolder(path):
    try:
        os.mkdir(path)
    except OSError:
        pass
