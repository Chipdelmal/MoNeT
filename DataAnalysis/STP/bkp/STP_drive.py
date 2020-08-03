#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet


def driveSelector(id):
    if(id == drive_LDR.get('id')):
        return drive_LDR
    if(id == drive_LDS.get('id')):
        return drive_LDS


# #############################################################################
# Linked Drive
# #############################################################################
drive_LDR = {
        'id': 'LDR', 'folder': 'LDR', 'loc': 1,
        'HLT': monet.generateAggregationDictionary(
            ["H", "Other", "Total"],
            [
                [1, 4, 5, 6],
                [0, 2, 3, 7, 8, 9],
                [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]
            ]
        ),
        'ECO': monet.generateAggregationDictionary(
            ["H", "B", "R", "W", "Total"],
            [
                [1, 4, 4, 5, 6],
                [3, 6, 8, 9, 9],
                [2, 5, 7, 7, 8],
                [0, 0, 1, 2, 3],
                [1, 4, 4, 5, 6, 3, 6, 8, 9, 9, 2, 5, 7, 7, 8, 0, 0, 1, 2, 3]
            ]
        )
    }


# #############################################################################
# Linked Drive
# #############################################################################
drive_LDS = {
        'id': 'LDS', 'folder': 'LDR', 'loc': 1,
        'HLT': monet.generateAggregationDictionary(
            ["H", "Other", "Total"],
            [
                [1, 4, 5, 6],
                [0, 2, 3, 7, 8, 9],
                [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]
            ]
        ),
        'ECO': monet.generateAggregationDictionary(
            ["H", "B", "R", "W", "Total"],
            [
                [1, 4, 4, 5, 6],
                [3, 6, 8, 9, 9],
                [2, 5, 7, 7, 8],
                [0, 0, 1, 2, 3],
                [1, 4, 4, 5, 6, 3, 6, 8, 9, 9, 2, 5, 7, 7, 8, 0, 0, 1, 2, 3]
            ]
        )
    }
