#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet

# #############################################################################
# Linked Drive
# #############################################################################
drive_CRISPR = {
        'id': 'CRISPR', 'folder': 'CRISPR', 'loc': 1,
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
