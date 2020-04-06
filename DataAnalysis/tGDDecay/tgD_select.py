import MoNeT_MGDrivE as monet


def driveSelector(DRIVE, pathRoot):
    if DRIVE == 1:
        pathExt = "CRISPR/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "H", "R", "B", "G"],
            [
                [0, 0, 1, 2, 3],
                [1, 4, 4, 5, 6],
                [2, 5, 7, 7, 8],
                [3, 6, 8, 9, 9],
                []
            ]
        )
        yRange = 11000
    if DRIVE == 2:
        pathExt = "CRISPRX/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "H", "R", "B", "Y"],
            [
                [0, 0, 1, 2, 3, 4, 4, 8, 11, 13],
                [1, 5, 5, 6, 7, 8],
                [2, 6, 9, 9, 10, 11],
                [3, 7, 10, 12, 12, 13],
                []
            ]
        )
        yRange = 11000
    if DRIVE == 3:
        pathExt = "tGD/New/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["WA+WB", "H", "RA", "RB", "G"],
            [
                [
                    0, 5, 10, 15, 90, 95, 100, 155, 160, 195, 0, 1, 2, 3, 4, 5, 6, 7, 8,
                    9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24, 29, 34, 42, 47, 52,
                    59, 64, 69, 75, 80, 85, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                    101, 102, 103, 104, 109, 114, 122, 127, 134, 139, 145, 150, 155, 156,
                    157, 158, 159, 160, 161, 162, 163, 164, 169, 177, 184, 190, 195, 196,
                    197, 198, 199,
                    0, 1, 2, 3, 4, 20, 21, 22, 23, 24, 27, 29, 32, 34, 37, 39, 40, 41,
                    42, 43, 45, 47, 48, 50, 52, 53, 55, 57, 58, 59, 64, 69, 74, 75, 76,
                    77, 78, 80, 81, 82, 83, 85, 86, 87, 88, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 28,
                    30, 31, 33, 35, 36, 38, 39, 40, 41, 44, 46, 49, 51, 54, 56, 57, 58,
                    60, 61, 62, 63, 65, 66, 67, 68, 70, 71, 72, 73, 74, 79, 84, 89
                ],
                [
                    1, 6, 11, 16, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 60, 65, 70,
                    91, 96, 101, 105, 107, 109, 110, 112, 114, 115, 117, 135, 140, 156,
                    161, 165, 167, 169, 170, 172, 185, 196, 200, 202, 20, 21, 23, 25, 26,
                    28, 30, 31, 33, 35, 36, 38, 43, 48, 53, 76, 81, 86, 105, 106, 108,
                    110, 111, 113, 115, 116, 118, 123, 128, 146, 151, 165, 166, 168, 170,
                    171, 173, 178, 191, 200, 201, 203, 2, 7, 12, 17, 21, 26, 31, 36, 39,
                    40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 61, 66, 71, 92,
                    97, 102, 106, 111, 116, 119, 120, 122, 123, 124, 125, 127, 128, 129,
                    130, 136, 141, 157, 162, 166, 171, 174, 175, 177, 178, 179, 180, 186,
                    197, 201, 204, 205, 39, 41, 44, 46, 49, 51, 54, 56, 77, 82, 87, 119,
                    121, 124, 126, 129, 131, 147, 152, 174, 176, 179, 181, 192, 204, 206
                ],
                [
                    3, 8, 13, 18, 57, 59, 62, 64, 67, 69, 72, 93, 98, 103, 132, 134, 137,
                    139, 142, 158, 163, 182, 184, 187, 198, 207, 22, 27, 32, 37, 40, 45,
                    50, 55, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68, 70, 71, 72, 73, 78,
                    83, 88, 107, 112, 117, 120, 125, 130, 132, 133, 135, 136, 137, 138,
                    140, 141, 142, 143, 148, 153, 167, 172, 175, 180, 182, 183, 185, 186,
                    187, 188, 193, 202, 205, 207, 208, 4, 9, 14, 19, 23, 28, 33, 38, 41,
                    46, 51, 56, 58, 63, 68, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
                    84, 85, 86, 87, 88, 89, 94, 99, 104, 108, 113, 118, 121, 126, 131,
                    133, 138, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154,
                    159, 164, 168, 173, 176, 181, 183, 188, 189, 190, 191, 192, 193, 194,
                    199, 203, 206, 208, 209, 74, 79, 84, 89, 144, 149, 154, 189, 194, 209
                ],
                [
                    10, 11, 12, 13, 14, 30, 31, 33, 49, 51, 65, 66, 67, 68, 84, 96, 97,
                    98, 99, 111, 113, 126, 135, 136, 138, 155, 156, 157, 158, 159, 165,
                    166, 167, 168, 169, 172, 174, 175, 176, 177, 178, 180, 182, 183, 184,
                    189, 190, 191, 192, 193, 29, 32, 47, 48, 50, 64, 80, 81, 82, 83, 95,
                    109, 110, 112, 122, 123, 124, 125, 134, 137, 145, 146, 147, 148, 149,
                    155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
                    170, 171, 173, 174, 175, 176, 179, 181, 182, 183, 185, 186, 187, 188,
                    189, 194, 15, 16, 17, 18, 19, 35, 36, 38, 54, 56, 70, 71, 72, 73, 89,
                    100, 101, 102, 103, 104, 115, 116, 118, 129, 131, 140, 141, 142, 143,
                    154, 160, 161, 162, 163, 164, 170, 171, 173, 179, 181, 185, 186, 187,
                    188, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206,
                    207, 208, 209, 34, 37, 52, 53, 55, 69, 85, 86, 87, 88, 114, 117, 127,
                    128, 130, 139, 150, 151, 152, 153, 169, 172, 177, 178, 180, 184, 190,
                    191, 192, 193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205,
                    206, 207, 208, 209
                ],
                [
                    5, 6, 7, 8, 9, 25, 26, 28, 44, 46, 60, 61, 62, 63, 79, 90, 91, 92,
                    93, 94, 95, 105, 106, 107, 108, 109, 110, 112, 114, 117, 119, 120,
                    121, 122, 123, 124, 125, 127, 128, 130, 132, 133, 134, 137, 139, 144,
                    145, 146, 147, 148, 149, 150, 151, 152, 153, 24, 27, 42, 43, 45, 59,
                    75, 76, 77, 78, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102,
                    103, 104, 105, 106, 107, 108, 111, 113, 115, 116, 118, 119, 120, 121,
                    126, 129, 131, 132, 133, 135, 136, 138, 140, 141, 142, 143, 144, 154
                ]
            ]
        )
        yRange = 11000
    if DRIVE == 4:
        pathExt = "tGDX/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["WA+WB", "H", "RA", "RB", "G"],
            [
                [
                    0, 5, 10, 15, 90, 95, 100, 155, 160, 195, 210, 215, 220, 225, 0, 1,
                    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24,
                    29, 34, 42, 47, 52, 59, 64, 69, 75, 80, 85, 90, 91, 92, 93, 94, 95,
                    96, 97, 98, 99, 100, 101, 102, 103, 104, 109, 114, 122, 127, 134,
                    139, 145, 150, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 169,
                    177, 184, 190, 195, 196, 197, 198, 199, 210, 211, 212, 213, 214, 215,
                    216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229,
                    0, 1, 2, 3, 4, 20, 21, 22, 23, 24, 27, 29, 32, 34, 37, 39, 40, 41,
                    42, 43, 45, 47, 48, 50, 52, 53, 55, 57, 58, 59, 64, 69, 74, 75, 76,
                    77, 78, 80, 81, 82, 83, 85, 86, 87, 88, 210, 211, 212, 213, 214, 0,
                    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                    20, 21, 22, 23, 25, 26, 28, 30, 31, 33, 35, 36, 38, 39, 40, 41, 44,
                    46, 49, 51, 54, 56, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68, 70, 71,
                    72, 73, 74, 79, 84, 89, 210, 211, 212, 213, 214, 215, 216, 217, 218,
                    219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229
                ],
                [
                    1, 6, 11, 16, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 60, 65, 70,
                    91, 96, 101, 105, 107, 109, 110, 112, 114, 115, 117, 135, 140, 156,
                    161, 165, 167, 169, 170, 172, 185, 196, 200, 202, 211, 216, 221, 226,
                    20, 21, 23, 25, 26, 28, 30, 31, 33, 35, 36, 38, 43, 48, 53, 76, 81,
                    86, 105, 106, 108, 110, 111, 113, 115, 116, 118, 123, 128, 146, 151,
                    165, 166, 168, 170, 171, 173, 178, 191, 200, 201, 203, 2, 7, 12, 17,
                    21, 26, 31, 36, 39, 40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54,
                    55, 61, 66, 71, 92, 97, 102, 106, 111, 116, 119, 120, 122, 123, 124,
                    125, 127, 128, 129, 130, 136, 141, 157, 162, 166, 171, 174, 175, 177,
                    178, 179, 180, 186, 197, 201, 204, 205, 212, 217, 222, 227, 39, 41,
                    44, 46, 49, 51, 54, 56, 77, 82, 87, 119, 121, 124, 126, 129, 131,
                    147, 152, 174, 176, 179, 181, 192, 204, 206
                ],
                [
                    3, 8, 13, 18, 57, 59, 62, 64, 67, 69, 72, 93, 98, 103, 132, 134, 137,
                    139, 142, 158, 163, 182, 184, 187, 198, 207, 213, 218, 223, 228, 22,
                    27, 32, 37, 40, 45, 50, 55, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68,
                    70, 71, 72, 73, 78, 83, 88, 107, 112, 117, 120, 125, 130, 132, 133,
                    135, 136, 137, 138, 140, 141, 142, 143, 148, 153, 167, 172, 175, 180,
                    182, 183, 185, 186, 187, 188, 193, 202, 205, 207, 208, 4, 9, 14, 19,
                    23, 28, 33, 38, 41, 46, 51, 56, 58, 63, 68, 73, 74, 75, 76, 77, 78,
                    79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 94, 99, 104, 108, 113,
                    118, 121, 126, 131, 133, 138, 143, 144, 145, 146, 147, 148, 149, 150,
                    151, 152, 153, 154, 159, 164, 168, 173, 176, 181, 183, 188, 189, 190,
                    191, 192, 193, 194, 199, 203, 206, 208, 209, 214, 219, 224, 229, 74,
                    79, 84, 89, 144, 149, 154, 189, 194, 209
                ],
                [
                    10, 11, 12, 13, 14, 30, 31, 33, 49, 51, 65, 66, 67, 68, 84, 96, 97,
                    98, 99, 111, 113, 126, 135, 136, 138, 155, 156, 157, 158, 159, 165,
                    166, 167, 168, 169, 172, 174, 175, 176, 177, 178, 180, 182, 183, 184,
                    189, 190, 191, 192, 193, 220, 221, 222, 223, 224, 29, 32, 47, 48, 50,
                    64, 80, 81, 82, 83, 95, 109, 110, 112, 122, 123, 124, 125, 134, 137,
                    145, 146, 147, 148, 149, 155, 156, 157, 158, 159, 160, 161, 162, 163,
                    164, 165, 166, 167, 168, 170, 171, 173, 174, 175, 176, 179, 181, 182,
                    183, 185, 186, 187, 188, 189, 194, 15, 16, 17, 18, 19, 35, 36, 38,
                    54, 56, 70, 71, 72, 73, 89, 100, 101, 102, 103, 104, 115, 116, 118,
                    129, 131, 140, 141, 142, 143, 154, 160, 161, 162, 163, 164, 170, 171,
                    173, 179, 181, 185, 186, 187, 188, 194, 195, 196, 197, 198, 199, 200,
                    201, 202, 203, 204, 205, 206, 207, 208, 209, 225, 226, 227, 228, 229,
                    34, 37, 52, 53, 55, 69, 85, 86, 87, 88, 114, 117, 127, 128, 130, 139,
                    150, 151, 152, 153, 169, 172, 177, 178, 180, 184, 190, 191, 192, 193,
                    195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208,
                    209
                ],
                [
                    5, 6, 7, 8, 9, 25, 26, 28, 44, 46, 60, 61, 62, 63, 79, 90, 91, 92,
                    93, 94, 95, 105, 106, 107, 108, 109, 110, 112, 114, 117, 119, 120,
                    121, 122, 123, 124, 125, 127, 128, 130, 132, 133, 134, 137, 139, 144,
                    145, 146, 147, 148, 149, 150, 151, 152, 153, 215, 216, 217, 218, 219,
                    24, 27, 42, 43, 45, 59, 75, 76, 77, 78, 90, 91, 92, 93, 94, 96, 97,
                    98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 111, 113, 115,
                    116, 118, 119, 120, 121, 126, 129, 131, 132, 133, 135, 136, 138, 140,
                    141, 142, 143, 144, 154
                ]
            ]
        )
        yRange = 11000
    if DRIVE == 5:
        pathExt = "tGDCross/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["WA+WB", "H", "RA", "RB", "G"],
            [
                [
                    0, 5, 10, 15, 90, 95, 100, 155, 160, 195, 0, 1, 2, 3, 4, 5, 6, 7, 8,
                    9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24, 29, 34, 42, 47, 52,
                    59, 64, 69, 75, 80, 85, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                    101, 102, 103, 104, 109, 114, 122, 127, 134, 139, 145, 150, 155, 156,
                    157, 158, 159, 160, 161, 162, 163, 164, 169, 177, 184, 190, 195, 196,
                    197, 198, 199,
                    0, 1, 2, 3, 4, 20, 21, 22, 23, 24, 27, 29, 32, 34, 37, 39, 40, 41,
                    42, 43, 45, 47, 48, 50, 52, 53, 55, 57, 58, 59, 64, 69, 74, 75, 76,
                    77, 78, 80, 81, 82, 83, 85, 86, 87, 88, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 28,
                    30, 31, 33, 35, 36, 38, 39, 40, 41, 44, 46, 49, 51, 54, 56, 57, 58,
                    60, 61, 62, 63, 65, 66, 67, 68, 70, 71, 72, 73, 74, 79, 84, 89
                ],
                [
                    1, 6, 11, 16, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 60, 65, 70,
                    91, 96, 101, 105, 107, 109, 110, 112, 114, 115, 117, 135, 140, 156,
                    161, 165, 167, 169, 170, 172, 185, 196, 200, 202, 20, 21, 23, 25, 26,
                    28, 30, 31, 33, 35, 36, 38, 43, 48, 53, 76, 81, 86, 105, 106, 108,
                    110, 111, 113, 115, 116, 118, 123, 128, 146, 151, 165, 166, 168, 170,
                    171, 173, 178, 191, 200, 201, 203, 2, 7, 12, 17, 21, 26, 31, 36, 39,
                    40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 61, 66, 71, 92,
                    97, 102, 106, 111, 116, 119, 120, 122, 123, 124, 125, 127, 128, 129,
                    130, 136, 141, 157, 162, 166, 171, 174, 175, 177, 178, 179, 180, 186,
                    197, 201, 204, 205, 39, 41, 44, 46, 49, 51, 54, 56, 77, 82, 87, 119,
                    121, 124, 126, 129, 131, 147, 152, 174, 176, 179, 181, 192, 204, 206
                ],
                [
                    3, 8, 13, 18, 57, 59, 62, 64, 67, 69, 72, 93, 98, 103, 132, 134, 137,
                    139, 142, 158, 163, 182, 184, 187, 198, 207, 22, 27, 32, 37, 40, 45,
                    50, 55, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68, 70, 71, 72, 73, 78,
                    83, 88, 107, 112, 117, 120, 125, 130, 132, 133, 135, 136, 137, 138,
                    140, 141, 142, 143, 148, 153, 167, 172, 175, 180, 182, 183, 185, 186,
                    187, 188, 193, 202, 205, 207, 208, 4, 9, 14, 19, 23, 28, 33, 38, 41,
                    46, 51, 56, 58, 63, 68, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
                    84, 85, 86, 87, 88, 89, 94, 99, 104, 108, 113, 118, 121, 126, 131,
                    133, 138, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154,
                    159, 164, 168, 173, 176, 181, 183, 188, 189, 190, 191, 192, 193, 194,
                    199, 203, 206, 208, 209, 74, 79, 84, 89, 144, 149, 154, 189, 194, 209
                ],
                [
                    10, 11, 12, 13, 14, 30, 31, 33, 49, 51, 65, 66, 67, 68, 84, 96, 97,
                    98, 99, 111, 113, 126, 135, 136, 138, 155, 156, 157, 158, 159, 165,
                    166, 167, 168, 169, 172, 174, 175, 176, 177, 178, 180, 182, 183, 184,
                    189, 190, 191, 192, 193, 29, 32, 47, 48, 50, 64, 80, 81, 82, 83, 95,
                    109, 110, 112, 122, 123, 124, 125, 134, 137, 145, 146, 147, 148, 149,
                    155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
                    170, 171, 173, 174, 175, 176, 179, 181, 182, 183, 185, 186, 187, 188,
                    189, 194, 15, 16, 17, 18, 19, 35, 36, 38, 54, 56, 70, 71, 72, 73, 89,
                    100, 101, 102, 103, 104, 115, 116, 118, 129, 131, 140, 141, 142, 143,
                    154, 160, 161, 162, 163, 164, 170, 171, 173, 179, 181, 185, 186, 187,
                    188, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206,
                    207, 208, 209, 34, 37, 52, 53, 55, 69, 85, 86, 87, 88, 114, 117, 127,
                    128, 130, 139, 150, 151, 152, 153, 169, 172, 177, 178, 180, 184, 190,
                    191, 192, 193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205,
                    206, 207, 208, 209
                ],
                [
                    5, 6, 7, 8, 9, 25, 26, 28, 44, 46, 60, 61, 62, 63, 79, 90, 91, 92,
                    93, 94, 95, 105, 106, 107, 108, 109, 110, 112, 114, 117, 119, 120,
                    121, 122, 123, 124, 125, 127, 128, 130, 132, 133, 134, 137, 139, 144,
                    145, 146, 147, 148, 149, 150, 151, 152, 153, 24, 27, 42, 43, 45, 59,
                    75, 76, 77, 78, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102,
                    103, 104, 105, 106, 107, 108, 111, 113, 115, 116, 118, 119, 120, 121,
                    126, 129, 131, 132, 133, 135, 136, 138, 140, 141, 142, 143, 144, 154
                ]
            ]
        )
        yRange = 11000
    if DRIVE == 6:
        pathExt = "tGDXCross/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["WA+WB", "H", "RA", "RB", "G"],
            [
                [
                    0, 5, 10, 15, 90, 95, 100, 155, 160, 195, 210, 215, 220, 225, 0, 1,
                    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24,
                    29, 34, 42, 47, 52, 59, 64, 69, 75, 80, 85, 90, 91, 92, 93, 94, 95,
                    96, 97, 98, 99, 100, 101, 102, 103, 104, 109, 114, 122, 127, 134,
                    139, 145, 150, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 169,
                    177, 184, 190, 195, 196, 197, 198, 199, 210, 211, 212, 213, 214, 215,
                    216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229,
                    0, 1, 2, 3, 4, 20, 21, 22, 23, 24, 27, 29, 32, 34, 37, 39, 40, 41,
                    42, 43, 45, 47, 48, 50, 52, 53, 55, 57, 58, 59, 64, 69, 74, 75, 76,
                    77, 78, 80, 81, 82, 83, 85, 86, 87, 88, 210, 211, 212, 213, 214, 0,
                    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                    20, 21, 22, 23, 25, 26, 28, 30, 31, 33, 35, 36, 38, 39, 40, 41, 44,
                    46, 49, 51, 54, 56, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68, 70, 71,
                    72, 73, 74, 79, 84, 89, 210, 211, 212, 213, 214, 215, 216, 217, 218,
                    219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229
                ],
                [
                    1, 6, 11, 16, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 60, 65, 70,
                    91, 96, 101, 105, 107, 109, 110, 112, 114, 115, 117, 135, 140, 156,
                    161, 165, 167, 169, 170, 172, 185, 196, 200, 202, 211, 216, 221, 226,
                    20, 21, 23, 25, 26, 28, 30, 31, 33, 35, 36, 38, 43, 48, 53, 76, 81,
                    86, 105, 106, 108, 110, 111, 113, 115, 116, 118, 123, 128, 146, 151,
                    165, 166, 168, 170, 171, 173, 178, 191, 200, 201, 203, 2, 7, 12, 17,
                    21, 26, 31, 36, 39, 40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54,
                    55, 61, 66, 71, 92, 97, 102, 106, 111, 116, 119, 120, 122, 123, 124,
                    125, 127, 128, 129, 130, 136, 141, 157, 162, 166, 171, 174, 175, 177,
                    178, 179, 180, 186, 197, 201, 204, 205, 212, 217, 222, 227, 39, 41,
                    44, 46, 49, 51, 54, 56, 77, 82, 87, 119, 121, 124, 126, 129, 131,
                    147, 152, 174, 176, 179, 181, 192, 204, 206
                ],
                [
                    3, 8, 13, 18, 57, 59, 62, 64, 67, 69, 72, 93, 98, 103, 132, 134, 137,
                    139, 142, 158, 163, 182, 184, 187, 198, 207, 213, 218, 223, 228, 22,
                    27, 32, 37, 40, 45, 50, 55, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68,
                    70, 71, 72, 73, 78, 83, 88, 107, 112, 117, 120, 125, 130, 132, 133,
                    135, 136, 137, 138, 140, 141, 142, 143, 148, 153, 167, 172, 175, 180,
                    182, 183, 185, 186, 187, 188, 193, 202, 205, 207, 208, 4, 9, 14, 19,
                    23, 28, 33, 38, 41, 46, 51, 56, 58, 63, 68, 73, 74, 75, 76, 77, 78,
                    79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 94, 99, 104, 108, 113,
                    118, 121, 126, 131, 133, 138, 143, 144, 145, 146, 147, 148, 149, 150,
                    151, 152, 153, 154, 159, 164, 168, 173, 176, 181, 183, 188, 189, 190,
                    191, 192, 193, 194, 199, 203, 206, 208, 209, 214, 219, 224, 229, 74,
                    79, 84, 89, 144, 149, 154, 189, 194, 209
                ],
                [
                    10, 11, 12, 13, 14, 30, 31, 33, 49, 51, 65, 66, 67, 68, 84, 96, 97,
                    98, 99, 111, 113, 126, 135, 136, 138, 155, 156, 157, 158, 159, 165,
                    166, 167, 168, 169, 172, 174, 175, 176, 177, 178, 180, 182, 183, 184,
                    189, 190, 191, 192, 193, 220, 221, 222, 223, 224, 29, 32, 47, 48, 50,
                    64, 80, 81, 82, 83, 95, 109, 110, 112, 122, 123, 124, 125, 134, 137,
                    145, 146, 147, 148, 149, 155, 156, 157, 158, 159, 160, 161, 162, 163,
                    164, 165, 166, 167, 168, 170, 171, 173, 174, 175, 176, 179, 181, 182,
                    183, 185, 186, 187, 188, 189, 194, 15, 16, 17, 18, 19, 35, 36, 38,
                    54, 56, 70, 71, 72, 73, 89, 100, 101, 102, 103, 104, 115, 116, 118,
                    129, 131, 140, 141, 142, 143, 154, 160, 161, 162, 163, 164, 170, 171,
                    173, 179, 181, 185, 186, 187, 188, 194, 195, 196, 197, 198, 199, 200,
                    201, 202, 203, 204, 205, 206, 207, 208, 209, 225, 226, 227, 228, 229,
                    34, 37, 52, 53, 55, 69, 85, 86, 87, 88, 114, 117, 127, 128, 130, 139,
                    150, 151, 152, 153, 169, 172, 177, 178, 180, 184, 190, 191, 192, 193,
                    195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208,
                    209
                ],
                [
                    5, 6, 7, 8, 9, 25, 26, 28, 44, 46, 60, 61, 62, 63, 79, 90, 91, 92,
                    93, 94, 95, 105, 106, 107, 108, 109, 110, 112, 114, 117, 119, 120,
                    121, 122, 123, 124, 125, 127, 128, 130, 132, 133, 134, 137, 139, 144,
                    145, 146, 147, 148, 149, 150, 151, 152, 153, 215, 216, 217, 218, 219,
                    24, 27, 42, 43, 45, 59, 75, 76, 77, 78, 90, 91, 92, 93, 94, 96, 97,
                    98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 111, 113, 115,
                    116, 118, 119, 120, 121, 126, 129, 131, 132, 133, 135, 136, 138, 140,
                    141, 142, 143, 144, 154
                ]
            ]
        )
        yRange = 11000
    if DRIVE == 7:
        pathExt = "tGD/1to2/"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["H", "G"],
            [
                [
                    1, 6, 11, 16, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 60, 65, 70,
                    91, 96, 101, 105, 107, 109, 110, 112, 114, 115, 117, 135, 140, 156,
                    161, 165, 167, 169, 170, 172, 185, 196, 200, 202, 20, 21, 23, 25, 26,
                    28, 30, 31, 33, 35, 36, 38, 43, 48, 53, 76, 81, 86, 105, 106, 108,
                    110, 111, 113, 115, 116, 118, 123, 128, 146, 151, 165, 166, 168, 170,
                    171, 173, 178, 191, 200, 201, 203, 2, 7, 12, 17, 21, 26, 31, 36, 39,
                    40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 61, 66, 71, 92,
                    97, 102, 106, 111, 116, 119, 120, 122, 123, 124, 125, 127, 128, 129,
                    130, 136, 141, 157, 162, 166, 171, 174, 175, 177, 178, 179, 180, 186,
                    197, 201, 204, 205, 39, 41, 44, 46, 49, 51, 54, 56, 77, 82, 87, 119,
                    121, 124, 126, 129, 131, 147, 152, 174, 176, 179, 181, 192, 204, 206,
                    1, 6, 11, 16, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 60, 65, 70,
                    91, 96, 101, 105, 107, 109, 110, 112, 114, 115, 117, 135, 140, 156,
                    161, 165, 167, 169, 170, 172, 185, 196, 200, 202, 20, 21, 23, 25, 26,
                    28, 30, 31, 33, 35, 36, 38, 43, 48, 53, 76, 81, 86, 105, 106, 108,
                    110, 111, 113, 115, 116, 118, 123, 128, 146, 151, 165, 166, 168, 170,
                    171, 173, 178, 191, 200, 201, 203, 2, 7, 12, 17, 21, 26, 31, 36, 39,
                    40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 61, 66, 71, 92,
                    97, 102, 106, 111, 116, 119, 120, 122, 123, 124, 125, 127, 128, 129,
                    130, 136, 141, 157, 162, 166, 171, 174, 175, 177, 178, 179, 180, 186,
                    197, 201, 204, 205, 39, 41, 44, 46, 49, 51, 54, 56, 77, 82, 87, 119,
                    121, 124, 126, 129, 131, 147, 152, 174, 176, 179, 181, 192, 204, 206
                ],
                [
                    5, 6, 7, 8, 9, 25, 26, 28, 44, 46, 60, 61, 62, 63, 79, 90, 91, 92,
                    93, 94, 95, 105, 106, 107, 108, 109, 110, 112, 114, 117, 119, 120,
                    121, 122, 123, 124, 125, 127, 128, 130, 132, 133, 134, 137, 139, 144,
                    145, 146, 147, 148, 149, 150, 151, 152, 153, 24, 27, 42, 43, 45, 59,
                    75, 76, 77, 78, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102,
                    103, 104, 105, 106, 107, 108, 111, 113, 115, 116, 118, 119, 120, 121,
                    126, 129, 131, 132, 133, 135, 136, 138, 140, 141, 142, 143, 144, 154,
                    5, 6, 7, 8, 9, 25, 26, 28, 44, 46, 60, 61, 62, 63, 79, 90, 91, 92,
                    93, 94, 95, 105, 106, 107, 108, 109, 110, 112, 114, 117, 119, 120,
                    121, 122, 123, 124, 125, 127, 128, 130, 132, 133, 134, 137, 139, 144,
                    145, 146, 147, 148, 149, 150, 151, 152, 153, 24, 27, 42, 43, 45, 59,
                    75, 76, 77, 78, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102,
                    103, 104, 105, 106, 107, 108, 111, 113, 115, 116, 118, 119, 120, 121,
                    126, 129, 131, 132, 133, 135, 136, 138, 140, 141, 142, 143, 144, 154
                ]
            ]
        )
        yRange = 11000
    return [pathExt, aggregationDictionary, yRange]


