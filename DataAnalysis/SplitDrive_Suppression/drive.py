import MoNeT_MGDrivE as monet


def driveSelector(folder):
    if(folder == drive_CRISPR.get('folder')):   return drive_CRISPR;
    if(folder == drive_fsRIDL.get('folder')):   return drive_fsRIDL;
    if(folder == drive_IIT.get('folder')):      return drive_IIT;
    if(folder == drive_SIT.get('folder')):      return drive_SIT;
    if(folder == drive_SD.get('folder')):       return drive_SD;
    if(folder == drive_pgSIT.get('folder')):    return drive_pgSIT;
    if(folder == drive_autoShred.get('folder')):    return drive_autoShred;
    if(folder == drive_yShred.get('folder')):    return drive_yShred;

###############################################################################
# CRISPR
###############################################################################
drive_CRISPR = {
        'id': 'CRISPR', 'folder': 'CRISPR',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [[1, 4, 5, 6], [0, 2, 3, 7, 8, 9], [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]]
            ),
        'ECO': monet.generateAggregationDictionary(
                ["H", "B", "R", "W", "Total"],
                [
                    [1, 4, 4, 5, 6], [3, 6, 8, 9, 9],
                    [2, 5, 7, 7, 8], [0, 0, 1, 2, 3],
                    [1, 4, 4, 5, 6, 3, 6, 8, 9, 9, 2, 5, 7, 7, 8, 0, 0, 1, 2, 3]
                ]
            )
    }
###############################################################################
# fsRIDL
###############################################################################
drive_fsRIDL = {
        'id': 'fsRIDL', 'folder': 'fsRIDL',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [1, 2],
                    [0],
                    [0, 1, 2]
                ]
            ),
        'ECO': monet.generateAggregationDictionary(
                ["H", "W", "Total"],
                [[1, 2, 2], [0, 0, 1], [0, 0, 1, 1, 2, 2]]
            )
    }
###############################################################################
# IIT (Wolbachia)
###############################################################################
drive_IIT = {
        'id': 'IIT', 'folder': 'IIT',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [[0], [1], [0, 1]]
            ),
        'ECO': monet.generateAggregationDictionary(
                ["H", "W", "Total"],
                [[0], [1], [0, 1]]
            )
    }
###############################################################################
# SIT
###############################################################################
drive_SIT = {
        'id': 'SIT', 'folder': 'SIT',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [[1, 2], [0], [0, 1, 2]]
            ),
        'ECO': monet.generateAggregationDictionary(
                ["H", "W", "Total"],
                [[1, 2, 2], [0, 0, 1], [0, 0, 1, 1, 2, 2]]
            )
    }
###############################################################################
# Split Drive
###############################################################################
drive_SD = {
        'id': 'SD', 'folder': 'SplitDrive',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26],
                    [0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18, 19, 20, 22, 23, 27, 28, 29],
                    [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26, 0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18, 19, 20, 22, 23, 27, 28, 29]
                ]
            ),
        'ECO': monet.generateAggregationDictionary(
                ["H", "B", "R", "W", "C", "Total"],
                [
                    [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26],
                    [3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29],
                    [2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28],
                    [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23],
                    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29],
                    [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26, 3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29, 2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29]
                ]
            )
    }
###############################################################################
# pgSIT
###############################################################################
drive_pgSIT = {
        'id': 'pgSIT', 'folder': 'pgSIT',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [[1, 2], [0], [0, 1, 2]]
            ),
        'ECO': monet.generateAggregationDictionary(
                ["H", "W", "Total"],
                [[1, 2, 2], [0, 0, 1], [0, 0, 1, 1, 2, 2]]
            )
    }
