## Roads and Buildings Shapefiles Exporter

### Instructions

Run the *exportRoadAndBuildings.py* script to parse the shapefiles for a particular *lat-long* coordinate:

```shell
python exportRoadAndBuildings.py "PLACE_NAME" lat long dist
```

This will generate folders within the *SHP* path. These folders will contain the buildings and roads shapefiles for the requested location
(a preview of the area will also be exported to the *images* folder).

* SHP folder contains the [shapefiles](https://en.wikipedia.org/wiki/Shapefile) for buildings and roads
* NTW contains the network ([graphml](https://en.wikipedia.org/wiki/GraphML)) files for roads

<img src="https://chipdelmal.github.io/MGDrivE/images/combinedView.png" width=100%>

### Requirements

This scripts requires [OSMnx](https://github.com/gboeing/osmnx) to work.
