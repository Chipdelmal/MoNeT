################################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Mosquito Networks Taskforce
# Centrality parser for shapefiles in R
################################################################################
rm(list=ls());gc()
library(maptools)
library(shapefiles)
library(ggplot2)
library(viridis)
library(MGDrivE)
library(MGDrivEv2)
library(igraph)
library(rgdal)
################################################################################
# Select the name tag of the location (same as the one used in the OSMnx parser)
# Setup your MoNeT base directory
placeNameTag="PasoRobles"
setwd("~/Documents/GitHub/MoNeT/")
outputFolder="./OSMnx/"
################################################################################
# Read shapefile
shapeFile=read.shp(paste0("./OSMnx/SHP/Buildings/",placeNameTag,"/",placeNameTag,".shp"))
################################################################################
# Plot shapefile's polygons
#shape=readOGR("./GeoLandscapes/SHP/Buildings/Moroni/")
#ggplot(data = shape, aes(x = long, y = lat, group = group)) + geom_path()
################################################################################
# Calculate the centroids of the buildings polygons and store as matrix
latLongsVoid=vector("list",length(shapeFile$shp))
latLongs=for(i in 1:length(shapeFile$shp)){
  temp=shapeFile$shp[[i]]$points
  latLongsVoid[[i]]=c(mean(temp$X),mean(temp$Y))
}
matrixLatLongs=unname(Reduce(rbind,latLongsVoid))
colnames(matrixLatLongs)=c("Latitude","Longitude")
write.table(matrixLatLongs,paste0(outputFolder,"POINTS/",placeNameTag,"_Coordinates.csv"),row.names=FALSE,col.names=FALSE,sep=",")
################################################################################
# Calculate the distances matrix and the movement kernel
distancesMatrix=calc_haversine(matrixLatLongs)
write.table(distancesMatrix,paste0(outputFolder,"DISTANCES/",placeNameTag,"_Distances.csv"),row.names=FALSE,col.names=FALSE,sep=",")
################################################################################