###############################################################################
# Autosomal X-Shredder
###############################################################################
drive_autoShred = {
        'id': 'autoShred', 'folder': 'autosomalXShredder',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [1, 3, 4, 7, 9, 10, 13, 15, 16, 19, 21, 22, 25, 27, 28],
                    [0, 2, 5, 6, 8, 11, 12, 14, 17, 18, 20, 23, 24, 26, 29],
                    [
                        1, 3, 4, 7, 9, 10, 13, 15, 16, 19, 21, 22, 25, 27, 28,
                        0, 2, 5, 6, 8, 11, 12, 14, 17, 18, 20, 23, 24, 26, 29
                    ]
                ]
            ),
        'ECO': monet.generateAggregationDictionary(
                ['A', 'B', 'W', 'X', 'Y', 'R', 'Total'],
                [
                    [1, 3, 3, 4, 7, 9, 9, 10, 13, 15, 15, 16, 19, 21, 21, 22, 25, 27, 27, 28],
                    [2, 4, 5, 5, 8, 10, 11, 11, 14, 16, 17, 17, 20, 22, 23, 23, 26, 28, 29, 29],
                    [0, 0, 1, 2, 6, 6, 7, 8, 12, 12, 13, 14, 18, 18, 19, 20, 24, 24, 25, 26],
                    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23],
                    [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                    [6, 7, 8, 9, 10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 24, 25, 26, 27, 28, 29],
                    [
                        1, 3, 3, 4, 7, 9, 9, 10, 13, 15, 15, 16, 19, 21, 21, 22, 25, 27, 27, 28,
                        2, 4, 5, 5, 8, 10, 11, 11, 14, 16, 17, 17, 20, 22, 23, 23, 26, 28, 29, 29,
                        0, 0, 1, 2, 6, 6, 7, 8, 12, 12, 13, 14, 18, 18, 19, 20, 24, 24, 25, 26,
                        0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23,
                        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                        6, 7, 8, 9, 10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 24, 25, 26, 27, 28, 29
                    ]
                ]
            )
    }
###############################################################################
# Y-Linked X-Shredder
###############################################################################
drive_yShred = {
        'id': 'yShred', 'folder': 'ylinkedXShredder',
        'HLT': monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [[4, 7], [0, 1, 3, 5, 6, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8]]
            ),
        'ECO': monet.generateAggregationDictionary(
                ['A', 'B', 'X', 'Y', 'R', 'Total'],
                [
                    [4, 7],
                    [5, 8],
                    [0, 0, 1, 3, 4, 5],
                    [3, 6],
                    [1, 2, 2, 6, 7, 8],
                    [
                       4, 7, 5, 8, 0, 0, 1, 3, 4, 5,
                       3, 6, 1, 2, 2, 6, 7, 8
                    ]
                ]
            )
    }




###############################################################################
# Scratch code to get indices
###############################################################################
#
# #
# monet.autoGenerateGenotypesDictionary(
#     ['A', 'B', 'X', 'Y', 'R'],
#     ['XX','XR','RR','XY','XA','XB','RY','RA','RB']
# )
#
#
# # len(    [
# #         'WWXX','WAXX','WBXX','AAXX','ABXX','BBXX','WWXR','WAXR','WBXR','AAXR',
# #         'ABXR','BBXR','WWRR','WARR','WBRR','AARR','ABRR','BBRR','WWXY','WAXY',
# #         'WBXY','AAXY','ABXY','BBXY','WWRY','WARY','WBRY','AARY','ABRY','BBRY'
# #     ])
# #
# # list(range(0,29))
#
# monet.autoGenerateGenotypesDictionary(
#     ['A', 'B', 'W', 'X', 'Y', 'R'],
#     [
#         'WWXX','WAXX','WBXX','AAXX','ABXX','BBXX','WWXR','WAXR','WBXR','AAXR',
#         'ABXR','BBXR','WWRR','WARR','WBRR','AARR','ABRR','BBRR','WWXY','WAXY',
#         'WBXY','AAXY','ABXY','BBXY','WWRY','WARY','WBRY','AARY','ABRY','BBRY'
#     ]
# )
#
# {'genotypes': ['A', 'B', 'W', 'X', 'Y', 'R'], 'indices': [[1, 3, 3, 4, 7, 9, 9, 10, 13, 15, 15, 16, 19, 21, 21, 22, 25, 27, 27, 28], [2, 4, 5, 5, 8, 10, 11, 11, 14, 16, 17, 17, 20, 22, 23, 23, 26, 28, 29, 29], [0, 0, 1, 2, 6, 6, 7, 8, 12, 12, 13, 14, 18, 18, 19, 20, 24, 24, 25, 26], [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23], [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [6, 7, 8, 9, 10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 24, 25, 26, 27, 28, 29]]}

# monet.autoGenerateGenotypesDictionary(
# ["H", "B", "R", "W", "C"],
# ['WWWW','WWWH','WWWR','WWWB','WWHH','WWHR','WWHB','WWRR','WWRB','WWBB','WCWW','WCWH','WCWR','WCWB','WCHH','WCHR','WCHB','WCRR','WCRB','WCBB','CCWW','CCWH','CCWR','CCWB','CCHH','CCHR','CCHB','CCRR','CCRB','CCBB']
# )
