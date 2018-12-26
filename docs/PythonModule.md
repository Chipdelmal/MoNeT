# Python Module and Conda Environment

This module was created to accompany the [*MGDrivE*](https://marshalllab.github.io/MGDrivE/) project, although its codebase is totally independent to allow as much modularity as possible. This is not only convenient in terms of the code, but it also provides a clear-cut separation between designing and running experiments, and analysing the results.

The creation of this package is ongoing, and is currently being thoroughly tested against previous scattered scripts developed in _Mathematica_.



```Python
import MoNeT_MGDrivE as monet
# Define the experiment's path
type = float
experimentString = "E_090_050_010_025"
path = "/Users/sanchez.hmsc/Desktop/ParserDataset/"
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)
# Get the filenames lists
filenames = monet.readExperimentFilenames(path + experimentString)
# Load a single node (Auxiliary function)
nodeIndex = 0
nodeData = monet.loadNodeData(
    filenames.get("male")[nodeIndex],
    filenames.get("female")[nodeIndex],
    dataType=float
)
```

<hr>


## Authors

Sarafina Smith, Biyonka Liang, Víctor Ferman, Sabrina Wong, Héctor M. Sánchez C.
