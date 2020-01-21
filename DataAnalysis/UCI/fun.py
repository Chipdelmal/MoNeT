#!/usr/bin/python
# -*- coding: utf-8 -*-

import aux


def experimentSelector(args):
    # Device
    if args.dev == 0:
        ROOT = 'Volumes'
    else:
        ROOT = 'RAID5'
    # Landscape
    if args.land == 0:
        LAND = 'Comoros'
    else:
        LAND = 'STP'
    # Selected IDs
    return (ROOT, LAND)


def printExperimentHead(PATH_ROOT, PATH_IMG, time):
    print(aux.PAD)
    print(
            aux.CWHT + 'UCI Experiments Analysis ' +
            '[' + time + ']' + aux.CEND
        )
    print('* Root  PATH: ' + aux.CYEL + PATH_ROOT + aux.CEND)
    print('* Image PATH: ' + aux.CYEL + PATH_IMG + aux.CEND)
    print(aux.PAD)