INT_DICTIONARY = monet.generateAggregationDictionary(
    ["R1","R2,""R1+R2", "All"],
    [
        [
            13, 13, 14, 14, 18, 18, 19, 19, 32, 32, 33, 33, 37, 37, 38, 38, 50,
            50, 51, 51, 55, 55, 56, 56, 64, 64, 65, 65, 66, 66, 67, 68, 69, 69,
            70, 70, 71, 71, 72, 73, 80, 80, 81, 81, 82, 82, 83, 84, 85, 85, 86,
            86, 87, 87, 88, 89, 98, 98, 99, 99, 103, 103, 104, 104, 112, 112,
            113, 113, 117, 117, 118, 118, 125, 125, 126, 126, 130, 130, 131, 131,
            134, 134, 135, 135, 136, 136, 137, 138, 139, 139, 140, 140, 141, 141,
            142, 143, 145, 145, 146, 146, 147, 147, 148, 149, 150, 150, 151, 151,
            152, 152, 153, 154, 158, 159, 163, 164, 167, 168, 172, 173, 175, 176,
            180, 181, 184, 185, 186, 190, 191, 192, 198, 199, 202, 203, 205, 206,
            223, 223, 224, 224, 228, 228, 229, 229
        ],
        [
            0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5,
            5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
            11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 16,
            16, 16, 16, 17, 17, 17, 17, 18, 18, 19, 19, 20, 20, 20, 20, 21, 21,
            21, 21, 22, 22, 22, 22, 23, 23, 23, 23, 24, 24, 24, 24, 25, 25, 25,
            25, 26, 26, 26, 26, 27, 27, 27, 27, 28, 28, 28, 28, 29, 29, 29, 29,
            30, 30, 30, 30, 31, 31, 31, 31, 32, 32, 33, 33, 34, 34, 34, 34, 35,
            35, 35, 35, 36, 36, 36, 36, 37, 37, 38, 38, 39, 39, 39, 39, 40, 40,
            40, 40, 41, 41, 41, 41, 42, 42, 42, 42, 43, 43, 43, 43, 44, 44, 44,
            44, 45, 45, 45, 45, 46, 46, 46, 46, 47, 47, 47, 47, 48, 48, 48, 48,
            49, 49, 49, 49, 50, 50, 51, 51, 52, 52, 52, 52, 53, 53, 53, 53, 54,
            54, 54, 54, 55, 55, 56, 56, 57, 57, 57, 57, 58, 58, 58, 58, 59, 59,
            59, 59, 60, 60, 60, 60, 61, 61, 61, 61, 62, 62, 62, 62, 63, 63, 63,
            63, 64, 64, 65, 65, 66, 66, 67, 68, 69, 69, 70, 70, 71, 71, 72, 73,
            74, 74, 74, 74, 75, 75, 75, 75, 76, 76, 76, 76, 77, 77, 77, 77, 78,
            78, 78, 78, 79, 79, 79, 79, 80, 80, 81, 81, 82, 82, 83, 84, 85, 85,
            86, 86, 87, 87, 88, 89, 90, 90, 90, 90, 91, 91, 91, 91, 92, 92, 92,
            92, 93, 93, 93, 93, 94, 94, 94, 94, 95, 95, 95, 95, 96, 96, 96, 96,
            97, 97, 97, 97, 98, 98, 99, 99, 100, 100, 100, 100, 101, 101, 101,
            101, 102, 102, 102, 102, 103, 103, 104, 104, 105, 105, 105, 105, 106,
            106, 106, 106, 107, 107, 107, 107, 108, 108, 108, 108, 109, 109, 109,
            109, 110, 110, 110, 110, 111, 111, 111, 111, 112, 112, 113, 113, 114,
            114, 114, 114, 115, 115, 115, 115, 116, 116, 116, 116, 117, 117, 118,
            118, 119, 119, 119, 119, 120, 120, 120, 120, 121, 121, 121, 121, 122,
            122, 122, 122, 123, 123, 123, 123, 124, 124, 124, 124, 125, 125, 126,
            126, 127, 127, 127, 127, 128, 128, 128, 128, 129, 129, 129, 129, 130,
            130, 131, 131, 132, 132, 132, 132, 133, 133, 133, 133, 134, 134, 135,
            135, 136, 136, 137, 138, 139, 139, 140, 140, 141, 141, 142, 143, 144,
            144, 144, 144, 145, 145, 146, 146, 147, 147, 148, 149, 150, 150, 151,
            151, 152, 152, 153, 154, 155, 155, 155, 155, 156, 156, 156, 156, 157,
            157, 157, 157, 158, 159, 160, 160, 160, 160, 161, 161, 161, 161, 162,
            162, 162, 162, 163, 164, 165, 165, 165, 165, 166, 166, 166, 166, 167,
            168, 169, 169, 169, 169, 170, 170, 170, 170, 171, 171, 171, 171, 172,
            173, 174, 174, 174, 174, 175, 176, 177, 177, 177, 177, 178, 178, 178,
            178, 179, 179, 179, 179, 180, 181, 184, 185, 186, 190, 191, 192, 195,
            195, 195, 195, 196, 196, 196, 196, 197, 197, 197, 197, 198, 199, 200,
            200, 200, 200, 201, 201, 201, 201, 202, 203, 204, 204, 204, 204, 205,
            206, 210, 210, 210, 210, 211, 211, 211, 211, 212, 212, 212, 212, 213,
            213, 213, 213, 214, 214, 214, 214, 215, 215, 215, 215, 216, 216, 216,
            216, 217, 217, 217, 217, 218, 218, 218, 218, 219, 219, 219, 219, 220,
            220, 220, 220, 221, 221, 221, 221, 222, 222, 222, 222, 223, 223, 224,
            224, 225, 225, 225, 225, 226, 226, 226, 226, 227, 227, 227, 227, 228,
            228, 229, 229
        ]
    ]
)
