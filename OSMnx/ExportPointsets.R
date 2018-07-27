################################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Mosquito Networks Taskforce
# Load SHP and Export LatLongs
################################################################################
rm(list=ls());gc()
library(maptools)
library(shapefiles)
library(ggplot2)
library(viridis)
library(igraph)
library(rgdal)
library(MGDrivE)
library(MGDrivEv2)
################################################################################
placeNameTag="YorkeyTrinity"
setwd("~/Documents/GitHub/MoNeT/")
outputFolder="./OSMnx/POINTS/"
################################################################################
# Read shapefile
shapeFile=read.shp(paste0("./OSMnx/SHP/Buildings/",placeNameTag,"/",placeNameTag,".shp"))
################################################################################
# Calculate the centroids of the buildings polygons and store as matrix
latLongsVoid=vector("list",length(shapeFile$shp))
latLongs=for(i in 1:length(shapeFile$shp)){
  temp=shapeFile$shp[[i]]$points
  latLongsVoid[[i]]=c(mean(temp$X),mean(temp$Y))
}
matrixLatLongs=unname(Reduce(rbind,latLongsVoid))
colnames(matrixLatLongs)=c("Latitude","Longitude")
write.table(matrixLatLongs,paste0(outputFolder,placeNameTag,"_LatLongs.csv"),sep=",",row.names=FALSE,col.names=FALSE)
################################################################################
# Calculate the distances matrix and the movement kernel
distancesMatrix=calc_haversine(matrixLatLongs)
write.table(distancesMatrix,paste0(outputFolder,placeNameTag,"_distancesMatrix.csv"),sep=",",row.names=FALSE,col.names=FALSE)
