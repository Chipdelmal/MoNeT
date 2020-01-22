#!/usr/bin/python
# -*- coding: utf-8 -*-

import aux


def experimentSelector(args):
    # Device
    if args.dev == 0:
        ROOT = '/Volumes'
    else:
        ROOT = '/RAID5'
    # Landscape
    if args.land == 0:
        LAND = 'Comoros'
    else:
        LAND = 'STP'
    # Selected IDs
    return (ROOT, LAND)


def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time):
    print(
            aux.CWHT + '\nUCI Experiments Analysis ' +
            '[' + time + ']' + aux.CEND
        )
    print(aux.CRED + 'Root  PATH: ' + PATH_ROOT + aux.CEND)
    print(aux.CRED + 'Image PATH: ' + PATH_IMG + aux.CEND)
    print(aux.CRED + 'Data  PATH: ' + PATH_DATA + aux.CEND)
    print(aux.PAD)
